# backend/app/constants/tuss_catalog.py

OPHTHALMIC_TUSS_CATALOG = {
    "10101012": "Consulta em consultório (médico)",
    "41301265": "Mapeamento de retina (oftalmoscopia indireta) - monocular",
    "41301257": "Campimetria computadorizada - monocular",
    "41301290": "Tonometria de aplanação - binocular",
    "41301303": "Paquimetria ultrassônica - monocular",
    "41301419": "Biometria ultrassônica - monocular",
    "41301338": "Tomografia de coerência óptica (OCT) - monocular",
    "30306027": "Facoemulsificação com implante de lente intraocular",
    "30304059": "Capsulotomia a YAG Laser",
    "30304067": "Iridotomia / Iridectomia a Laser",
    "30307040": "Trabeculectomia (Cirurgia antiglaucomatosa)",
    "30301033": "Exérese de pterígio com transplante conjuntival"
}

def is_valid_tuss(tuss_code: str) -> bool:
    """Verifica se o código TUSS pertence ao rol homologado da clínica."""
    return tuss_code in OPHTHALMIC_TUSS_CATALOG

def get_tuss_description(tuss_code: str) -> str:
    """Retorna a descrição oficial do procedimento ou fallback genérico."""
    return OPHTHALMIC_TUSS_CATALOG.get(tuss_code, "Procedimento não identificado na tabela básica")

