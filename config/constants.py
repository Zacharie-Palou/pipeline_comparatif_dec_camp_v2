import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(override=True)

# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BACKUPS = {
    "10-2024": {
        "server": os.environ.get("SERVER_1"),
        "database": os.environ.get("DB_10_2024")
    },
    "06-2025": {
        "server": os.environ.get("SERVER_2"),
        "database": os.environ.get("DB_06_2025")
    },
    "11-2025": {
        "server": os.environ.get("SERVER_2"),
        "database": os.environ.get("DB_11_2025")
    },
    "02-2026": {
        "server": os.environ.get("SERVER_2"),
        "database": os.environ.get("DB_02_2026")
    }
    # Ajouter d'autres années si nécessaire
}

DECLARATIONS = {
    "msm": {"table": "SYD_dec_ligne_msm"},
    "trt": {"table": "SYD_dec_ligne_trt"},
    "coll": {"table": "SYD_dec_ligne_coll"},
    "rrr": {"table": "SYD_dec_ligne_rrr"},
}

# ============================================================
# DATA UNITS
# ============================================================

UNITS = ["masse", "quantite"]

# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TEMP_DIR = DATA_DIR / "temp"
LOGS_DIR = PROJECT_ROOT / "logs"

# ============================================================
# DEMO MODE
# ============================================================

DEMO_MODE = os.environ.get("DEMO_MODE", "true")
if DEMO_MODE == "true":
    OUTPUT_DIR = DATA_DIR / "outputs_demo"
    DEMO_DIR = DATA_DIR / "data_demo"
else:
    OUTPUT_DIR = DATA_DIR / "outputs"
                                                     
# Créer les répertoires s'ils n'existent pas
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# EXCEL OUTPUT
# ============================================================

EXCEL_SHEETS = {
    "README": 0,           # Onglet 1: Documentation
    "DEC INIT": 1,             # Onglet 2: Données INIT
    "DEC CORR": 2,             # Onglet 3: Données CORR
    "STATS": 3,            # Onglet 4: Statistiques complètes
    "ANALYSE": 4,   # Onglet 5: Stats filtrées (>1% val absolue)
    "DASHBOARD": 5         # Onglet 6: TdB par filière
}

# ============================================================
# PROCESSING CONFIG
# ============================================================

EVOLUTION_THRESHOLD = 0.01  # 1% en valeur absolue pour filtrer
DECIMAL = 2          # Nombre de décimales pour les calculs

# ============================================================
# LOGGING CONFIG
# ============================================================

LOG_FORMAT = "[{step}] {message}"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"