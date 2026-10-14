import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

os.makedirs("manuais_pdf", exist_ok=True)

def criar_manual(filename, titulo, perfil, cor_primaria, modulos):
    doc = SimpleDocTemplate(
        f"manuais_pdf/{filename}",
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = getSampleStyleSheet()

    # Estilos customizados
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=cor_primaria,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#475569'),
        spaceAfter=14
    )
    sec_title_style = ParagraphStyle(
        'SecTitle',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=cor_primaria,
        spaceBefore=10,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=6
    )
    step_style = ParagraphStyle(
        'Step',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#0F172A')
    )

    story = []

    # Cabeçalho
    story.append(Paragraph(f"CliniCore ERP — {titulo}", title_style))
    story.append(Paragraph(f"<b>Perfil Alvo (RBAC):</b> {perfil} &nbsp;|&nbsp; <b>Versão:</b> 2.0 &nbsp;|&nbsp; <b>Conformidade:</b> ANS/TISS • CFM", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=cor_primaria, spaceAfter=14))

    for mod in modulos:
        story.append(Paragraph(mod['titulo'], sec_title_style))
        story.append(Paragraph(mod['descricao'], body_style))
        
        tabela_dados = [[Paragraph("<b>Passo / Ação</b>", step_style), Paragraph("<b>Procedimento Operacional no Sistema</b>", step_style)]]
        for passo, desc in mod['passos']:
            tabela_dados.append([Paragraph(f"<b>{passo}</b>", step_style), Paragraph(desc, step_style)])
        
        t = Table(tabela_dados, colWidths=[120, 420])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t)
        story.append(Spacer(1, 12))

    # Rodapé de assinatura
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#CBD5E1'), spaceAfter=8))
    story.append(Paragraph("<i>Manual gerado eletronicamente em 29/09/2026. CliniCore ERP — Uso estritamente restrito e confidencial.</i>", ParagraphStyle('Foot', parent=styles['Italic'], fontSize=8, textColor=colors.HexColor('#64748B'))))

    doc.build(story)
    print(f"✅ Manual gerado com sucesso: manuais_pdf/{filename}")

# DADOS DOS 4 MANUAIS

# 1. Recepção
criar_manual(
    filename="Manual_Recepcao_Atendimento.pdf",
    titulo="Manual de Operação: Recepção & Atendimento",
    perfil="Recepção / Atendente / Pré-cadastro",
    cor_primaria=colors.HexColor('#2563EB'),
    modulos=[
        {
            "titulo": "1. Módulo de Agendamentos (/dashboard/agendamento)",
            "descricao": "Controle central de reservas de consultas e exames, respeitando a trava máxima de 3 consultórios físicos simultâneos.",
            "passos": [
                ("1.1 Novo Agendamento", "Acesse a tela de Agendamentos, selecione o Paciente, Médico e Horário. O sistema valida se o consultório está livre."),
                ("1.2 Novo Paciente", "Clique em '+ Novo Paciente'. Preencha Nome, CPF, Contato, CEP (com busca automática) e Convênio/Carteirinha."),
                ("1.3 Calendário Mensal", "Clique em 'Calendário Mensal da Clínica' para visualizar em grade os pacientes e médicos alocados dia a dia."),
                ("1.4 Carga Diária", "Acesse 'Carga Diária & Lista de Pacientes' para conferir os atendimentos do plantão em tempo real.")
            ]
        },
        {
            "titulo": "2. Chat Interno da Clínica (/dashboard/chat)",
            "descricao": "Canal seguro de comunicação em tempo real entre a recepção e os médicos em consultório.",
            "passos": [
                ("2.1 Avisar Chegada", "Selecione o Consultório (1, 2 ou 3) na barra lateral do Chat e envie aviso de chegada e liberação da guia."),
                ("2.2 Mensagens Rápidas", "Utilize para tirar dúvidas sobre guias TUSS ou solicitar autorização de encaixe diretamente ao médico.")
            ]
        }
    ]
)

