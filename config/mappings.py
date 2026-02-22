# ============================================================
# DECLARATIONS TYPE MAPPING
# ============================================================

TYPE_DECLARATION = {"coll": "Collecte",
                    "trt": "Traitement",
                    "msm": "MSM",
                    "rrr": "RR"}

# ============================================================
# FILIÈRE MAPPINGS
# ============================================================

FILIERE_MAPPINGS = {
    "EMPAP": "EMBM",  # Exemple: EMPAP en 2025 devient EMBM en 2024
    # Ajouter d'autres mappings si nécessaire
}

# ============================================================
# TYPE MESURE MAPPING
# ============================================================

TYPE_MESURE = {
    "masse": "Tonnage",
    "quantite": "Quantite"}

def apply_filiere_mapping(filiere: str, date: str) -> str:
    """
    Applique les mappings de filière selon la date.
    
    Args:
        filiere (str): Code filière original
        date (str): Date au format MM-YYYY
    
    Returns:
        str: Code filière après mapping
    """
    # Extraire année de la date (format MM-YYYY)
    year = int(date.split("-")[1])
    
    # Appliquer mappage EMBM → EMPAP si année = 2024
    if year == 2025 and filiere in FILIERE_MAPPINGS:
        return FILIERE_MAPPINGS[filiere]
    
    return filiere

def apply_declaration_mapping(declaration: str)-> str:
    """
    Applique les mappings type de déclaration.

    Args: declaration
        
    Returns
        str: Code déclaration après maping
    """
    return TYPE_DECLARATION.get(declaration, declaration)
    
def apply_mesure_mapping(mesure:str)-> str:
    """
    Applique les mappings type de mesure.

    Args: mesure
        
    Returns
        str: Code mesure après maping
    """
    return TYPE_MESURE.get(mesure, mesure)