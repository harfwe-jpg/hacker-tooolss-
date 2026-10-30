"""Análisis web asíncrono con httpx."""
import asyncio
import httpx
from bs4 import BeautifulSoup
from colorama import Fore, Style
from src.utils import limpiar_pantalla, esperar_input


async def fetch_url(client, url):
    """Petición HTTP asíncrona."""
    try:
        r = await client.get(url, timeout=10, follow_redirects=True)
        return url, r, None
    except Exception as e:
        return url, None, str(e)


async def buscar_subdirectorios_async(url, wordlist=None):
    """Búsqueda asíncrona de subdirectorios (dirbusting)."""
    if not wordlist:
        wordlist = ["admin", "login", "api", "uploads", "backup",
                    "config", "test", "dev", "dashboard", "panel"]

    base = url.rstrip("/")
    urls = [f"{base}/{w}" for w in wordlist]

    async with httpx.AsyncClient(headers={"User-Agent": "EthicalToolkit/4.1"}) as client:
        tasks = [fetch_url(client, u) for u in urls]
        resultados = []
        for task in asyncio.as_completed(tasks):
            url, r, err = await task
            if r and r.status_code in (200, 301, 302, 403):
                resultados.append(
                    {"url": url, "status": r.status_code, "size": len(r.content)})
                color = Fore.GREEN if r.status_code == 200 else Fore.YELLOW
                print(
                    f"  {color}[{r.status_code}] {url} ({len(r.content)} bytes){Style.RESET_ALL}")
        return resultados


def buscar_subdirectorios(url):
    """Wrapper síncrono para el modo interactivo."""
    print(
        f"\n{Fore.CYAN}[*] Buscando subdirectorios en {url}...{Style.RESET_ALL}")
    return asyncio.run(buscar_subdirectorios_async(url))


def extraer_links(url):
    try:
        r = httpx.get(url, timeout=10, follow_redirects=True)
        soup = BeautifulSoup(r.text, "html.parser")
        links = set()
        for a in soup.find_all("a", href=True):
            links.add(a["href"])
        print(
            f"\n{Fore.GREEN}[+] {len(links)} enlaces encontrados:{Style.RESET_ALL}")
        for l in sorted(links)[:30]:
            print(f"    {l}")
        return list(links)
    except Exception as e:
        print(f"{Fore.RED}[✗] {e}{Style.RESET_ALL}")
        return []


def detectar_tecnologias(url):
    try:
        r = httpx.get(url, timeout=10, headers={
                      "User-Agent": "Mozilla/5.0"}, follow_redirects=True)
        soup = BeautifulSoup(r.text, "html.parser")
        techs = set()
        meta = soup.find("meta", attrs={"name": "generator"})
        if meta:
            techs.add(f"CMS: {meta.get('content')}")
        for s in soup.find_all("script", src=True):
            src = s["src"].lower()
            if "jquery" in src:
                techs.add("jQuery")
            if "react" in src:
                techs.add("React")
            if "vue" in src:
                techs.add("Vue.js")
            if "bootstrap" in src:
                techs.add("Bootstrap")
            if "angular" in src:
                techs.add("Angular")
        server = r.headers.get("Server", "")
        if server:
            techs.add(f"Server: {server}")
        powered = r.headers.get("X-Powered-By", "")
        if powered:
            techs.add(f"Powered-By: {powered}")

        print(f"\n{Fore.GREEN}[+] Tecnologías detectadas:{Style.RESET_ALL}")
        for t in techs or ["Ninguna identificada"]:
            print(f"    • {t}")
        return list(techs)
    except Exception as e:
        print(f"{Fore.RED}[✗] {e}{Style.RESET_ALL}")
        return []


def analizar_headers_cli(url):
    if not url.startswith("http"):
        url = "https://" + url
    try:
        r = httpx.get(url, timeout=10, follow_redirects=True)
        return {"status": r.status_code, "headers": dict(r.headers)}
    except Exception as e:
        return {"error": str(e)}


def mostrar_headers(resultado):
    if "error" in resultado:
        print(f"{Fore.RED}[✗] {resultado['error']}{Style.RESET_ALL}")
        return
    print(f"Status: {resultado['status']}")
    seguridad = ["Strict-Transport-Security",
                 "X-Frame-Options", "Content-Security-Policy"]
    for h in seguridad:
        val = resultado["headers"].get(h)
        print(f"  {h}: {'✓' if val else '✗'}")


def detectar_tecnologias_cli(url):
    return detectar_tecnologias(url)


def mostrar_tecnologias(techs):
    for t in techs:
        print(f"  • {t}")


def extraer_links_cli(url):
    return extraer_links(url)


def mostrar_links(links):
    for l in links[:20]:
        print(f"  {l}")


def ejecutar():
    while True:
        limpiar_pantalla()
        print(f"\n{Fore.MAGENTA}=== 🕷️ ANÁLISIS WEB (Async) ==={Style.RESET_ALL}")
        print("  [1] Buscar subdirectorios (async)")
        print("  [2] Extraer enlaces")
        print("  [3] Detectar tecnologías")
        print("  [4] Volver")
        op = input("\n[>] Opción: ").strip()
        url = input("URL: ").strip() if op in ("1", "2", "3") else ""
        if url and not url.startswith("http"):
            url = "https://" + url
        if op == "1":
            buscar_subdirectorios(url)
            esperar_input()
        elif op == "2":
            extraer_links(url)
            esperar_input()
        elif op == "3":
            detectar_tecnologias(url)
            esperar_input()
        elif op == "4":
            break
