import pandas as pd
from src.utils.logger import Logger

logger = Logger()

def combine_units(df_masse: pd.DataFrame, df_quantite: pd.DataFrame) -> pd.DataFrame:
    """
    Combine masse et quantité en un seul DataFrame.
    
    Args:
        df_masse (pd.DataFrame): DF avec colonne 'masse'
        df_quantite (pd.DataFrame): DF avec colonne 'quantite'
    
    Returns:
        pd.DataFrame: DF fusionné
    """
    
    dfs = []

    if df_masse is not None and "masse" in df_masse.columns and not df_masse.empty:
        df_m = df_masse.copy()
        df_m["unit"] = "masse"
        df_m["Valeur"] = df_m["masse"]
        df_m = df_m.drop(columns=["masse"], errors="ignore")
        dfs.append(df_m)

    if df_quantite is not None and "quantite" in df_quantite.columns and not df_quantite.empty:
        df_q = df_quantite.copy()
        df_q["unit"] = "quantite"
        df_q["Valeur"] = df_q["quantite"]
        df_q = df_q.drop(columns=["quantite"], errors="ignore")
        dfs.append(df_q)

    if not dfs:
        return pd.DataFrame()

    df_combined = pd.concat(dfs, ignore_index=True)
    df_combined = df_combined.dropna(axis=1, how="all")

    return df_combined

def standardize_declaration_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardise une déclaration.
    - Renomme colonnes
    - Ajuste types
    - Ajoute colonnes métadonnées
    
    Args:
        df (pd.DataFrame): DataFrame brut
        date (str): Date au format MM-YYYY
    
    Returns:
        pd.DataFrame: DataFrame standardisé
    """
    
    if df is None or df.empty:
        logger.warning(
            step="STANDARDIZE",
            message="DataFrame vide, retour direct"
        )
        return None
    
    df = df.copy()
    
    # Renommer colonnes (standard commun)
    column_mapping = {
        "date_donnee_debut": "Date de déclaration",
        "filiere": "Filière",
        "type_declaration": "Type de déclaration",
        "code": "Code",
        "acteur_declarant": "Déclarant",
        "unit": "Type de mesure",
        "valeur": "Valeur",
    }
    
    df.rename(columns=column_mapping, inplace=True)
            
    if "Valeur" in df.columns:
        df["Valeur"] = pd.to_numeric(df["Valeur"], errors="coerce")
    
    logger.info(
        step="STANDARDIZE",
        message=f"✓ Standardisation: {len(df)} lignes, {len(df.columns)} colonnes"
    )
    
    return df