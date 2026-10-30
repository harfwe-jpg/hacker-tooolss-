"""Sistema de logging profesional con timestamps y niveles."""
import logging
import os
from colorama import Fore, Style


class ColorFormatter(logging.Formatter):
    """Formateador con colores para la terminal."""
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, Fore.WHITE)
        record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)


def setup_logger(config):
    """Configura el logger con archivo y consola."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "toolkit.log")
    log_level_name = config.get("general", {}).get("log_level", "INFO")
    log_level = getattr(logging, log_level_name, logging.INFO)

    logger = logging.getLogger("EthicalToolkit")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # Handler para archivo (sin colores)
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(fh)

    # Handler para consola (con colores)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(ColorFormatter("%(levelname)s | %(message)s"))
    logger.addHandler(ch)

    logger.info(f"Logger inicializado - Archivo: {log_file}")
    return logger
