# views/ventana_principal.py

import tkinter as tk
from ttkbootstrap import Window as BootstrapWindow, ttk


class VentanaPrincipal:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.root.title("Sistema de Gestión - Principal")
        self.root.geometry("1000x600")

        # Frame principal con división entre menú y contenido
        self.frame_principal = ttk.Frame(self.root)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Barra lateral (menú)
        self.barra_menu = ttk.Frame(self.frame_principal, width=200, bootstyle="secondary")
        self.barra_menu.pack(side=tk.LEFT, fill=tk.Y)

        # Contenido principal (a la derecha)
        self.area_contenido = ttk.Frame(self.frame_principal, padding=10)
        self.area_contenido.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Botones del menú
        ttk.Button(self.barra_menu, text="Registrar Venta", bootstyle="primary", width=20,
                  command=lambda: self.cargar_vista("venta")).pack(pady=10, padx=10, fill=tk.X)

        ttk.Button(self.barra_menu, text="Gestión de Inventario", bootstyle="info", width=20,
                  command=lambda: self.cargar_vista("inventario")).pack(pady=10, padx=10, fill=tk.X)

        ttk.Button(self.barra_menu, text="Cerrar Sesión", bootstyle="danger", width=20,
                  command=self.cerrar_sesion).pack(pady=10, padx=10, fill=tk.X)

        # Carga inicial
        self.vista_actual = None
        self.cargar_vista("venta")  # Por defecto carga ventas

    def cargar_vista(self, vista):
        if self.vista_actual:
            self.vista_actual.pack_forget()  # ✅ Mejor que destroy(), ya que ahora es un Frame
            self.vista_actual.destroy()    # ✅ Puedes dejar esto solo si quieres liberar memoria
            self.vista_actual = None

        if vista == "venta":
            from views.registrar_venta import RegistrarVenta
            self.vista_actual = RegistrarVenta(self.area_contenido, self.usuario)
        elif vista == "inventario":
            from views.gestion_productos import GestionProductos
            self.vista_actual = GestionProductos(self.area_contenido)

        self.vista_actual.pack(fill=tk.BOTH, expand=True)

    def cerrar_sesion(self):
        self.root.destroy()
        from views.login import VentanaLogin
        VentanaLogin(BootstrapWindow(themename="superhero"))