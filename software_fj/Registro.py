"""Configuración del archivo de logs (errores y eventos relevantes)."""
import logging
import os

RUTA_LOG = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "software_fj.log")


def obtener_logger() -> logging.Logger:
    """Devuelve el logger del sistema, creándolo una sola vez."""
    logger = logging.getLogger("software_fj")
    if not logger.handlers:  # evita duplicar manejadores
        os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)
        logger.setLevel(logging.INFO)
        manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")
        manejador.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
        )
        logger.addHandler(manejador)
    return logger
