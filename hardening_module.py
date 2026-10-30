"""Auditoría de hardening del sistema local."""
import os
import platform
import subprocess
from colorama import Fore, Style
from src.utils import limpiar_pantalla, esperar_input


def auditar_sistema():
    """Realiza auditoría básica del sistema local."""
    resultados = []
    sistema = platform.system()

    print(
        f"\n{Fore.CYAN}[*] Auditando sistema: {sistema} {platform.release()}{Style.RESET_ALL}\n")

    # 1. Verificar usuario actual
    usuario = os.getenv("USER") or os.getenv("USERNAME")
    es_root = False
    if sistema != "Windows":
        es_root = os.geteuid() == 0
    resultados.append({
        "check": "Usuario actual",
        "valor": f"{usuario} ({'ROOT' if es_root else 'normal'})",
        "estado": "WARN" if es_root else "OK",
    })

    # 2. Verificar permisos de archivos críticos (Linux)
    if sistema == "Linux":
        archivos_criticos = ["/etc/passwd",
                             "/etc/shadow", "/etc/ssh/sshd_config"]
        for archivo in archivos_criticos:
            if os.path.exists(archivo):
                try:
                    stat = os.stat(archivo)
                    permisos = oct(stat.st_mode)[-3:]
                    estado = "OK" if permisos in (
                        "644", "640", "600", "400") else "WARN"
                    resultados.append({
                        "check": f"Permisos {archivo}",
                        "valor": permisos,
                        "estado": estado,
                    })
                except Exception as e:
                    resultados.append({
                        "check": f"Permisos {archivo}",
                        "valor": str(e),
                        "estado": "ERROR",
                    })

    # 3. Verificar servicios escuchando (Linux)
    if sistema == "Linux":
        try:
            output = subprocess.check_output(
                ["ss", "-tulpn"], stderr=subprocess.DEVNULL, text=True
            )
            lineas = output.strip().split("\n")[1:]
            resultados.append({
                "check": "Servicios escuchando",
                "valor": f"{len(lineas)} sockets activos",
                "estado": "INFO",
            })
        except Exception:
            resultados.append({
                "check": "Servicios escuchando",
                "valor": "No se pudo verificar (ss no disponible)",
                "estado": "INFO",
            })

    # 4. Verificar variables de entorno sensibles
    sensibles = ["PASSWORD", "SECRET", "API_KEY", "TOKEN"]
    encontradas = [k for k in os.environ if any(
        s in k.upper() for s in sensibles)]
    resultados.append({
        "check": "Variables de entorno sensibles",
        "valor": f"{len(encontradas)} encontradas",
        "estado": "WARN" if encontradas else "OK",
    })

    # 5. Verificar firewall (Linux)
    if sistema == "Linux":
        try:
            subprocess.check_output(
                ["iptables", "-L"], stderr=subprocess.DEVNULL)
            resultados.append({
                "check": "Firewall (iptables)",
                "valor": "Activo",
                "estado": "OK",
            })
        except Exception:
            resultados.append({
                "check": "Firewall (iptables)",
                "valor": "No activo o sin permisos",
                "estado": "WARN",
            })

    return resultados


def mostrar_auditoria(resultados):
    """Muestra resultados de auditoría."""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  RESULTADOS DE AUDITORÍA DE HARDENING{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

    for r in resultados:
        color = {
            "OK": Fore.GREEN,
            "WARN": Fore.YELLOW,
            "ERROR": Fore.RED,
            "INFO": Fore.CYAN,
        }.get(r["estado"], Fore.WHITE)

        print(
            f"  {color}[{r['estado']:5}]{Style.RESET_ALL} {r['check']}: {r['valor']}")

    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

    warns = sum(1 for r in resultados if r["estado"] == "WARN")
    errors = sum(1 for r in resultados if r["estado"] == "ERROR")
    oks = sum(1 for r in resultados if r["estado"] == "OK")
    print(f"\n  Resumen: {Fore.GREEN}{oks} OK{Style.RESET_ALL}, "
          f"{Fore.YELLOW}{warns} WARN{Style.RESET_ALL}, "
          f"{Fore.RED}{errors} ERROR{Style.RESET_ALL}")


def ejecutar():
    while True:
        limpiar_pantalla()
        print(
            f"\n{Fore.MAGENTA}=== 🛡️ AUDITORÍA DE HARDENING LOCAL ==={Style.RESET_ALL}")
        print("  [1] Ejecutar auditoría completa")
        print("  [2] Ver recomendaciones de hardening")
        print("  [3] Volver")
        op = input("\n[>] Opción: ").strip()

        if op == "1":
            resultados = auditar_sistema()
            mostrar_auditoria(resultados)
            esperar_input()

        elif op == "2":
            print(
                f"\n{Fore.GREEN}=== RECOMENDACIONES DE HARDENING ==={Style.RESET_ALL}")
            recomendaciones = [
                "Mantén el sistema actualizado (apt upgrade / yum update).",
                "Usa contraseñas fuertes y autenticación de dos factores.",
                "Deshabilita servicios innecesarios.",
                "Configura firewall con política por defecto DENY.",
                "Revisa logs regularmente (/var/log/auth.log, syslog).",
                "Usa SSH con claves, deshabilita root login y password auth.",
                "Implementa backups automáticos y cifrados.",
                "Usa herramientas como Lynis o OpenSCAP para auditorías profundas.",
            ]
            for i, r in enumerate(recomendaciones, 1):
                print(f"  {i}. {r}")
            esperar_input()

        elif op == "3":
            break
