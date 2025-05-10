# controllers/auth_controller.py

from models.usuario import obtener_usuario_por_username
import bcrypt
from tkinter import messagebox
import tkinter as tk
from views.ventana_principal import VentanaPrincipal
from models.usuario import validar_credenciales  # Debe devolver resultado de BD


def iniciar_sesion(root, usuario, clave):
    if usuario == "admin" and clave == "1234":
        root.withdraw()
        VentanaPrincipal(tk.Toplevel(root), {"nombre": usuario, "id_usuario": 1})
    else:
        from tkinter import messagebox
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

def iniciar_sesion(root, usuario, clave):
    resultado = validar_credenciales(usuario, clave)

    if resultado:
        root.withdraw()
        from views.ventana_principal import VentanaPrincipal
        VentanaPrincipal(tk.Toplevel(root), resultado)
    else:
        from tkinter import messagebox
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")