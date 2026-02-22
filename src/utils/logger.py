from datetime import datetime
from pathlib import Path
from config.constants import LOGS_DIR, LOG_FORMAT, LOG_DATE_FORMAT


class Logger:
    """Logging structuré avec formatage uniforme"""
    
    def __init__(self, log_file: str = None):
        self.log_file = log_file or LOGS_DIR / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)
    
    def _format_message(self, step: str, message: str, exc: Exception = None) -> str:
        """Formate un message de log"""
        timestamp = datetime.now().strftime(LOG_DATE_FORMAT)
        msg = f"[{timestamp}] {LOG_FORMAT.format(step=step, message=message)}"
        if exc:
            msg += f"\n  Exception: {type(exc).__name__}: {str(exc)}"
        return msg
    
    def info(self, step: str, message: str):
        """Log info"""
        msg = self._format_message(step, message)
        print(msg)
        self._write_to_file(msg)
    
    def warning(self, step: str, message: str):
        """Log warning"""
        msg = self._format_message(step, f"⚠️  {message}")
        print(msg)
        self._write_to_file(msg)
    
    def error(self, step: str, message: str, exc: Exception = None):
        """Log error"""
        msg = self._format_message(step, f"❌ {message}", exc)
        print(msg)
        self._write_to_file(msg)
    
    def _write_to_file(self, message: str):
        """Écrit dans le fichier log"""
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except Exception as e:
            print(f"[ERROR] Impossible d'écrire dans le log: {e}")