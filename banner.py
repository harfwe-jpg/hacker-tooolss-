"""Banners y menús con arte ASCII."""
from colorama import Fore, Style
import pyfiglet
import random


def mostrar_banner():
    arte = pyfiglet.figlet_format("HACK TOOLKIT", font="slant")
    colores = [Fore.CYAN, Fore.GREEN, Fore.MAGENTA, Fore.YELLOW]
    color = random.choice(colores)
    print(color + arte + Style.RESET_ALL)
    print(
        f"{Fore.WHITE}   [ v4.1 - Ethical Hacking Framework ]{Style.RESET_ALL}")
    print(f"{Fore.RED}   ⚠  Solo para auditorías autorizadas{Style.RESET_ALL}\n")


def mostrar_menu_principal():
    opciones = [
        ("1", "🔐 Criptografía Avanzada (Fernet / AES / Hashes)"),
        ("2", "🌐 Reconocimiento de Red (Multihilo)"),
        ("3", "🔑 Auditoría de Contraseñas"),
        ("4", "🕷️ Análisis Web (Async)"),
        ("5", "🖼️ Esteganografía"),
        ("6", "🔍 OSINT (WHOIS / DNS)"),
        ("7", "💉 Fuzzing & Payloads"),
        ("8", "🛡️ Hardening Local"),
        ("9", "🚪 Salir"),
    ]
    for num, desc in opciones:
        print(f"  {Fore.CYAN}[{num}]{Style.RESET_ALL} {desc}")
