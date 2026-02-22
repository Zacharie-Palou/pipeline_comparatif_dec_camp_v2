import pandas as pd
from src.utils.logger import Logger

logger = Logger()

def aggregate_by_filiere(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrège les données par filière.
    Calcule taux d'évolution globale par filière.
    
    Args:
        df (pd.DataFrame): DataFrame avec colonnes "Déclaration initiale" et "Déclaration corrective"
    
    Returns:
        pd.DataFrame: Agrégé par filière avec taux d'évolution
    """
    
    logger.info(step="AGGREGATE", message="Agrégation par filière")
    
    # Somme des valeurs par filière
    df_agg = df.groupby("Filière").agg({
        "Déclaration initiale": "sum",
        "Déclaration corrective": "sum"
    }).reset_index()
    
    # Calcul du taux d'évolution (%)
    df_agg["Taux d'évolution"] = (
        (df_agg["Déclaration corrective"] - df_agg["Déclaration initiale"]) 
        / df_agg["Déclaration initiale"] * 100
    ).round(2)
    
    logger.info(step="AGGREGATE", message=f"✓ Agrégation: {len(df_agg)} filières")
    
    return df_agg


def aggregate_by_declaration_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrège les données par type de déclaration.
    
    Args:
        df (pd.DataFrame): DataFrame avec colonnes "Déclaration initiale" et "Déclaration corrective"
    
    Returns:
        pd.DataFrame: Agrégé par type déclaration avec taux d'évolution
    """
    
    logger.info(step="AGGREGATE", message="Agrégation par type déclaration")
    
    df_agg = df.groupby("Type de déclaration").agg({
        "Déclaration initiale": "sum",
        "Déclaration corrective": "sum"
    }).reset_index()
    
    # Calcul du taux d'évolution (%)
    df_agg["Taux d'évolution"] = (
        (df_agg["Déclaration corrective"] - df_agg["Déclaration initiale"])
        / df_agg["Déclaration initiale"] * 100
    )
    
    logger.info(step="AGGREGATE", message=f"✓ {len(df_agg)} types déclaration")
    
    return df_agg

def aggregate_dashboard(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivot dashboard : filières × code → taux d'évolution global.
    """
    logger.info(step="AGGREGATE", message="Création dashboard pivot")

    # Agrégation par filière + type de mesure + type de déclaration
    df_agg = df.groupby(["Filière", "Type de mesure", "Code"]).agg(
        total_init=("Déclaration initiale", "sum"),
        total_corr=("Déclaration corrective", "sum")
    ).reset_index()

    # Taux global : (somme corr - somme init) / somme init
    df_agg["Taux global"] = (
        (df_agg["total_corr"] - df_agg["total_init"])
        / df_agg["total_init"].replace(0, float("nan"))
    )

    df_pmcb = df_agg[(df_agg["Filière"] == "PMCB") & (df_agg["Type de mesure"] == "Tonnage")]
    print(df_pmcb[["Filière", "Type de mesure", "Code", "total_init", "total_corr", "Taux global"]])

    # Pivot
    df_pivot = df_agg.pivot_table(
        index=["Filière", "Type de mesure"],
        columns="Code",
        values="Taux global",
        aggfunc="first"
    )

    df_pivot.columns.name = None
    df_pivot = df_pivot.reset_index()

    logger.info(step="AGGREGATE", message=f"✓ Dashboard: {len(df_pivot)} lignes")

    return df_pivot