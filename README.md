# Pipeline Comparatif Déclarations de Campagne

Pipeline Python automatisant la comparaison entre déclarations initiales et correctives dans le cadre du suivi des filières REP (Responsabilité Élargie du Producteur), développé pour le compte de l'ADEME / Ministère de la Transition Écologique.

---

## Contexte

Les producteurs soumis à la réglementation REP déposent chaque année des déclarations de tonnages et quantités mis sur le marché. Ces déclarations passent par deux étapes : une déclaration **initiale**, puis une déclaration **corrective** intégrant les ajustements.

Ce pipeline compare automatiquement ces deux campagnes, calcule les écarts et taux d'évolution par filière, type de déclaration, déclarant et code, puis génère un rapport Excel multi-onglets prêt à l'emploi pour les équipes métier.

---

## Fonctionnalités

- Extraction SQL multi-bases (deux serveurs, deux périodes)
- Standardisation et mapping automatique des référentiels (gestion des renommages de filières entre campagnes)
- Calcul des écarts et taux d'évolution ligne par ligne
- Export Excel multi-onglets avec mise à jour **in place** (préserve les formats et mises en forme métier)
- Dashboard pivot : taux d'évolution global par filière × code
- Mode DEMO intégré : tourne sans accès aux serveurs SQL, avec données fictives

---

## Architecture

```
automat_diff_dec_v2/
│
├── main.py                         # Point d'entrée — 3 variables à renseigner
│
├── config/
│   ├── constants.py                # Chemins, connexions, mode DEMO
│   └── mappings.py                 # Règles métier (filières, types, mesures)
│
├── data/
│   └── data_demo/                  # CSV fictifs pour le mode DEMO
│
├── src/
│   ├── ingestion/
│   │   ├── connectors.py           # Connexions SQL Server
│   │   └── extractors.py          # Extraction des déclarations
│   │
│   ├── transformation/
│   │   ├── standardizers.py       # Normalisation des colonnes
│   │   └── transformers.py        # Application des mappings métier
│   │
│   ├── processing/
│   │   ├── mergers.py             # Fusion INIT vs CORR
│   │   ├── calculators.py         # Calcul écarts et taux d'évolution
│   │   ├── filters.py             # Filtrage par seuil
│   │   └── aggregators.py        # Agrégation dashboard
│   │
│   ├── output/
│   │   └── excel_writer.py        # Export Excel multi-onglets
│   │
│   └── utils/
│       ├── logger.py              # Logger horodaté
│       └── helpers.py             # Utilitaires (nommage fichiers...)
│
├── .env.example                   # Template configuration
├── requirements.txt
└── README.md
```

**4 couches distinctes :** Ingestion → Transformation → Processing → Output. Chaque module a une responsabilité unique, aucune logique métier dans le pipeline d'orchestration.

---

## Installation

```bash
git clone https://github.com/Zacharie-Palou/pipeline_comparatif_dec_camp_v2.git
cd pipeline_comparatif_dec_camp_v2
pip install -r requirements.txt
cp .env.example .env
```

Le fichier `.env` est pré-configuré en mode DEMO (`DEMO_MODE=true`) — aucun accès SQL requis.

---

## Utilisation

Ouvrir `main.py` et renseigner les 3 variables :

```python
DEC_INIT    = "10-2024"   # Déclaration initiale  (format MM-YYYY)
DEC_CORR    = "06-2025"   # Déclaration corrective (format MM-YYYY)
TARGET_YEAR = 2023        # Année de campagne cible
```

Puis lancer :

```bash
python main.py
```

Le rapport Excel est généré dans `data/outputs/` avec le nommage automatique :
`DEC_CIBLE-2023__BACKUPS-10-2024_06-2025.xlsx`

Le rapport Excel en mode DEMO est généré dans 'data/outputs_demo/' avec le nommage : 
'rapport_demo'

---

## Rapport Excel généré

| Onglet | Contenu |
|--------|---------|
| `INIT` | Déclarations initiales standardisées |
| `CORR` | Déclarations correctives standardisées |
| `STATS` | Comparaison ligne par ligne avec écart et taux d'évolution |
| `DASHBOARD` | Taux d'évolution global par filière × code (vue pivot) |

Le fichier supporte la **mise à jour in place** : relancer le pipeline sur un fichier existant met à jour les données sans écraser les formats, couleurs ou annotations ajoutés manuellement par les équipes métier.

---

## Mode DEMO

Le mode DEMO permet de faire tourner le pipeline sans accès aux serveurs SQL internes.

```env
# .env
DEMO_MODE=true
```

Les données sont chargées depuis `data/data_demo/` — 8 fichiers CSV couvrant 4 types de déclarations (MSM, Traitement, Collecte, RR) en version initiale et corrective, avec des écarts volontairement significatifs pour illustrer les fonctionnalités de détection.

---

## Configuration avancée

```env
# .env — mode production
DEMO_MODE=false

SERVER_1=<serveur_init>
DB_10_2024=<base_init>

SERVER_2=<serveur_corr>
DB_06_2025=<base_corr>
```

---

## Stack technique

- **Python 3.11**
- **pandas** — manipulation et transformation des données
- **pyodbc / SQLAlchemy** — connexions SQL Server
- **openpyxl** — génération et mise à jour Excel
- **python-dotenv** — gestion des variables d'environnement

---

## Contexte de développement

Ce pipeline est une refactorisation complète d'une V1 développée en "god function" (~400 lignes dans un seul script). La V2 introduit une architecture modulaire en couches, la séparation des règles métier dans des modules dédiés, un mode DEMO pour la portabilité, et un système de mise à jour in place du rapport Excel.

---

*Développé dans le cadre d'une mission Data à l'ADEME — Agence de la Transition Écologique.*