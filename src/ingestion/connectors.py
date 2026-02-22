import pyodbc
from src.utils.logger import Logger
logger = Logger()

def get_connection(server: str, database: str):
    """
    Retourne une connexion pyodbc sur SQL Server pour le serveur et la base spécifiés.
    """
    conn_str = (
        f'DRIVER={{SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'Trusted_Connection=yes;'
    )
    try:
        conn = pyodbc.connect(conn_str)
        logger.info(
                step="CONNECTOR",
                message=f"✓ Connexion établie ({server}/{database})"
            )
        return conn
    except Exception as e:
            logger.error(
                step="CONNECTOR",
                message=f"Impossible de se connecter à {server}/{database}",
                exc=e
            )
    return None