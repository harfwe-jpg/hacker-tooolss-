"""Módulo de criptografía con librería 'cryptography' y hashlib."""
import hashlib
from colorama import Fore, Style
from cryptography.fernet import Fernet
import pyperclip
from src.utils import limpiar_pantalla, esperar_input


def generar_hash_cli(texto: str, algo: str) -> str:
    """Genera hash para la CLI."""
    texto_bytes = texto.encode('utf-8')
    algoritmos = {
        "md5": hashlib.md5,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
        "blake2b": hashlib.blake2b,
    }
    if algo not in algoritmos:
        return "Algoritmo no soportado"
    return algoritmos[algo](texto_bytes).hexdigest()


def generar_clave_fernet():
    """Genera una clave Fernet (AES-128-CBC + HMAC) segura."""
    clave = Fernet.generate_key()
    print(f"\n{Fore.GREEN}[+] Clave generada (¡guárdala!):{Style.RESET_ALL}")
    print(f"    {clave.decode()}")
    try:
        pyperclip.copy(clave.decode())
        print(f"{Fore.CYAN}    (Copiada al portapapeles){Style.RESET_ALL}")
    except Exception:
        pass
    return clave


def cifrar_mensaje():
    texto = input("Mensaje a cifrar: ")
    clave = input("Pega tu clave Fernet (o Enter para generar una): ").strip()
    if not clave:
        clave = generar_clave_fernet().decode()
    try:
        f = Fernet(clave.encode())
        cifrado = f.encrypt(texto.encode()).decode()
        print(f"\n{Fore.GREEN}[+] Cifrado:{Style.RESET_ALL}\n    {cifrado}")
        print(f"{Fore.CYAN}    Clave: {clave}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[✗] Error: {e}{Style.RESET_ALL}")


def descifrar_mensaje():
    cifrado = input("Mensaje cifrado: ")
    clave = input("Clave Fernet: ").strip()
    try:
        f = Fernet(clave.encode())
        original = f.decrypt(cifrado.encode()).decode()
        print(
            f"\n{Fore.GREEN}[+] Descifrado:{Style.RESET_ALL}\n    {original}")
    except Exception:
        print(
            f"{Fore.RED}[✗] Clave incorrecta o mensaje corrupto.{Style.RESET_ALL}")


def generar_hash_interactivo():
    texto = input("Texto a hashear: ")
    print("  [1] SHA-256  [2] SHA-512  [3] MD5  [4] Blake2b")
    op = input("Algoritmo: ").strip()
    alg = {"1": "sha256", "2": "sha512", "3": "md5", "4": "blake2b"}.get(op)
    if not alg:
        print(f"{Fore.RED}[✗] Opción inválida{Style.RESET_ALL}")
        return
    resultado = generar_hash_cli(texto, alg)
    print(f"\n{Fore.GREEN}[+] Hash ({alg}):{Style.RESET_ALL}\n    {resultado}")


def ejecutar():
    """Modo interactivo del módulo."""
    while True:
        limpiar_pantalla()
        print(f"\n{Fore.MAGENTA}=== 🔐 CRIPTOGRAFÍA AVANZADA ==={Style.RESET_ALL}")
        print("  [1] Generar clave Fernet")
        print("  [2] Cifrar mensaje")
        print("  [3] Descifrar mensaje")
        print("  [4] Generar Hash (MD5, SHA256, SHA512, Blake2b)")
        print("  [5] Volver")
        op = input("\n[>] Opción: ").strip()

        if op == "1":
            generar_clave_fernet()
            esperar_input()
        elif op == "2":
            cifrar_mensaje()
            esperar_input()
        elif op == "3":
            descifrar_mensaje()
            esperar_input()
        elif op == "4":
            generar_hash_interactivo()
            esperar_input()
        elif op == "5":
            break
