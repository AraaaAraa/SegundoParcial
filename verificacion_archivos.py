import os
import json

def verificar_archivo_existe(archivo, mensaje_error) -> None:
    if not os.path.exists(archivo):
        print(f"{mensaje_error}")
        return False
    return True

def cargar_json(archivo, default=None) -> None:
    if default is None:
        default = {}
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return default

def guardar_json(archivo, datos) -> None:
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    return True

def verificar_archivo_y_devolver_path(path: str) -> str:
    abs_path = os.path.join(os.path.dirname(__file__), path)
    if verificar_archivo_existe(abs_path, f"No se encontró el archivo: {abs_path}"):
        return abs_path
    return ""