"""
Gestión de configuración desde YAML y .env.
"""
import os
import yaml
from dotenv import load_dotenv


def load_config():
    """Carga configuración desde config.yaml y .env."""
    load_dotenv()

    config = {}
    config_file = "config.yaml"

    if os.path.exists(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                contenido = yaml.safe_load(f)
                config = contenido if contenido else {}
        except yaml.YAMLError as e:
            print(
                f"[!] Error en config.yaml: {e}. Usando configuración por defecto.")
            config = {}

    # Inyectar variables de entorno
    config["api_keys"] = {
        "virustotal": os.getenv("VIRUSTOTAL_API_KEY"),
        "shodan": os.getenv("SHODAN_API_KEY"),
        "abuseipdb": os.getenv("ABUSEIPDB_API_KEY"),
    }

    return config


def get_api_key(service, config):
    """Obtiene una API key específica."""
    return config.get("api_keys", {}).get(service)
