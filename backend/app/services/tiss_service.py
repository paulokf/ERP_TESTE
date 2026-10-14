import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List
from app.models.billing import GuiaTISS, StatusGuiaEnum

class TISSService:
    @staticmethod
    def validar_guia(guia: GuiaTISS) -> List[str]:
        """Aplica regras de validação pré-faturamento para evitar glosas ANS."""
        erros = []
        if not guia.numero_carteira_beneficiario or len(guia.numero_carteira_beneficiario) < 5:
            erros.append("Número da carteira do beneficiário inválido.")
        if not guia.codigo_tuss or len(guia.codigo_tuss) != 8:
            erros.append("Código TUSS deve possuir 8 dígitos no padrão ANS.")
        if guia.valor_procedimento <= 0:
            erros.append("Valor do procedimento deve ser superior a R$ 0,00.")
        return erros

    @staticmethod
    def gerar_xml_lote(lote_id: str, guias: List[GuiaTISS], cnpj_prestador: str = "00000000000100") -> str:
        """Gera payload XML no formato TISS estruturado para operadoras."""
        root = ET.Element("mensagemTISS", xmlns="http://www.ans.gov.br/padroes/tiss/schemas")
        
        cabecalho = ET.SubElement(root, "cabecalho")
        identificacao = ET.SubElement(cabecalho, "identificacaoTransacao")
        ET.SubElement(identificacao, "tipoTransacao").text = "ENVIO_LOTE_GUIAS"
        ET.SubElement(identificacao, "numeroLote").text = lote_id
        ET.SubElement(identificacao, "dataRegistroTransacao").text = datetime.utcnow().strftime("%Y-%m-%d")
        ET.SubElement(identificacao, "horaRegistroTransacao").text = datetime.utcnow().strftime("%H:%M:%S")

        origem = ET.SubElement(cabecalho, "origem")
        ET.SubElement(origem, "cnpjPrestador").text = cnpj_prestador

        lote_guias = ET.SubElement(root, "loteGuias")
        for g in guias:
            guia_el = ET.SubElement(lote_guias, "guiaFaturamento")
            ET.SubElement(guia_el, "numeroGuiaPrestador").text = g.numero_guia_prestador
            ET.SubElement(guia_el, "numeroCarteira").text = g.numero_carteira_beneficiario
            ET.SubElement(guia_el, "nomeBeneficiario").text = g.nome_beneficiario
            ET.SubElement(guia_el, "convenio").text = g.convenio
            
            proc_el = ET.SubElement(guia_el, "procedimento")
            ET.SubElement(proc_el, "codigoTUSS").text = g.codigo_tuss
            ET.SubElement(proc_el, "descricao").text = g.descricao_procedimento
            ET.SubElement(proc_el, "valorTotal").text = f"{g.valor_procedimento:.2f}"
            
            prof = ET.SubElement(guia_el, "profissionalExecutante")
            ET.SubElement(prof, "crm").text = g.medico_crm
            ET.SubElement(prof, "uf").text = g.medico_uf

        return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")
