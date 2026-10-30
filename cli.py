#!/usr/bin/env python3
"""
CLI del Toolkit - Modo comandos directos
Ejemplos:
  python cli.py scan --target 192.168.1.1 --ports 80,443
  python cli.py hash --text "hola" --algo sha256
  python cli.py osint --domain ejemplo.com
  python cli.py password --generate --length 20
  python cli.py web --url https://ejemplo.com --headers
"""
import argparse
import sys
from colorama import init, Fore, Style
from core.logger import setup_logger
from core.config import load_config
from core.reporter import ReportGenerator
from src import (
    crypto_module, network_module, password_module,
    web_module, osint_module,
)

init(autoreset=True)


def crear_parser():
    parser = argparse.ArgumentParser(
        description="🛡️ Ethical Hacking Toolkit v4.1 - CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(
        dest="comando", help="Comandos disponibles")

    # === SCAN ===
    p_scan = subparsers.add_parser("scan", help="Escáner de puertos multihilo")
    p_scan.add_argument("--target", "-t", required=True, help="IP o dominio")
    p_scan.add_argument("--ports", "-p", default="80,443,22",
                        help="Puertos (ej: 80,443,1-100)")
    p_scan.add_argument("--threads", type=int, default=100,
                        help="Hilos concurrentes")
    p_scan.add_argument("--output", "-o", help="Guardar reporte JSON")

    # === HASH ===
    p_hash = subparsers.add_parser("hash", help="Generar hash")
    p_hash.add_argument("--text", required=True, help="Texto a hashear")
    p_hash.add_argument("--algo", default="sha256",
                        choices=["sha256", "sha512", "md5", "blake2b"])

    # === OSINT ===
    p_osint = subparsers.add_parser(
        "osint", help="Inteligencia de fuentes abiertas")
    p_osint.add_argument("--domain", "-d", help="Dominio a investigar")
    p_osint.add_argument("--dns", action="store_true",
                         help="Solo consultas DNS")
    p_osint.add_argument("--whois", action="store_true", help="Solo WHOIS")

    # === PASSWORD ===
    p_pwd = subparsers.add_parser("password", help="Auditoría de contraseñas")
    p_pwd.add_argument("--generate", "-g", action="store_true",
                         help="Generar contraseña")
    p_pwd.add_argument("--length", "-l", type=int, default=16, help="Longitud")
    p_pwd.add_argument(
        "--check", "-c", help="Analizar entropía de una contraseña")

    # === WEB ===
    p_web = subparsers.add_parser("web", help="Análisis web asíncrono")
    p_web.add_argument("--url", "-u", required=True, help="URL objetivo")
    p_web.add_argument("--headers", action="store_true",
                         help="Analizar headers de seguridad")
    p_web.add_argument("--tech", action="store_true",
                         help="Detectar tecnologías")
    p_web.add_argument("--links", action="store_true", help="Extraer enlaces")

    return parser


def cmd_scan(args, config, logger):
    logger.info(f"CLI scan: target={args.target}")
    resultado = network_module.escanear_puertos_cli(
        args.target, args.ports, args.threads)
    if args.output and resultado:
        reporter = ReportGenerator()
        reporter.save_json(resultado, args.output)
        print(f"[✓] Reporte guardado: {args.output}")
    elif resultado:
        network_module.mostrar_resultados(resultado)


def cmd_hash(args, config, logger):
    logger.info(f"CLI hash: algo={args.algo}")
    resultado = crypto_module.generar_hash_cli(args.text, args.algo)
    print(f"[+] Hash ({args.algo}): {resultado}")


def cmd_osint(args, config, logger):
    if not args.domain:
        print(f"{Fore.RED}[✗] Debes especificar --domain{Style.RESET_ALL}")
        return
    logger.info(f"CLI osint: domain={args.domain}")
    resultado = osint_module.ejecutar_cli(args.domain, args.dns, args.whois)
    osint_module.mostrar_resultados_osint(resultado)


def cmd_password(args, config, logger):
    if args.generate:
        pwd, entropia = password_module.generar_password_cli(args.length)
        print(f"[+] Contraseña: {pwd}")
        print(f"[+] Entropía: {entropia:.2f} bits")
    elif args.check:
        entropia = password_module.analizar_entropia_cli(args.check)
        print(f"[+] Entropía de '{args.check}': {entropia:.2f} bits")
    else:
        print(f"{Fore.YELLOW}[!] Usa --generate o --check{Style.RESET_ALL}")


def cmd_web(args, config, logger):
    logger.info(f"CLI web: url={args.url}")
    if args.headers:
        resultado = web_module.analizar_headers_cli(args.url)
        web_module.mostrar_headers(resultado)
    elif args.tech:
        resultado = web_module.detectar_tecnologias_cli(args.url)
        web_module.mostrar_tecnologias(resultado)
    elif args.links:
        resultado = web_module.extraer_links_cli(args.url)
        web_module.mostrar_links(resultado)
    else:
        print(
            f"{Fore.YELLOW}[!] Usa --headers, --tech o --links{Style.RESET_ALL}")


def main():
    parser = crear_parser()
    args = parser.parse_args()

    if not args.comando:
        parser.print_help()
        sys.exit(1)

    config = load_config()
    logger = setup_logger(config)

    comandos = {
        "scan": cmd_scan,
        "hash": cmd_hash,
        "osint": cmd_osint,
        "password": cmd_password,
        "web": cmd_web,
    }

    try:
        comandos[args.comando](args, config, logger)
    except KeyboardInterrupt:
        print(
            f"\n{Fore.YELLOW}[!] Ejecución interrumpida por el usuario.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error en CLI: {e}")
        print(f"{Fore.RED}[✗] Error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
