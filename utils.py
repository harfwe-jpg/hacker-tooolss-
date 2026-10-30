"""Utilidades generales."""
import os
import time
from colorama import Fore, Style
from tqdm import tqdm


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def esperar_input():
    input(f"\n{Fore.YELLOW}[Enter] para continuar...{Style.RESET_ALL}")


def efecto_carga(mensaje, duracion=1.5):
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} {mensaje}")
    for _ in tqdm(range(100), desc="Procesando", bar_format="{l_bar}{bar}|", ncols=60):
        time.sleep(duracion / 100)
