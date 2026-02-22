"""
Validation des données et entrées.
"""

from config.constants import BACKUPS
from src.utils.logger import Logger

logger = Logger()


def validate_date(date: str) -> bool:
    """
    Valide qu'une date est dans BACKUPS.
    
    Args:
        date (str): Date format MM-YYYY
    
    Returns:
        bool: True si valide
    """
    if date not in BACKUPS:
        logger.error(
            "VALIDATE",
            f"Date {date} non reconnue. Disponibles: {list(BACKUPS.keys())}"
        )
        return False
    return True


def validate_dataframe(df, expected_cols: list = None) -> bool:
    """
    Valide un DataFrame.
    
    Args:
        df: DataFrame à valider
        expected_cols (list): Colonnes attendues
    
    Returns:
        bool: True si valide
    """
    
    if df is None:
        logger.warning("VALIDATE", "DataFrame est None")
        return False
    
    if df.empty:
        logger.warning("VALIDATE", "DataFrame est vide")
        return False
    
    if expected_cols:
        missing = [col for col in expected_cols if col not in df.columns]
        if missing:
            logger.warning("VALIDATE", f"Colonnes manquantes: {missing}")
            return False
    
    return True