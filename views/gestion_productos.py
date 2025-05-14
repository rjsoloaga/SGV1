# views/gestion_productos.py

import tkinter as tk
from ttkbootstrap import ttk
from tkinter import messagebox
from config_db import conectar


class GestionProductos(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)

        # Campo de entrada para código de barras
        frame_entrada = ttk.Frame(self)
        frame_entrada.pack(pady=10)

        ttk.Label(frame_entrada, text="Código de Barras", bootstyle="inverse").pack(side=tk.LEFT)
        self.codigo_barras = ttk.Entry(frame_entrada, width=30, font=("Arial", 14))
        self.codigo_barras.pack(side=tk.LEFT, padx=5)
        self.codigo_barras.bind("<Return>", lambda e: self.buscar_producto())
        self.codigo_barras.focus_set()

        # Campos del producto
        frame_datos = ttk.Frame(self)
        frame_datos.pack(pady=10, fill=tk.BOTH, expand=True)

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

        ttk.Label(frame_datos, text="Precio Venta", anchor='w').pack(fill=tk.X)
        self.campos['precio_venta'] = ttk.Entry(frame_datos, width=40)
        self.campos['precio_venta'].pack(pady=5)

        ttk.Label(frame_datos, text="Stock", anchor='w').pack(fill=tk.X)
        self.campos['stock'] = ttk.Entry(frame_datos, width=40)
        self.campos['stock'].pack(pady=5)

        ttk.Label(frame_datos, text="Fecha de Vencimiento YYYY-MM-DD", anchor='w').pack(fill=tk.X)
        self.campos['vencimiento'] = ttk.Entry(frame_datos, width=40)
        self.campos['vencimiento'].pack(pady=5)

        ttk.Label(frame_datos, text="Ruta de Imagen (opcional)", anchor='w').pack(fill=tk.X)
        self.campos['imagen'] = ttk.Entry(frame_datos, width=40)
        self.campos['imagen'].pack(pady=5)

        # Botón guardar
        ttk.Button(
            self,
            text="Guardar Producto",
            bootstyle="success",
            command=self.guardar_producto
        ).pack(pady=10)

        self.producto_actual = None

    def buscar_producto(self, event=None):
        codigo = self.codigo_barras.get().strip()
        if not codigo:
            return

        from models.producto import obtener_producto_por_codigo
        self.producto_actual = obtener_producto_por_codigo(codigo)

        for campo in ['nombre', 'categoria', 'descripcion', 'precio_venta', 'stock', 'vencimiento', 'imagen']:
            self.campos[campo].delete(0, tk.END)

        if self.producto_actual:
            self.campos['nombre'].insert(0, self.producto_actual['nombre'])
            self.campos['categoria'].insert(0, self.producto_actual.get('categoria', 'otros'))
            self.campos['descripcion'].insert(0, self.producto_actual.get('descripcion', ''))
            self.campos['precio_venta'].insert(0, str(self.producto_actual['precio']))
            self.campos['stock'].insert(0, str(self.producto_actual['stock']))

            if self.producto_actual.get('fecha_vencimiento'):
                self.campos['vencimiento'].insert(0, str(self.producto_actual['fecha_vencimiento']))

            if self.producto_actual.get('ruta_imagen'):
                self.campos['imagen'].insert(0, self.producto_actual['ruta_imagen'])

        else:
            messagebox.showinfo("Producto no encontrado", "Puede registrar uno nuevo.")

        self.codigo_barras.delete(0, tk.END)
        self.codigo_barras.focus_set()

    def guardar_producto(self):
        codigo = self.codigo_barras.get().strip()
        nombre = self.campos['nombre'].get().strip()
        categoria = self.campos['categoria'].get().strip() or "otros"
        descripcion = self.campos['descripcion'].get().strip() or None
        precio_venta_str = self.campos['precio_venta'].get().strip()
        stock_str = self.campos['stock'].get().strip()
        vencimiento = self.campos['vencimiento'].get().strip() or None
        imagen = self.campos['imagen'].get().strip() or None

        if not nombre or not precio_venta_str or not stock_str:
            messagebox.showerror("Datos incompletos", "Nombre, Precio y Stock son obligatorios.")
            return

        try:
            precio_venta = float(precio_venta_str)
            stock = int(stock_str)
        except ValueError:
            messagebox.showerror("Datos inválidos", "Precio y stock deben ser números válidos.")
            return

        conn = conectar()
        if not conn:
            return

        cursor = conn.cursor()

        if self.producto_actual:
            # Actualizar producto existente
            cursor.execute("""
                UPDATE productos 
                SET nombre = %s, categoria = %s, descripcion = %s, 
                    precio = %s, stock = %s, fecha_vencimiento = %s, ruta_imagen = %s
                WHERE codigo_barras = %s
            """, (
                nombre, categoria, descripcion,
                precio_venta, stock, vencimiento,
                imagen, codigo
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
        else:
            # Registrar producto nuevo
            cursor.execute("""
                INSERT INTO productos 
                (codigo_barras, nombre, categoria, descripcion, precio, stock, fecha_vencimiento, ruta_imagen, creado_por)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                codigo, nombre, categoria, descripcion,
                precio_venta, stock, vencimiento,
                imagen, 1  # Cambia por el id real del usuario si lo tienes
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto registrado correctamente.")

        conn.close()
        self.limpiar_formulario()

    def limpiar_formulario(self):
        self.codigo_barras.delete(0, tk.END)
        for campo in ['nombre', 'categoria', 'descripcion', 'precio_venta', 'stock', 'vencimiento', 'imagen']:
            self.campos[campo].delete(0, tk.END)
        self.codigo_barras.focus_set()