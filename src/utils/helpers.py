#Création nom fichier automatique en fonction des backups

def build_report_filename(target_year: int, backups: list[str]) -> str:
    """Construit un nom de fichier automatique à partir de l'année cible et des backups"""
    backups_part = "_".join(sorted(backups))
    return f"DEC_CIBLE-{target_year}__BACKUPS-{backups_part}.xlsx"