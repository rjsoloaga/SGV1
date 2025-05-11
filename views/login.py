# views/login.py

import tkinter as tk
from ttkbootstrap import ttk

# ✅ Cambiado aquí: ahora importamos desde models.usuario
from models.usuario import validar_credenciales  
from tkinter import messagebox


class VentanaLogin:
    def __init__(self, root):
        self.root = root
        self.root.deiconify()
        self.root.title("Inicio de Sesión - SGV1")
        self.root.geometry("300x250")

        frame_central = ttk.Frame(self.root)
        frame_central.pack(expand=True)

        ttk.Label(frame_central, text="Usuario", bootstyle="inverse").pack(pady=5)
        self.usuario = ttk.Entry(frame_central)
        self.usuario.pack(pady=5)
        self.usuario.focus()

        ttk.Label(frame_central, text="Contraseña", bootstyle="inverse").pack(pady=5)
        self.clave = ttk.Entry(frame_central, show="*")
        self.clave.pack(pady=5)

        ttk.Button(
            frame_central,
            text="Iniciar Sesión",
            bootstyle="primary",
            command=self.iniciar_sesion
        ).pack(pady=10)

    def iniciar_sesion(self):
        usuario = self.usuario.get().strip()
        clave = self.clave.get().strip()

        resultado = validar_credenciales(usuario, clave)  # ✅ Ahora sí anda

        if resultado:
            self.root.withdraw()
            from views.ventana_principal import VentanaPrincipal
            VentanaPrincipal(tk.Toplevel(self.root), resultado)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")