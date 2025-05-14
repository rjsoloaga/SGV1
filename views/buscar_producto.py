# views/buscar_producto.py

import tkinter as tk
from ttkbootstrap import ttk


class VentanaBuscarProducto:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback

        # Creamos ventana emergente
        self.ventana_busqueda = tk.Toplevel(master)
        self.ventana_busqueda.title("Buscar Producto")
        self.ventana_busqueda.geometry("600x400")

        # Campo de búsqueda
        self.entry_buscar = ttk.Entry(self.ventana_busqueda, font=("Arial", 14))
        self.entry_buscar.pack(pady=10, padx=10, fill=tk.X)
        self.entry_buscar.focus_set()
        self.entry_buscar.bind("<KeyRelease>", lambda e: self.filtrar_productos())
        self.entry_buscar.bind("<Return>", lambda e: self.seleccionar_producto())

        # Tabla de resultados con scroll
        frame_tabla = ttk.Frame(self.ventana_busqueda)
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(frame_tabla)
        scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=canvas.yview)
        self.frame_resultados = ttk.Frame(canvas)

        self.frame_resultados.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.frame_resultados, anchor="nw", width=580)
        canvas.configure(yscrollcommand=scrollbar_y.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        self.productos = []
        self.filtrar_productos()

    def filtrar_productos(self, event=None):
        """Filtra productos por nombre según lo que escribe el usuario"""
        from models.producto import obtener_productos_por_nombre

        texto_busqueda = self.entry_buscar.get().strip().lower()
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()

        if not texto_busqueda:
            ttk.Label(self.frame_resultados, text="Escriba para buscar...", bootstyle="light").pack(pady=10)
            return

        self.productos = obtener_productos_por_nombre(texto_busqueda)
        if not self.productos:
            ttk.Label(self.frame_resultados, text="No se encontraron productos.", bootstyle="light").pack(pady=10)
            return

        for prod in self.productos:
            fila = ttk.Frame(self.frame_resultados)
            fila.pack(fill=tk.X, pady=2)

            ttk.Label(fila, text=prod['nombre'], width=30, anchor="w").pack(side=tk.LEFT, padx=5)
            ttk.Label(fila, text=f"${prod['precio']:.2f}", width=10, anchor="e").pack(side=tk.RIGHT, padx=5)
            fila.bind("<Button-1>", lambda e, p=prod: self.seleccionar_producto(p))

    def seleccionar_producto(self, producto):
        """Envía el producto seleccionado a registrar_venta.py"""
        self.ventana_busqueda.destroy()
        self.callback(producto)