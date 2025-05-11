# views/gestion_productos.py

import tkinter as tk
from ttkbootstrap import ttk, Window
from models.producto import obtener_producto_por_codigo, guardar_producto
from config_db import conectar


class GestionProductos(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)

        # Campo de entrada para código de barras
        frame_entrada = ttk.Frame(self)
        frame_entrada.pack(pady=10, anchor="w")

        ttk.Label(frame_entrada, text="Código de Barras", bootstyle="inverse").pack(side=tk.LEFT)
        self.codigo_barras = ttk.Entry(frame_entrada, width=30, font=("Arial", 14))
        self.codigo_barras.pack(side=tk.LEFT, padx=5)
        self.codigo_barras.bind("<Return>", lambda e: self.buscar_producto())
        self.codigo_barras.focus_set()

        # Campos del producto
        frame_datos = ttk.Frame(self)
        frame_datos.pack(fill=tk.BOTH, expand=True)

        self.campos = {}

        ttk.Label(frame_datos, text="Nombre", anchor='w').pack(fill=tk.X)
        self.campos['nombre'] = ttk.Entry(frame_datos, width=40)
        self.campos['nombre'].pack(pady=5)

        ttk.Label(frame_datos, text="Categoría", anchor='w').pack(fill=tk.X)
        self.campos['categoria'] = ttk.Entry(frame_datos, width=40)
        self.campos['categoria'].insert(0, "otros")
        self.campos['categoria'].pack(pady=5)

        ttk.Label(frame_datos, text="Descripción (Opcional)", anchor='w').pack(fill=tk.X)
        self.campos['descripcion'] = ttk.Entry(frame_datos, width=40)
        self.campos['descripcion'].pack(pady=5)

        ttk.Label(frame_datos, text="Precio Costo", anchor='w').pack(fill=tk.X)
        self.campos['precio_costo'] = ttk.Entry(frame_datos, width=40)
        self.campos['precio_costo'].pack(pady=5)

        ttk.Label(frame_datos, text="Precio Venta", anchor='w').pack(fill=tk.X)
        self.campos['precio_venta'] = ttk.Entry(frame_datos, width=40)
        self.campos['precio_venta'].pack(pady=5)

        ttk.Label(frame_datos, text="Stock", anchor='w').pack(fill=tk.X)
        self.campos['stock'] = ttk.Entry(frame_datos, width=40)
        self.campos['stock'].pack(pady=5)

        ttk.Label(frame_datos, text="Fecha de Vencimiento (YYYY-MM-DD)", anchor='w').pack(fill=tk.X)
        self.campos['vencimiento'] = ttk.Entry(frame_datos, width=40)
        self.campos['vencimiento'].pack(pady=5)

        ttk.Label(frame_datos, text="Ruta de Imagen (opcional)", anchor='w').pack(fill=tk.X)
        self.campos['imagen'] = ttk.Entry(frame_datos, width=40)
        self.campos['imagen'].pack(pady=5)

        # Botón Guardar
        self.boton_guardar = ttk.Button(
            self,
            text="Guardar Producto",
            bootstyle="success",
            command=self.guardar_producto
        )
        self.boton_guardar.pack(pady=10)

        self.producto_actual = None

    def buscar_producto(self):
        codigo = self.codigo_barras.get().strip()
        if not codigo:
            return

        self.producto_actual = obtener_producto_por_codigo(codigo)

        for campo in ['nombre', 'categoria', 'descripcion', 'precio_costo', 'precio_venta', 'stock', 'vencimiento', 'imagen']:
            self.campos[campo].delete(0, tk.END)

        if self.producto_actual:
            self.campos['nombre'].insert(0, self.producto_actual['nombre'])
            self.campos['categoria'].insert(0, self.producto_actual['categoria'])

            if self.producto_actual['descripcion']:
                self.campos['descripcion'].insert(0, self.producto_actual['descripcion'])

            if self.producto_actual['precio_costo']:
                self.campos['precio_costo'].insert(0, str(self.producto_actual['precio_costo']))

            self.campos['precio_venta'].insert(0, str(self.producto_actual['precio']))
            self.campos['stock'].insert(0, str(self.producto_actual['stock']))

            if self.producto_actual['fecha_vencimiento']:
                self.campos['vencimiento'].insert(0, str(self.producto_actual['fecha_vencimiento']))

            if self.producto_actual['ruta_imagen']:
                self.campos['imagen'].insert(0, self.producto_actual['ruta_imagen'])

            self.boton_guardar.config(text="Actualizar Producto")
        else:
            self.boton_guardar.config(text="Guardar Nuevo Producto")

    def guardar_producto(self):
        codigo = self.codigo_barras.get().strip()
        nombre = self.campos['nombre'].get().strip()
        categoria = self.campos['categoria'].get().strip() or "otros"
        descripcion = self.campos['descripcion'].get().strip()
        precio_costo_str = self.campos['precio_costo'].get().strip()
        precio_venta_str = self.campos['precio_venta'].get().strip()
        stock_str = self.campos['stock'].get().strip()
        vencimiento = self.campos['vencimiento'].get().strip()
        imagen = self.campos['imagen'].get().strip()

        if not codigo or not nombre or not precio_costo_str or not precio_venta_str or not stock_str:
            from tkinter import messagebox
            messagebox.showwarning("Datos incompletos", "Los campos obligatorios deben estar completos.")
            return

        try:
            precio_costo = float(precio_costo_str)
            precio_venta = float(precio_venta_str)
            stock = int(stock_str)
        except ValueError:
            from tkinter import messagebox
            messagebox.showerror("Datos inválidos", "Precio y stock deben ser números válidos.")
            return

        conn = conectar()
        if not conn:
            from tkinter import messagebox
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        cursor = conn.cursor()

        if self.producto_actual:
            # Actualizar producto existente
            cursor.execute("""
                UPDATE productos 
                SET nombre = %s, categoria = %s, descripcion = %s, precio_costo = %s, precio = %s,
                    stock = %s, fecha_vencimiento = %s, ruta_imagen = %s
                WHERE codigo_barras = %s
            """, (nombre, categoria, descripcion, precio_costo, precio_venta, stock, vencimiento, imagen, codigo))

            conn.commit()
            from tkinter import messagebox
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
        else:
            # Registrar producto nuevo
            cursor.execute("""
                INSERT INTO productos 
                (codigo_barras, nombre, categoria, descripcion, precio_costo, precio, stock, fecha_vencimiento, ruta_imagen, creado_por)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (codigo, nombre, categoria, descripcion, precio_costo, precio_venta, stock, vencimiento, imagen, 1))  # Reemplaza '1' por ID real si necesitas

            conn.commit()
            from tkinter import messagebox
            messagebox.showinfo("Éxito", "Producto registrado correctamente.")

        conn.close()
        self.limpiar_formulario()

    def limpiar_formulario(self):
        self.codigo_barras.delete(0, tk.END)
        for campo in self.campos.values():
            campo.delete(0, tk.END)
        self.codigo_barras.focus_set()