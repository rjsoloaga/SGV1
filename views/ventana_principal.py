# views/ventana_principal.py

import tkinter as tk
from ttkbootstrap import Window as BootstrapWindow, ttk


class VentanaPrincipal:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.root.title("Sistema de Gestión - Principal")
        self.root.geometry("800x600")

        # Bienvenida
        ttk.Label(
            self.root,
            text=f"Bienvenido, {usuario['nombre']}",
            bootstyle="inverse",
            font=("Arial", 16)
        ).pack(pady=20)

        # Botones principales
        frame_botones = ttk.Frame(self.root)
        frame_botones.pack(pady=30)

        ttk.Button(
            frame_botones,
            text="Registrar Venta",
            bootstyle="primary",
            width=30,
            command=lambda: self.abrir_registrar_venta(usuario)
        ).pack(pady=10)

        ttk.Button(
            frame_botones,
            text="Gestión de Inventario",
            bootstyle="info",
            width=30,
            command=self.abrir_gestion_inventario
        ).pack(pady=10)

        ttk.Button(
            frame_botones,
            text="Cerrar Sesión",
            bootstyle="danger",
            width=30,
            command=self.cerrar_sesion
        ).pack(pady=10)

    def abrir_registrar_venta(self, usuario):
        from views.registrar_venta import RegistrarVenta
        RegistrarVenta(tk.Toplevel(self.root), usuario)

    def abrir_gestion_inventario(self):
        from views.gestion_productos import GestionProductos
        GestionProductos(tk.Toplevel(self.root))

    def cerrar_sesion(self):
        self.root.destroy()
        from views.login import VentanaLogin
        VentanaLogin(BootstrapWindow(themename="superhero"))