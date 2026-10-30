"""Módulo de Auditoría y Generación de Contraseñas."""
import secrets
import string
import math
import itertools
from colorama import Fore, Style
from tqdm import tqdm
from src.utils import limpiar_pantalla, esperar_input, efecto_carga


def generar_password_cli(length: int = 16) -> tuple:
    """Genera contraseña segura y calcula su entropía."""
    alfabeto = string.ascii_letters + string.digits + string.punctuation
    pwd = ''.join(secrets.choice(alfabeto) for _ in range(length))
    entropia = length * math.log2(len(alfabeto))
    return pwd, entropia


def analizar_entropia_cli(pwd: str) -> float:
    """Calcula la entropía de una contraseña dada."""
    pool_size = 0
    if any(c.islower() for c in pwd):
        pool_size += 26
    if any(c.isupper() for c in pwd):
        pool_size += 26
    if any(c.isdigit() for c in pwd):
        pool_size += 10
    if any(c in string.punctuation for c in pwd):
        pool_size += 32
    if pool_size == 0:
        pool_size = 26
    return len(pwd) * math.log2(pool_size)


def generar_password():
    try:
        longitud = int(input("Longitud (mín 8): "))
        longitud = max(8, longitud)
    except ValueError:
        longitud = 16
    chars = string.ascii_letters + string.digits + string.punctuation
    pwd = "".join(secrets.choice(chars) for _ in range(longitud))
    entropia = analizar_entropia_cli(pwd)
    print(f"\n{Fore.GREEN}[+] Contraseña:{Style.RESET_ALL} {pwd}")
    print(f"{Fore.CYAN}    Entropía: {entropia:.2f} bits{Style.RESET_ALL}")
    nivel = "Débil" if entropia < 50 else "Media" if entropia < 80 else "Fuerte"
    color = Fore.RED if entropia < 50 else Fore.YELLOW if entropia < 80 else Fore.GREEN
    print(f"    Fortaleza: {color}{nivel}{Style.RESET_ALL}")


def ataque_diccionario():
    objetivo = input("Contraseña a auditar: ").strip()
    diccionario = [
        "123456", "password", "admin", "root", "qwerty", "letmein",
        "welcome", "monkey", "dragon", "master", "123456789", "abc123",
    ]
    efecto_carga("Probando diccionario")
    for palabra in tqdm(diccionario, ncols=60):
        if palabra == objetivo:
            print(f"\n{Fore.RED}[!] CRACKED: {palabra}{Style.RESET_ALL}")
            return
    print(
        f"\n{Fore.GREEN}[✓] No está en el diccionario básico.{Style.RESET_ALL}")


def fuerza_bruta_limitada():
    print(
        f"{Fore.YELLOW}[!] Solo para longitudes ≤ 4 (demo educativa){Style.RESET_ALL}")
    objetivo = input("Password objetivo (máx 4 chars): ").strip()[:4]
    charset = string.ascii_lowercase + string.digits
    efecto_carga("Generando combinaciones")
    intentos = 0
    for largo in range(1, len(objetivo) + 1):
        for combo in itertools.product(charset, repeat=largo):
            intento = "".join(combo)
            intentos += 1
            if intento == objetivo:
                print(
                    f"\n{Fore.RED}[!] Encontrado: '{intento}' en {intentos} intentos{Style.RESET_ALL}")
                return
    print(
        f"\n{Fore.YELLOW}[-] No encontrado en el espacio de búsqueda.{Style.RESET_ALL}")


def ejecutar():
    """Modo interactivo del módulo."""
    while True:
        limpiar_pantalla()
        print(f"\n{Fore.MAGENTA}=== 🔑 AUDITORÍA DE CONTRASEÑAS ==={Style.RESET_ALL}")
        print("  [1] Generar contraseña segura")
        print("  [2] Analizar entropía de una contraseña")
        print("  [3] Ataque de diccionario")
        print("  [4] Fuerza bruta (limitada)")
        print("  [5] Volver")
        op = input("\n[>] Opción: ").strip()

        if op == "1":
            generar_password()
            esperar_input()
        elif op == "2":
            p = input("Contraseña a analizar: ")
            e = analizar_entropia_cli(p)
            print(f"{Fore.CYAN}Entropía: {e:.2f} bits{Style.RESET_ALL}")
            esperar_input()
        elif op == "3":
            ataque_diccionario()
            esperar_input()
        elif op == "4":
            fuerza_bruta_limitada()
            esperar_input()
        elif op == "5":
            break
