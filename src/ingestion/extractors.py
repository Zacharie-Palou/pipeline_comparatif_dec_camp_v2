import pandas as pd
import os
from datetime import datetime
from config.constants import DATA_DIR
from config.constants import DECLARATIONS, UNITS, BACKUPS
from src.ingestion.connectors import get_connection
from src.utils.logger import Logger

logger = Logger()

# ============================================================
# SQL QUERIES
# ============================================================

QUERY_EXTRACT_DECLARATIONS = """
SELECT
    camp.date_donnee_debut,
    fil.cle AS filiere,
    dectyp.fk_dec_nature_cle AS type_declaration,
    typ_ong.code,
    acteur_declarant.raison_sociale AS acteur_declarant,
    SUM(lignes.{unit}) AS {unit}
FROM [{database}].[ODS].[{table}] lignes
LEFT JOIN [{database}].[ODS].[SYD_declaration] decl
    ON decl.id = lignes.fk_declaration_id
LEFT JOIN [{database}].[ODS].[SYD_dec_campagne] camp
    ON decl.fk_dec_campagne_id = camp.id
LEFT JOIN [{database}].[ODS].[SYD_dec_onglet] ong
    ON ong.id = lignes.fk_dec_onglet_id
LEFT JOIN [{database}].[ODS].[SYD_dec_onglet_type] typ_ong
    ON typ_ong.id = ong.fk_dec_onglet_type_id
LEFT JOIN [{database}].[ODS].[SYD_dec_type] dectyp
    ON dectyp.id = camp.fk_dec_type_id
LEFT JOIN [{database}].[ODS].[SYD_filiere_ref] fil
    ON dectyp.fk_filiere_cle = fil.cle
LEFT JOIN [{database}].[ODS].[SYD_inscription] insc_declarant 
    ON decl.fk_insc_iddeclarant = insc_declarant.id
LEFT JOIN [{database}].[ODS].[SYD_acteur] acteur_declarant
    ON insc_declarant.fk_acteur_id = acteur_declarant.id
WHERE camp.date_donnee_debut = ?
GROUP BY camp.date_donnee_debut, 
    acteur_declarant.raison_sociale, 
    dectyp.fk_dec_nature_cle, 
    typ_ong.code,
    fil.cle
ORDER BY camp.date_donnee_debut, fil.cle;
"""

# ============================================================
# EXTRACTORS
# ============================================================

def extract_single_declaration(
    decl_type: str,
    backups: str,
    target_year: int,
    server: str,
    database: str,
    is_corr: bool = False
) -> dict:
    """
    Extrait UNE déclaration (1 type) pour 2 unités.
    
    Args:
        decl_type (str): Type ("msm", "trt", "coll", "rrr")
        backups (str): Date format "MM-YYYY"
        target_year (int): Date format "YYYY"
        server (str): Serveur SQL
        database (str): Base de données
    
    Returns:
        dict: {"masse": df, "quantite": df}
    """
    
    # ============================================================
    # MODE DEMO
    # ============================================================
    
    import os
    
    DEMO_MODE = os.environ.get("DEMO_MODE", "true")
    if DEMO_MODE == "true":
        from config.constants import DEMO_DIR
        suffix ="_corr" if is_corr else ""
        df_demo = pd.read_csv(DEMO_DIR / f"sample_{decl_type}{suffix}.csv")
        df_masse = df_demo.drop(columns=["quantite"], errors="ignore")
        df_quantite = df_demo.drop(columns=["masse"], errors="ignore")
        return {"masse": df_masse, "quantite": df_quantite}

    # ============================================================
    
    connector = get_connection(server, database)
    
    if connector is None:
        logger.error(
            
            step="EXTRACT",
            message=f"Impossible d'extraire {decl_type} (connexion échouée)"
        )
        return {"masse": None, "quantite": None}
    
    table = DECLARATIONS[decl_type]["table"]
    results = {}

    #filter_date : date de filtrage SQL dynamique
    filter_date = datetime(target_year, 1,1)
    
    try:
        for unit in UNITS:
            logger.info(
                step="EXTRACT",
                message=f"Extraction {decl_type.upper()} - {unit.upper()} ({backups})"
            )
            
            query = QUERY_EXTRACT_DECLARATIONS.format(
                database=database,
                table=table,
                unit=unit,
            )
            
            df = pd.read_sql(query, connector, params=[filter_date])
            df["type_declaration"] = decl_type
            df["unit"] = unit
            
            results[unit] = df
            logger.info(
                step="EXTRACT",
                message=f"✓ {decl_type.upper()} {unit}: {len(df)} lignes"
            )
        
        return results
    
    except Exception as e:
        logger.error(
            step="EXTRACT",
            message=f"Erreur lors de l'extraction {decl_type}",
            exc=e
        )
        return {"masse": None, "quantite": None}
    
    finally:
        if connector is not None:
           connector.close()
           logger.info(
               step="CONNECTOR",
               message="Connexion fermée"
           )
           
def extract_all_declarations(backups: str, target_year: int, is_corr: bool =False) -> dict:
    """
    Extrait TOUTES les déclarations (4 types × 2 unités).
   
    Args:
       backups (str): Date format "MM-YYYY"
       target_year(str) : Date format "YYYY"
   
    Returns:
       dict: {"msm": {...}, "trt": {...}, ...}
    """
    
    if os.environ.get("DEMO_MODE", "true") != "true":
        logger.info(
            step="EXTRACT",
            message=f"\n{'='*60}\nEXTRACTION {backups}\n{'='*60}"
        )
    
    if backups not in BACKUPS:
        logger.error(
            step="EXTRACT",
            message=f"Date {backups} non dans BACKUPS"
        )
        return {}
    
    backup_info = BACKUPS[backups]
    server = backup_info["server"]
    database = backup_info["database"]
    
    if os.environ.get("DEMO_MODE", "true") != "true":
        logger.info(
            step="EXTRACT",
            message=f"Serveur: {server} | Base: {database}"
        )
    
    all_results = {}
    
    for decl_type in DECLARATIONS.keys():
        data = extract_single_declaration(decl_type, backups, target_year, server, database,is_corr)
        

        if (data["masse"] is None) and (data["quantite"] is None):
            logger.warning(
                step="EXTRACT",
                message=f"Aucune donnée pour {decl_type} - {backups}, création DataFrame vide"
            )
            empty_columns = ["date_donnee_debut", "filiere", "type_declaration",
                         "acteur_declarant", "code", "unit"]
            data["masse"] = pd.DataFrame(columns=empty_columns)
            data["quantite"] = pd.DataFrame(columns=empty_columns)

        all_results[decl_type] = data
    
    logger.info(
        step="EXTRACT",
        message=f"\n{'='*60}\nEXTRACTION TERMINÉE\n{'='*60}\n"
    )
    
    return all_results


def get_server_and_database(backups: str) -> tuple:
    """Retourne (server, database) pour un backups"""
    if backups not in BACKUPS:
        return None, None
    
    backup_info = BACKUPS[backups]
    return backup_info["server"], backup_info["database"]