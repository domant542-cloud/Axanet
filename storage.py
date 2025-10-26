"""
storage.py - funciones de manejo de archivos para Axanet
"""
import os
from pathlib import Path

CLIENTS_DIR = Path.cwd() / "clientes"

def ensure_clients_dir():
    CLIENTS_DIR.mkdir(exist_ok=True)

def normalize_filename(name: str) -> str:
    # Normaliza nombre para filename: minusculas, guiones bajos, sin acentos basicos
    import re, unicodedata
    name = unicodedata.normalize("NFKD", name).encode("ASCII", "ignore").decode()
    name = re.sub(r"[^\w\s-]", "", name).strip().lower()
    name = re.sub(r"[\s]+", "_", name)
    return name

def client_filepath(filename: str) -> str:
    return str(CLIENTS_DIR / filename)

def write_client_file(path: str, data: dict):
    lines = []
    lines.append(f"Nombre: {data.get('Nombre','')}")
    lines.append(f"ID_Cliente: {data.get('ID_Cliente','')}")
    lines.append(f"Telefono: {data.get('Telefono','')}")
    lines.append(f"Correo: {data.get('Correo','')}")
    lines.append(f"FechaRegistro: {data.get('FechaRegistro','')}")
    lines.append("Servicios:")
    for s in data.get("Servicios", []):
        lines.append(s)
    content = "\\n".join(lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def read_client_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def list_client_files():
    ensure_clients_dir()
    return [p.name for p in CLIENTS_DIR.glob("*.txt")]

def delete_client_file(path: str):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