# 2. Corpo Clínico
criar_manual(
    filename="Manual_Corpo_Clinico_PEP.pdf",
    titulo="Manual de Operação: Corpo Clínico & Cirúrgico",
    perfil="Médico Oftalmologista / Cirurgião / Especialista",
    cor_primaria=colors.HexColor('#0284C7'),
    modulos=[
        {
            "titulo": "1. Prontuário Eletrônico Oftalmológico (/dashboard/pep)",
            "descricao": "Registro de consulta oftalmológica em tela bilateral (Olho Direito e Olho Esquerdo) em estrita conformidade CFM nº 1.821/2007.",
            "passos": [
                ("1.1 Seleção do Paciente", "Selecione o paciente agendado no topo. O histórico prévio e a queixa principal serão carregados."),
                ("1.2 Acuidade & Refração", "Lance nos campos bilaterais de OD e OE a Acuidade Visual (Snellen), Esférico, Cilíndrico, Eixo e Adição."),
                ("1.3 Tonometria & Bio", "Registre a Pressão Intraocular (mmHg) e descreva os achados do Segmento Anterior e Fundoscopia."),
                ("1.4 CID-10 & Prognóstico", "Insira o diagnóstico CID-10, determine a conduta e informe o prognóstico na aba clínica dedicada."),
                ("1.5 Salvar & Assinar", "Clique em 'Salvar Atendimento Oftalmológico (CFM)' para gerar o carimbo de tempo e a assinatura digital SHA-256.")
            ]
        }
    ]
)

# 3. Faturamento e Financeiro
criar_manual(
    filename="Manual_Faturamento_Financeiro.pdf",
    titulo="Manual de Operação: Faturamento & Financeiro",
    perfil="Faturamento TISS/TUSS / Analista Financeiro / Controladoria",
    cor_primaria=colors.HexColor('#059669'),
    modulos=[
        {
            "titulo": "1. Módulo Faturamento TISS/TUSS (/dashboard/faturamento)",
            "descricao": "Gestão de guias médicas, validação TUSS e empacotamento em Lotes XML padrão ANS.",
            "passos": [
                ("1.1 Filtragem de Guias", "Consulte guias por status: 'Todas', 'Pendentes', 'Faturadas' ou 'Glosadas'."),
                ("1.2 Geração de Lote XML", "Clique em 'Gerar Lote XML' para empacotar as guias aprovadas no padrão TISS 4.01."),
                ("1.3 Emissão de NFS-e", "Utilize o botão de Nota Fiscal para carregar os dados cadastrais do tomador e serviço para emissão.")
            ]
        },
        {
            "titulo": "2. Módulo Financeiro & Repasses (/dashboard/financeiro)",
            "descricao": "Livro-razão, controle de fluxo de caixa operacional e DRE anual estruturado.",
            "passos": [
                ("2.1 Nova Transação", "Registre lançamentos de Receita ou Despesa, categorizando e vinculando opcionalmente à guia TISS."),
                ("2.2 Relatório DRE Anual", "Abra o modal de DRE para acompanhar a tabela horizontal de 12 meses (meses futuros em branco e cálculo YTD)."),
                ("2.3 Gráfico Comparativo", "Analise visualmente as barras mensais de receitas vs despesas para tomada de decisão.")
            ]
        }
    ]
)

# 4. Gestão, RH e Auditoria
criar_manual(
    filename="Manual_Gestao_RH_Auditoria.pdf",
    titulo="Manual de Operação: Gestão, RH & Auditoria LGPD",
    perfil="Administrador / DPO LGPD / Recursos Humanos / Auditoria",
    cor_primaria=colors.HexColor('#475569'),
    modulos=[
        {
            "titulo": "1. Recursos Humanos & Acessos (/dashboard/rh)",
            "descricao": "Gestão de colaboradores com perfis de controle de acesso baseado em função (RBAC).",
            "passos": [
                ("1.1 Novo Colaborador", "Clique em 'Novo Colaborador'. Preencha Nome, E-mail, Senha Provisória e atribua o Nível de Acesso (Role)."),
                ("1.2 Registro de Conselho", "Para o corpo clínico, preencha o número de registro e UF para formatação automática (ex: CRM 54210/SP e RQE).")
            ]
        },
        {
            "titulo": "2. Auditoria & Conformidade LGPD (/dashboard/auditoria)",
            "descricao": "Trilha imutável append-only com rastreabilidade de IP, operador, ação e hash SHA-256.",
            "passos": [
                ("2.1 Filtros Avançados", "Abra o modal de filtros para cruzar Data, Operador, Endereço IP, Nível de Risco e Entidade afetada."),
                ("2.2 Rastreio de Laudos", "Confira o hash SHA-256 gerado em cada laudo e prontuário para garantir a integridade do dado."),
                ("2.3 Exportar CSV", "Clique em 'Exportar Relatório (CSV)' para baixar a planilha consolidada para auditoria externa.")
            ]
        }
    ]
)
