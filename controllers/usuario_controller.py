from models.usuario import registrar_usuario, obtener_todos_los_usuarios
from tkinter import messagebox

def agregar_usuario(nombre, username, password, rol):
    if not nombre or not username or not password:
        messagebox.showwarning("Datos incompletos", "Nombre, username y contraseña son obligatorios.")
        return False

    return registrar_usuario(nombre, username, password, rol)

def listar_usuarios():
    return obtener_todos_los_usuarios()