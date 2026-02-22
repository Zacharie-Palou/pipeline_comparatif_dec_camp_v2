import pandas as pd
import numpy as np
from config.constants import EVOLUTION_THRESHOLD
from src.utils.logger import Logger

logger = Logger()

def filter_by_evolution_threshold(
    df: pd.DataFrame,
    threshold: float = None,
) -> pd.DataFrame:
    """
    Filtre les lignes ayant un taux d'évolution >= threshold (en valeur absolue).
    
    Args:
        df (pd.DataFrame): DataFrame avec colonnes d'évolution
        threshold (float): Seuil en % (ex: 0.01 pour 1%)
        unit (str): "masse" ou "quantite"
    
    Returns:
        pd.DataFrame: Filtré
    """
    
    if threshold is None:
        threshold = EVOLUTION_THRESHOLD
    
    if "Taux d'évolution (abs)" not in df.columns:
       logger.warning(
           step="FILTER",
           message=f"Colonne 'Taux d'évolution (abs)' non trouvée"
       )
       return df
    
    before = len(df)
    df_filtered = df[df["Taux d'évolution (abs)"] >= threshold].copy()
    after = len(df_filtered)
    
    logger.info(
        step="FILTER",
        message=f"Filtrage 'Taux d'évolution (abs)' >= {threshold*100:.1f}%: {before} → {after} lignes"
    )
    
    return df_filtered


def filter_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtre les anomalies (NaN, infinies, etc.).
    
    Args:
        df (pd.DataFrame): DataFrame
        unit (str): "masse" ou "quantite"
    
    Returns:
        pd.DataFrame: Filtré
    """
    
    df = df.copy()
    
    if "Taux d'évolution (abs)" not in df.columns:
        return df
    
    # Supprimer infinies et NaN
    df = df[~df["Taux d'évolution (abs)"].isin([np.inf, -np.inf])]
    df = df[df["Taux d'évolution (abs)"].notna()]
    
    logger.info(
        step="FILTER",
        message=f"Anomalies supprimées ('Taux d'évolution (abs)': {len(df)} lignes"
    )
    
    return df