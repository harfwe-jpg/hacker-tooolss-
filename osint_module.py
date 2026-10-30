"""Módulo OSINT: WHOIS, DNS y reputación de dominios."""
import socket
from colorama import Fore, Style
import dns.resolver
from src.utils import limpiar_pantalla, esperar_input


def safe_str(val):
    """Convierte valores WHOIS (posibles listas de datetimes) a string seguro."""
    if val is None:
        return "N/A"
    if isinstance(val, list):
        if not val:
            return "N/A"
        return str(val[0])
    return str(val)


def consultar_dns(dominio):
    """Consulta registros DNS (A, AAAA, MX, NS, TXT)."""
    resultados = {"dominio": dominio, "registros": {}}
    tipos = ["A", "AAAA", "MX", "NS", "TXT"]

    for tipo in tipos:
        try:
            respuestas = dns.resolver.resolve(dominio, tipo)
            resultados["registros"][tipo] = [str(r) for r in respuestas]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.DNSException):
            resultados["registros"][tipo] = []

    return resultados


def consultar_whois(dominio):
    """Consulta WHOIS del dominio con manejo seguro de listas/fechas."""
    try:
        import whois
        w = whois.whois(dominio)

        return {
            "dominio": dominio,
            "registrar": safe_str(w.registrar),
            "creacion": safe_str(w.creation_date),
            "expiracion": safe_str(w.expiration_date),
            "nameservers": w.name_servers or [],
            "estado": safe_str(w.status),
        }
    except Exception as e:
        return {"dominio": dominio, "error": str(e)}


def mostrar_resultados_osint(resultado):
    """Muestra resultados OSINT formateados."""
    print(
        f"\n{Fore.CYAN}=== OSINT: {resultado.get('dominio', 'N/A')} ==={Style.RESET_ALL}")

    if "registros" in resultado:
        print(f"\n{Fore.GREEN}Registros DNS:{Style.RESET_ALL}")
        for tipo, valores in resultado["registros"].items():
            if valores:
                print(f"  [{tipo}]")
                for v in valores:
                    print(f"    • {v}")

    if "registrar" in resultado:
        print(f"\n{Fore.GREEN}WHOIS:{Style.RESET_ALL}")
        print(f"  Registrar: {resultado.get('registrar')}")
        print(f"  Creación: {resultado.get('creacion')}")
        print(f"  Expiración: {resultado.get('expiracion')}")
        if resultado.get("nameservers"):
            print(f"  Nameservers:")
            for ns in resultado["nameservers"]:
                print(f"    • {ns}")

    if "error" in resultado:
        print(f"{Fore.RED}Error: {resultado['error']}{Style.RESET_ALL}")


def ejecutar_cli(dominio, solo_dns=False, solo_whois=False):
    resultado = {"dominio": dominio}
    if solo_dns or (not solo_dns and not solo_whois):
        resultado.update(consultar_dns(dominio))
    if solo_whois or (not solo_dns and not solo_whois):
        resultado.update(consultar_whois(dominio))
    return resultado


def ejecutar():
    while True:
        limpiar_pantalla()
        print(
            f"\n{Fore.MAGENTA}=== 🔍 OSINT (Inteligencia de Fuentes Abiertas) ==={Style.RESET_ALL}")
        print("  [1] Consulta DNS completa")
        print("  [2] Consulta WHOIS")
        print("  [3] Análisis completo (DNS + WHOIS)")
        print("  [4] Volver")
        op = input("\n[>] Opción: ").strip()

        if op in ("1", "2", "3"):
            dominio = input("Dominio objetivo (ej: ejemplo.com): ").strip()
            if op == "1":
                resultado = consultar_dns(dominio)
            elif op == "2":
                resultado = consultar_whois(dominio)
            else:
                dns_res = consultar_dns(dominio)
                whois_res = consultar_whois(dominio)
                resultado = {**dns_res, **whois_res}
            mostrar_resultados_osint(resultado)
            esperar_input()
        elif op == "4":
            break
