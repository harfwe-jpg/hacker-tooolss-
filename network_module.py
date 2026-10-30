"""Reconocimiento de red con escáner multihilo."""
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style
import requests
from tqdm import tqdm
from core.logger import setup_logger
from core.config import load_config
from core.reporter import ReportGenerator
from src.utils import limpiar_pantalla, esperar_input


logger = setup_logger(load_config())


def escanear_puerto(ip, puerto, timeout=1):
    """Escanea un puerto individual (función para hilos)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            resultado = s.connect_ex((ip, puerto))
            if resultado == 0:
                try:
                    servicio = socket.getservbyport(puerto, "tcp")
                except OSError:
                    servicio = "unknown"
                return {"puerto": puerto, "estado": "ABIERTO", "servicio": servicio}
    except Exception:
        pass
    return None


def parsear_puertos(puertos_str):
    """Parsea string de puertos: '80,443,1-100' de forma segura."""
    puertos = set()
    for parte in puertos_str.split(","):
        parte = parte.strip()
        if not parte:
            continue
        if "-" in parte:
            partes_rango = parte.split("-", 1)
            try:
                inicio, fin = int(partes_rango[0]), int(partes_rango[1])
                if inicio > fin:
                    inicio, fin = fin, inicio
                puertos.update(range(inicio, fin + 1))
            except ValueError:
                continue
        else:
            try:
                puertos.add(int(parte))
            except ValueError:
                continue
    return sorted(puertos)


def escanear_puertos_multihilo(objetivo, puertos_str="80,443,22,21,3306", max_threads=100):
    """Escáner de puertos concurrente con ThreadPoolExecutor."""
    try:
        ip = socket.gethostbyname(objetivo)
    except socket.gaierror:
        logger.error(f"No se pudo resolver: {objetivo}")
        return None

    puertos = parsear_puertos(puertos_str)
    if not puertos:
        print(
            f"{Fore.RED}[✗] No se pudieron parsear los puertos.{Style.RESET_ALL}")
        return None

    logger.info(
        f"Escaneando {ip} - {len(puertos)} puertos con {max_threads} hilos")

    abiertos = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(escanear_puerto, ip, p): p for p in puertos}

        with tqdm(total=len(puertos), desc="Escaneando", ncols=70) as pbar:
            for future in as_completed(futures):
                resultado = future.result()
                if resultado:
                    abiertos.append(resultado)
                    print(
                        f"  {Fore.GREEN}[+] {resultado['puerto']}/tcp ABIERTO ({resultado['servicio']}){Style.RESET_ALL}")
                pbar.update(1)

    return {
        "target": objetivo,
        "ip": ip,
        "puertos_abiertos": abiertos,
        "total_escaneados": len(puertos),
    }


def escanear_puertos_cli(target, ports, threads):
    return escanear_puertos_multihilo(target, ports, threads)


def mostrar_resultados(resultado):
    if not resultado:
        return
    print(f"\n{Fore.CYAN}=== RESULTADO DEL ESCANEO ==={Style.RESET_ALL}")
    print(f"Objetivo: {resultado['target']} ({resultado['ip']})")
    print(f"Puertos escaneados: {resultado['total_escaneados']}")
    print(f"Puertos abiertos: {len(resultado['puertos_abiertos'])}")
    for p in resultado["puertos_abiertos"]:
        print(f"  [+] {p['puerto']}/tcp - {p['servicio']}")


def escanear_interactivo():
    objetivo = input("IP/Dominio objetivo: ").strip()
    puertos = input("Puertos (ej: 80,443,1-100) [default: comunes]: ").strip()
    if not puertos:
        puertos = "21,22,23,25,53,80,110,143,443,445,3306,3389,5432,8080,8443"
    try:
        threads = int(input("Hilos concurrentes [100]: ").strip() or "100")
    except ValueError:
        threads = 100

    resultado = escanear_puertos_multihilo(objetivo, puertos, threads)

    if resultado:
        guardar = input("\n¿Guardar reporte? (s/n): ").strip().lower()
        if guardar == "s":
            reporter = ReportGenerator()
            paths = reporter.generar_reporte_escaneo(
                objetivo, resultado["puertos_abiertos"], resultado["total_escaneados"]
            )
            print(f"\n{Fore.GREEN}[✓] Reportes generados:{Style.RESET_ALL}")
            print(f"    JSON: {paths['json']}")
            print(f"    HTML: {paths['html']}")


def analizar_headers_http():
    url = input("URL objetivo (https://ejemplo.com): ").strip()
    if not url.startswith("http"):
        url = "https://" + url
    try:
        r = requests.get(url, timeout=5, allow_redirects=True)
        print(f"\n{Fore.CYAN}Status: {r.status_code}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Server: {r.headers.get('Server', 'N/A')}{Style.RESET_ALL}")
        seguridad = {
            "Strict-Transport-Security": "HSTS",
            "X-Frame-Options": "Clickjacking Protection",
            "X-Content-Type-Options": "MIME Sniffing Protection",
            "Content-Security-Policy": "CSP",
        }
        print(f"\n{Fore.GREEN}Cabeceras de seguridad:{Style.RESET_ALL}")
        for h, desc in seguridad.items():
            val = r.headers.get(h)
            estado = f"{Fore.GREEN}✓ {val}" if val else f"{Fore.RED}✗ Ausente"
            print(f"  {desc}: {estado}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[✗] Error: {e}{Style.RESET_ALL}")


def ejecutar():
    while True:
        limpiar_pantalla()
        print(
            f"\n{Fore.MAGENTA}=== 🌐 RECONOCIMIENTO DE RED (Multihilo) ==={Style.RESET_ALL}")
        print("  [1] Escáner de puertos TCP (concurrente)")
        print("  [2] Análisis de cabeceras HTTP")
        print("  [3] Volver")
        op = input("\n[>] Opción: ").strip()
        if op == "1":
            escanear_interactivo()
            esperar_input()
        elif op == "2":
            analizar_headers_http()
            esperar_input()
        elif op == "3":
            break
