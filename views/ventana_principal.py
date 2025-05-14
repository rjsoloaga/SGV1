# views/ventana_principal.py

import tkinter as tk
from ttkbootstrap import Window as BootstrapWindow, ttk


class VentanaPrincipal:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.root.title("Sistema de Gestión - Principal")
        self.root.geometry("1000x600")

        # Frame principal dividido
        self.frame_principal = ttk.Frame(self.root)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Menú lateral izquierdo
        self.barra_menu = ttk.Frame(self.frame_principal, width=200, bootstyle="secondary")
        self.barra_menu.pack(side=tk.LEFT, fill=tk.Y)

        # Área derecha para contenido dinámico
        self.area_contenido = ttk.Frame(self.frame_principal, padding=10)
        self.area_contenido.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Botones del menú + atajos visibles
        ttk.Button(
            self.barra_menu,
            text="Registrar Venta [F2]",
            bootstyle="primary",
            command=lambda: self.cargar_vista("venta")
        ).pack(pady=10, padx=10, fill=tk.X)

        ttk.Button(
            self.barra_menu,
            text="Gestión de Inventario [F3]",
            bootstyle="info",
            command=lambda: self.cargar_vista("inventario")
        ).pack(pady=10, padx=10, fill=tk.X)

        ttk.Button(
            self.barra_menu,
            text="Cierre de Caja [F4]",
            bootstyle="warning",
            command=lambda: self.cargar_vista("caja")
        ).pack(pady=10, padx=10, fill=tk.X)


        ttk.Button(
            self.barra_menu,
            text="Buscar Producto [F5]",
            bootstyle="warning",
            command=lambda: self.cargar_vista("buscar")
        ).pack(pady=10, padx=10, fill=tk.X)

        ttk.Button(
            self.barra_menu,
            text="Cerrar Sesión [Esc]",
            bootstyle="danger",
            command=self.cerrar_sesion
        ).pack(pady=10, padx=10, fill=tk.X)


        # Atajos globales
        self.root.bind("<F2>", lambda e: self.cargar_vista("venta"))
        self.root.bind("<F3>", lambda e: self.cargar_vista("inventario"))
        self.root.bind("<F4>", lambda e: self.cargar_vista("caja"))
        self.root.bind("<F5>", lambda e: self.cargar_vista("buscar"))
        self.root.bind("<Escape>", lambda e: self.cerrar_sesion())

        # Carga inicial
        self.vista_actual = None
        self.cargar_vista("venta")


    def cargar_vista(self, vista):
        if self.vista_actual:
            self.vista_actual.pack_forget()
            self.vista_actual.destroy()

        if vista == "venta":
            from views.registrar_venta import RegistrarVenta
            self.vista_actual = RegistrarVenta(self.area_contenido, self.usuario)
        elif vista == "inventario":
            from views.gestion_productos import GestionProductos
            self.vista_actual = GestionProductos(self.area_contenido)
        elif vista == "buscar":
            from views.buscar_producto import VentanaBuscarProducto
            self.vista_actual = VentanaBuscarProducto(self.area_contenido, self.agregar_producto_directo)
        elif vista == "caja":
            from views.cierre_caja import VentanaCierreCaja
            self.vista_actual = VentanaCierreCaja(self.area_contenido)

        self.vista_actual.pack(fill=tk.BOTH, expand=True)
        self.resaltar_boton(vista)

        # Solo activa 't' cuando estás en Registrar Venta
        if hasattr(self.vista_actual, "finalizar_venta"):
            self.root.bind("<t>", lambda e: self.vista_actual.finalizar_venta())
        else:
            self.root.unbind("<t>")

    def resaltar_boton(self, boton_activo):
        for btn in self.barra_menu.winfo_children():
            if btn.winfo_class() == "TButton":
                texto = btn.cget("text").lower()
                if boton_activo in texto:
                    btn.configure(bootstyle="warning")
                else:
                    btn.configure(bootstyle="default")


    def cerrar_sesion(self):
        self.root.destroy()
        from views.login import VentanaLogin
        VentanaLogin(BootstrapWindow(themename="superhero"))


    def agregar_producto_directo(self, producto):
        """Recibe un producto desde buscar_producto.py"""
        from views.registrar_venta import RegistrarVenta

        if isinstance(self.vista_actual, RegistrarVenta):
            self.vista_actual.codigo_barras.delete(0, tk.END)
            self.vista_actual.codigo_barras.insert(0, producto["codigo_barras"])
            self.vista_actual.agregar_producto()
        else:
            self.cargar_vista("venta")
            self.root.update_idletasks()
            self.vista_actual.codigo_barras.delete(0, tk.END)
            self.vista_actual.codigo_barras.insert(0, producto["codigo_barras"])
            self.vista_actual.agregar_producto()