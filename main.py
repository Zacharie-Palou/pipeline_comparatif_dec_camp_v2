import sys
import warnings 
import shutil # Copie du rapport
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.constants import OUTPUT_DIR, BACKUPS, DEMO_MODE
from src.orchestration.pipeline import DataPipeline
from src.utils.helpers import build_report_filename
from src.utils.logger import Logger

# ============================================================
# Renseignez juste ces 3 variables et exécutez le script
# ============================================================

# À MODIFIER
DEC_INIT = "10-2024"      # ← Déclaration initiale
DEC_CORR = "06-2025"      # ← Déclaration corrective
TARGET_YEAR = 2023

# ============================================================
# NE RIEN MODIFIER APRÈS CETTE LIGNE
# ============================================================

if DEMO_MODE == "true":
    OUTPUT_PATH = OUTPUT_DIR / "rapport_demo.xlsx"
else:
    OUTPUT_PATH = OUTPUT_DIR / build_report_filename(TARGET_YEAR, [DEC_INIT, DEC_CORR])

# Ignorer le warning spécifique de pandas
warnings.filterwarnings(
    "ignore",
    message="pandas only supports SQLAlchemy connectable"
)

logger = Logger()

def main():
    """Fonction principale simplifiée pour Spyder"""

    try:
        # =========================
        # Validation des dates
        # =========================
        if DEC_INIT not in BACKUPS:
            print(f"❌ Erreur: DEC_INIT='{DEC_INIT}' non valide")
            print(f"   Dates disponibles: {list(BACKUPS.keys())}")
            return

        if DEC_CORR not in BACKUPS:
            print(f"❌ Erreur: DEC_CORR='{DEC_CORR}' non valide")
            print(f"   Dates disponibles: {list(BACKUPS.keys())}")
            return

        # =========================
        # Affichage infos
        # =========================
        print("\n" + "=" * 60)
        print("PIPELINE COMPARATIF DÉCLARATIONS")
        print("=" * 60)
        print(f"\nDéclaration INITIALE: {DEC_INIT}")
        print(f"Déclaration CORRECTIVE: {DEC_CORR}")
        print(f"Rapport Excel: {OUTPUT_PATH}")
        print("\n" + "=" * 60)

        # =========================
        # Lancement pipeline
        # =========================
        
        ADEME_PATH = Path(r"C:\Users\palouz\ADEME\O-DSREP - 08-ValorisationCom\Donnees-Transverses\Différenciel_declaration_automat\Rapport_final\Rapport_pip_v2")
        
        pipeline = DataPipeline(log_level="INFO")
        pipeline.run(
            dec_init=DEC_INIT,
            dec_corr=DEC_CORR,
            target_year=TARGET_YEAR,
            output_path=OUTPUT_PATH
        )

        # shutil.copy(OUTPUT_PATH, ADEME_PATH / OUTPUT_PATH.name)

        print("\n" + "=" * 60)
        print("✓ TERMINÉ AVEC SUCCÈS")
        print(f"Rapport généré: {OUTPUT_PATH}")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
