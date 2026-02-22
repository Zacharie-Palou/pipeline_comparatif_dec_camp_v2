import pandas as pd
import numpy as np
from config.constants import DECIMAL, EVOLUTION_THRESHOLD
from src.utils.logger import Logger

logger = Logger()

def calculate_metrics(
    df: pd.DataFrame,
    col_init: str,
    col_corr: str,
    sort_keys: list[str] | None = None,
    filter_threshold: bool = True
) -> pd.DataFrame:
    """
    Calcule les métriques d'évolution.
    - Différence absolue
    - Taux d'évolution (%)
    - Taux d'évolution absolue (%)
    
    Args:
        df (pd.DataFrame): DataFrame mergé avec colonnes _INIT et _CORR
        filter_threshold (bool): appliquer ou non le filtre EVOLUTION_THRESHOLD
    
    Returns:
        pd.DataFrame: Avec colonnes de métriques
    """
    
    df_stats = df.copy()
    
    logger.info(
        step="CALCULATE",
        message="Calcul des métriques d'évolution"
    )
    
    # Conversion en numérique sécurisée
    df_stats[col_init] = pd.to_numeric(df_stats[col_init], errors='coerce')
    df_stats[col_corr] = pd.to_numeric(df_stats[col_corr], errors='coerce')
    
    # Calcul vectorisé des écarts et taux d'évolution
    df_stats["Écart"] = df_stats[col_corr] - df_stats[col_init]
    
    # Taux d'évolution, avec protection contre division par zéro
    df_stats["Taux d'évolution"] = (df_stats["Écart"] / df_stats[col_init].replace({0: np.nan}))  #.round(DECIMAL)
    
    # Valeur absolue
    df_stats["Taux d'évolution (abs)"] = df_stats["Taux d'évolution"].abs()  #.round(DECIMAL)

    
    # Tri final si nécessaire
    if sort_keys:
        df_stats = df_stats.sort_values(by=sort_keys).reset_index(drop=True)
    
    return df_stats