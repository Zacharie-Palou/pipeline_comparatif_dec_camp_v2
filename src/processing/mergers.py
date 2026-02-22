import pandas as pd
from src.utils.logger import Logger

logger = Logger()

def merge_init_corr(
    df_init: pd.DataFrame,
    df_corr: pd.DataFrame,
    how: str = "outer"
) -> pd.DataFrame:

    logger.info(
        step="MERGE",
        message="Fusion déclaration initiale vs corrective"
    )
    
    if df_init is None or df_corr is None:
        raise ValueError("Extraction initiale ou corrective vide")
    
    df_n1 = df_init.copy()
    df_n2 = df_corr.copy()
    
    val_col_1 = "Déclaration initiale"
    val_col_2 = "Déclaration corrective"

    key_cols = ["Date de déclaration", "Filière", "Type de déclaration", "Code", "Déclarant", "Type de mesure"]

    # Merge complet pour avoir toutes les combinaisons possibles
    df_merged = pd.merge(
        df_n1,
        df_n2,
        on=key_cols,
        how=how
    )

    df_merged[val_col_1] = pd.to_numeric(df_merged[val_col_1], errors='coerce')
    df_merged[val_col_2] = pd.to_numeric(df_merged[val_col_2], errors='coerce')

    return df_merged