import tkinter as tk
from tkinter import ttk
from controllers.inventario_controller import agregar_producto

class GestionInventario:
    def __init__(self, root, usuario):
        self.root = root
        self.root.title("Gestión de Inventario")
        self.root.geometry("700x500")

        tk.Label(root, text="Registro de Producto", font=("Arial", 16)).pack(pady=10)

        # Campos del formulario
        self.codigo_barras = self.crear_campo("Código de Barras")
        self.codigo_barras.focus()
        self.nombre = self.crear_campo("Nombre")
        self.descripcion = self.crear_campo("Descripción (Opcional)")
        self.precio = self.crear_campo("Precio")
        self.stock = self.crear_campo("Stock")
        self.fecha_vencimiento = self.crear_campo("Fecha de Vencimiento (YYYY-MM-DD)")
        self.ruta_imagen = self.crear_campo("Ruta de Imagen (Opcional)")

        tk.Button(root, text="Registrar Producto", width=25,
                  command=self.guardar_producto).pack(pady=20)

    def crear_campo(self, texto):
        tk.Label(self.root, text=texto).pack()
        entry = ttk.Entry(self.root, width=40)
        entry.pack(pady=5)
        return entry

    def guardar_producto(self):
        codigo = self.codigo_barras.get()
        nombre = self.nombre.get()
        descripcion = self.descripcion.get()
        precio = self.precio.get()
        stock = self.stock.get()
        vencimiento = self.fecha_vencimiento.get()
        imagen = self.ruta_imagen.get()
        creado_por = 1  # Esto deberías tomarlo del usuario logueado

        if agregar_producto(codigo, nombre, descripcion, precio, stock, vencimiento, imagen, creado_por):
            from tkinter import messagebox
            messagebox.showinfo("Éxito", "Producto registrado correctamente.")
        else:
            from tkinter import messagebox
            messagebox.showerror("Error", "No se pudo registrar el producto.")