from decimal import Decimal
from typing import Dict, Any
from uuid import UUID

class OphthalmicCorrelationEngine:
    """
    Motor automatizado para correlation-linking de procedimentos cirúrgicos,
    alocação de OPME e pré-formatação de guias ANS/TISS.
    """
    
    SURGICAL_PROTOCOL_REGISTRY: Dict[str, Dict[str, Any]] = {
        "30306027": {  # Facoemulsificação com implante de LIO
            "description": "Facoemulsificação c/ LIO",
            "opme_kit": ["LIO_FOBICA_HIDROFILICA", "VISCOELASTICO_2.0", "AZUL_DE_TRIPANO"],
            "surgical_roles": ["Cirurgiao", "Primeiro_Auxiliar", "Anestesista"],
            "anesthetic_porte": "3",
            "default_cbhpm": "3.03.06.02-7",
            "cid10_compatible": ["H25.0", "H25.1", "H25.8", "H26.9"]
        },
        "30304059": {  # YAG Laser / Capsulotomia
            "description": "Capsulotomia a YAG Laser",
            "opme_kit": [],
            "surgical_roles": ["Cirurgiao"],
            "anesthetic_porte": "0",
            "default_cbhpm": "3.03.04.05-9",
            "cid10_compatible": ["H26.4"]
        }
    }

    @classmethod
    def trigger_surgical_workflow(
        cls, 
        tuss_code: str, 
        patient_id: UUID, 
        surgeon_id: UUID, 
        cid10_diag: str
    ) -> Dict[str, Any]:
        protocol = cls.SURGICAL_PROTOCOL_REGISTRY.get(tuss_code)
        if not protocol:
            raise ValueError(f"Procedimento {tuss_code} não indexado para automação.")
            
        if cid10_diag not in protocol["cid10_compatible"]:
            # Alerta de inconsistência clínica com risco de glosa
            glosa_risk = True
        else:
            glosa_risk = False

        guide_payload = {
            "tuss_code": tuss_code,
            "cbhpm_code": protocol["default_cbhpm"],
            "opme_allocated": protocol["opme_kit"],
            "glosa_risk_flag": glosa_risk,
            "team_allocation": protocol["surgical_roles"],
            "financial_event": "CONTAS_A_RECEBER_PENDENTE_AUTORIZACAO"
        }
        return guide_payload
