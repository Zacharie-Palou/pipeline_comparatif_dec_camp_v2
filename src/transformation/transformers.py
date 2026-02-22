import pandas as pd
from config.mappings import apply_filiere_mapping,apply_declaration_mapping, apply_mesure_mapping
from src.utils.logger import Logger

logger = Logger()

def apply_business_mappings(df: pd.DataFrame, date: str, declaration:str) -> pd.DataFrame:
    """
    Applique les mappings métier.
    - EMBM → EMPAP (filière)
    
    Args:
        df (pd.DataFrame): DataFrame standardisé
        date (str): Date au format MM-YYYY
    
    Returns:
        pd.DataFrame: DataFrame mappé
    """
    
    if df is None or df.empty:
        return df
    
    df = df.copy()
    
    # Appliquer mapping filière
    if "Filière" in df.columns:
        df["Filière"] = df["Filière"].apply(
            lambda x: apply_filiere_mapping(x, date)
        )


    if "Type de déclaration" in df.columns:
        df["Type de déclaration"] = df["Type de déclaration"].apply(
            lambda x : apply_declaration_mapping(x)
            )
        
    if "Type de mesure" in df.columns:
        df["Type de mesure"] = df["Type de mesure"].apply(
            lambda x : apply_mesure_mapping(x)
            )
        
        logger.info(
            step="MAPPING",
            message="Mapping delcaration appliqué)"
        )

    return df