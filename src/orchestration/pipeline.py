import pandas as pd
from config.constants import BACKUPS
from src.ingestion.extractors import extract_all_declarations
from src.transformation.standardizers import (
    standardize_declaration_df,
    combine_units,
)
from src.transformation.transformers import (
    apply_business_mappings
)
from src.processing.mergers import merge_init_corr
from src.processing.calculators import calculate_metrics
from src.processing.filters import filter_by_evolution_threshold
from src.processing.aggregators import aggregate_dashboard
from src.output.excel_writer import write_multi_sheet_excel
from src.utils.logger import Logger

# ============================================================
# PIPELINE ORCHESTRATION
# 
# V2 - Refactorisation complète depuis une V1 en God Function
# Objectif : architecture modulaire, peu dépendante au schéma,
# règles métier évolutives et gestion d'exceptions robuste.
# ============================================================

class DataPipeline:

    def __init__(self, log_level: str = "INFO"):
        self.logger = Logger()
        self.log_level = log_level

    def run(self, dec_init: str, dec_corr: str, target_year:int, output_path: str) -> None:

        try:
            # ========== LAYER 1: INGESTION ==========
            self.logger.info("PIPELINE", "\n[LAYER 1] INGESTION")

            data_init = extract_all_declarations(dec_init, target_year, is_corr=False)
            data_corr = extract_all_declarations(dec_corr, target_year, is_corr=True)

            # ========== LAYER 2: TRANSFORMATION ==========
            self.logger.info("PIPELINE", "\n[LAYER 2] TRANSFORMATION")

            df_init = self._transform_declarations(data_init, dec_init)
            df_corr = self._transform_declarations(data_corr, dec_corr)
            
            df_init = df_init.rename(columns={"Valeur": "Déclaration initiale"})
            df_corr = df_corr.rename(columns={"Valeur": "Déclaration corrective"})

            # ========== LAYER 3: PROCESSING ==========
            self.logger.info("PIPELINE", "\n[LAYER 3] PROCESSING")

            if df_init is None:
                raise ValueError("df_init est None après extraction")

            if df_corr is None:
                raise ValueError("df_corr est None après extraction")

            # Merge
            df_merged = merge_init_corr(df_init, df_corr)

            # Calcul métriques
            df_stats = calculate_metrics(df_merged, "Déclaration initiale", "Déclaration corrective")

            print(df_stats["Type de déclaration"].unique())

            # Filtrer
            #df_stats_filtered = filter_by_evolution_threshold(df_stats)

            # Dashboard
            df_dashboard = aggregate_dashboard(df_stats)

            # ========== LAYER 4: OUTPUT ==========
            self.logger.info("PIPELINE", "\n[LAYER 4] OUTPUT")

            sheets = {
                "INIT": df_init,
                "CORR": df_corr,
                "STATS": df_stats,
                #"ANALYSE": df_stats_filtered,
                "DASHBOARD": df_dashboard,
            }

            write_multi_sheet_excel(sheets, output_path, overwrite=False)

        except Exception as e:
            self.logger.error("PIPELINE", "Erreur critique", exc=e)
            raise

    def _transform_declarations(self, data_raw: dict, date: int):

        dfs_combined = []

        for decl_type, data in data_raw.items():
            df_masse = data.get("masse")
            df_quantite = data.get("quantite")

            # Combiner masse + quantité
            df_combined = combine_units(df_masse, df_quantite)

            # Standardiser
            df_standardized = standardize_declaration_df(df_combined)

            # Gestion execeptions via apply_business_mapping ex : 2025 
            # Appliquer mappings
            df = apply_business_mappings(df_standardized, date, decl_type)

            dfs_combined.append(df)     

        # Fusion des types
        if dfs_combined:
            df_final = pd.concat(dfs_combined, ignore_index=True)

            self.logger.info(
                "TRANSFORM",
                f"✓ Fusion des types ({date}) : {len(df_final)} lignes"
            )

            return df_final

        return None
