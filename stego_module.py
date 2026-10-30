"""Esteganografía: ocultar mensajes en imágenes PNG usando LSB."""
from PIL import Image
from colorama import Fore, Style
from src.utils import limpiar_pantalla, esperar_input


def ocultar_mensaje():
    """Oculta un mensaje en una imagen PNG usando el bit menos significativo."""
    img_path = input("Ruta de imagen PNG: ").strip()
    mensaje = input("Mensaje secreto: ").strip()

    if not mensaje:
        print(
            f"{Fore.RED}[✗] El mensaje no puede estar vacío{Style.RESET_ALL}")
        return

    binario = "".join(format(ord(c), "08b")
                      for c in mensaje) + "1111111111111110"

    try:
        img = Image.open(img_path).convert("RGB")
        pixeles = list(img.getdata())

        if len(binario) > len(pixeles) * 3:
            print(
                f"{Fore.RED}[✗] Imagen muy pequeña para el mensaje.{Style.RESET_ALL}")
            print(f"    Necesitas al menos {len(binario) // 3 + 1} píxeles.")
            return

        nuevos = []
        idx = 0
        for p in pixeles:
            nuevo = list(p)
            for i in range(3):
                if idx < len(binario):
                    nuevo[i] = nuevo[i] & ~1 | int(binario[idx])
                    idx += 1
            nuevos.append(tuple(nuevo))

        img.putdata(nuevos)
        salida = "stego_output.png"
        img.save(salida)
        print(f"\n{Fore.GREEN}[✓] Imagen guardada: {salida}{Style.RESET_ALL}")
        print(
            f"{Fore.CYAN}    Mensaje de {len(mensaje)} caracteres oculto.{Style.RESET_ALL}")
    except FileNotFoundError:
        print(
            f"{Fore.RED}[✗] Archivo no encontrado: {img_path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[✗] Error: {e}{Style.RESET_ALL}")


def revelar_mensaje():
    """Extrae un mensaje oculto de una imagen PNG."""
    img_path = input("Ruta de imagen PNG con mensaje: ").strip()

    try:
        img = Image.open(img_path)
        pixeles = list(img.getdata())

        binario = ""
        for p in pixeles:
            for c in p:
                binario += str(c & 1)

        chars = []
        for i in range(0, len(binario), 8):
            byte = binario[i:i+8]
            if len(byte) < 8:
                break
            if byte == "11111110":
                break
            try:
                chars.append(chr(int(byte, 2)))
            except ValueError:
                break

        mensaje = "".join(chars)
        if mensaje:
            print(
                f"\n{Fore.GREEN}[+] Mensaje oculto:{Style.RESET_ALL}\n    {mensaje}")
        else:
            print(
                f"{Fore.YELLOW}[!] No se encontró mensaje en la imagen.{Style.RESET_ALL}")
    except FileNotFoundError:
        print(
            f"{Fore.RED}[✗] Archivo no encontrado: {img_path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[✗] Error: {e}{Style.RESET_ALL}")


def ejecutar():
    """Modo interactivo del módulo."""
    while True:
        limpiar_pantalla()
        print(f"\n{Fore.MAGENTA}=== 🖼️ ESTEGANOGRAFÍA (LSB) ==={Style.RESET_ALL}")
        print("  [1] Ocultar mensaje en imagen PNG")
        print("  [2] Revelar mensaje de imagen PNG")
        print("  [3] Volver")
        op = input("\n[>] Opción: ").strip()

        if op == "1":
            ocultar_mensaje()
            esperar_input()
        elif op == "2":
            revelar_mensaje()
            esperar_input()
        elif op == "3":
            break
