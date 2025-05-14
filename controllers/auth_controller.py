from models.usuario import obtener_usuario_por_username  # Asegúrate de que esta función existe
import bcrypt
import tkinter as tk
from tkinter import messagebox
from views.ventana_principal import VentanaPrincipal

def iniciar_sesion(root, usuario, clave):
    resultado = validar_credenciales(usuario, clave)  # Ahora usa bcrypt
    
    if resultado:
        root.withdraw()
        VentanaPrincipal(tk.Toplevel(root), {
            "nombre": resultado['nombre'],
            "id_usuario": resultado['id_usuario'],
            "rol": resultado['rol']
        })
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")