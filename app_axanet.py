""
import os
from datetime import datetime
import uuid
from storage import (
    CLIENTS_DIR,
    ensure_clients_dir,
    normalize_filename,
    client_filepath,
    read_client_file,
    write_client_file,
    list_client_files,
    delete_client_file,
)

def generate_id(name: str) -> str:
    # ID: iniciales + timestamp
    initials = "".join([p[0].upper() for p in name.split() if p])
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{initials}_{timestamp}"

def create_client():
    name = input("Nombre completo del cliente: ").strip()
    if not name:
        print("Nombre vacío. Cancelando.")
        return
    telefono = input("Teléfono: ").strip()
    correo = input("Correo: ").strip()
    servicio = input("Descripción del primer servicio: ").strip()
    fecha = datetime.now().strftime("%Y-%m-%d")
    client_id = generate_id(name)
    data = {
        "Nombre": name,
        "ID_Cliente": client_id,
        "Telefono": telefono,
        "Correo": correo,
        "FechaRegistro": fecha,
        "Servicios": [f"- {servicio} ({fecha})"] if servicio else []
    }
    ensure_clients_dir()
    filename = normalize_filename(name) + ".txt"
    path = client_filepath(filename)
    if os.path.exists(path):
        print(f"Ya existe un cliente con el archivo {filename}.")
        proceed = input("Desea sobrescribirlo? (s/n): ").lower()
        if proceed != "s":
            print("Cancelado.")
            return
    write_client_file(path, data)
    print(f"Cliente creado: {path}")

def view_client():
    ensure_clients_dir()
    choice = input("1) Buscar por nombre\n2) Listar todos\nElija opción: ").strip()
    if choice == "1":
        name = input("Nombre del cliente: ").strip()
        filename = normalize_filename(name) + ".txt"
        path = client_filepath(filename)
        if not os.path.exists(path):
            print("Cliente no encontrado.")
            return
        print(read_client_file(path))
    elif choice == "2":
        files = list_client_files()
        if not files:
            print("No hay clientes.")
            return
        print("Clientes encontrados:")
        for f in files:
            print("-", f)
    else:
        print("Opción inválida.")

def add_service():
    ensure_clients_dir()
    name = input("Nombre del cliente a actualizar: ").strip()
    filename = normalize_filename(name) + ".txt"
    path = client_filepath(filename)
    if not os.path.exists(path):
        print("Cliente no encontrado.")
        return
    servicio = input("Descripción del nuevo servicio: ").strip()
    if not servicio:
        print("Servicio vacío. Cancelando.")
        return
    fecha = datetime.now().strftime("%Y-%m-%d")
    content = read_client_file(path)
    # Append service line
    content_lines = content.splitlines()
    # Find Servicios: section; if not present, add it
    try:
        idx = content_lines.index("Servicios:")
    except ValueError:
        content_lines.append("Servicios:")
        idx = content_lines.index("Servicios:")
    content_lines.insert(idx+1, f"- {servicio} ({fecha})")
    new_content = "\n".join(content_lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Servicio agregado.")

def delete_client():
    ensure_clients_dir()
    name = input("Nombre del cliente a eliminar: ").strip()
    filename = normalize_filename(name) + ".txt"
    path = client_filepath(filename)
    if not os.path.exists(path):
        print("Cliente no encontrado.")
        return
    confirm = input(f"Confirma eliminar {filename}? (s/n): ").lower()
    if confirm == "s":
        delete_client_file(path)
        print("Cliente eliminado.")
    else:
        print("Cancelado.")

def main_menu():
    while True:
        print("\nAxanet - Gestión de Clientes")
        print("1) Crear nuevo cliente")
        print("2) Visualizar cliente / Listar clientes")
        print("3) Agregar servicio a cliente existente")
        print("4) Eliminar cliente")
        print("5) Salir")
        opt = input("Elija una opción: ").strip()
        if opt == "1":
            create_client()
        elif opt == "2":
            view_client()
        elif opt == "3":
            add_service()
        elif opt == "4":
            delete_client()
        elif opt == "5":
            print("Saliendo.")
            break
        else:
            print("Opción inválida.")

if __name__ == '__main__':
    main_menu()
