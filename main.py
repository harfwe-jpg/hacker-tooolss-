
from src import (
    crypto_module, network_module, password_module,
    web_module, stego_module, osint_module,
    fuzzing_module, hardening_module,
)
from src.utils import limpiar_pantalla, esperar_input
from src.banner import mostrar_banner, mostrar_menu_principal
from core.config import load_config
from core.logger import setup_logger
from colorama import init
import sys

# 🎯 `main.py`

#!/usr/bin/env python3
"""
Ethical Hacking Toolkit v4.1 - Modo Interactivo
"""

init(autoreset=True)


def main():
    """Bucle principal interactivo."""
    config = load_config()
    logger = setup_logger(config)
    logger.info("=== Toolkit iniciado en modo interactivo ===")

    while True:
        limpiar_pantalla()
        mostrar_banner()
        mostrar_menu_principal()

        opcion = input("\n[>] Opción (1-9): ").strip()

        modulos = {
            "1": ("🔐 Criptografía", crypto_module),
            "2": ("🌐 Redes (Multihilo)", network_module),
            "3": ("🔑 Contraseñas", password_module),
            "4": ("🕷️ Análisis Web (Async)", web_module),
            "5": ("🖼️ Esteganografía", stego_module),
            "6": ("🔍 OSINT", osint_module),
            "7": ("💉 Fuzzing & Payloads", fuzzing_module),
            "8": ("🛡️ Hardening Local", hardening_module),
        }

        if opcion in modulos:
            nombre, modulo = modulos[opcion]
            logger.info(f"Ejecutando módulo: {nombre}")
            modulo.ejecutar()
        elif opcion == "9":
            logger.info("Sesión finalizada por el usuario")
            print("\n[✓] Sesión cerrada. ¡Hackea responsablemente!")
            sys.exit(0)
        else:
            print("[✗] Opción inválida.")
            esperar_input()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrumpido por el usuario.")
        sys.exit(0)
