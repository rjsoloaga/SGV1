# views/gestion_productos.py

import tkinter as tk
from ttkbootstrap import ttk
from tkinter import messagebox, simpledialog
from PIL import ImageTk, Image
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

        # Nombre
        ttk.Label(frame_datos, text="Nombre", anchor='w').pack(fill=tk.X)
        self.campos['nombre'] = ttk.Entry(frame_datos, width=40)
        self.campos['nombre'].pack(pady=5)

        # Categoría
        ttk.Label(frame_datos, text="Categoría", anchor='w').pack(fill=tk.X)
        self.campos['categoria'] = ttk.Entry(frame_datos, width=40)
        self.campos['categoria'].insert(0, "otros")
        self.campos['categoria'].pack(pady=5)

        # Descripción
        ttk.Label(frame_datos, text="Descripción (Opcional)", anchor='w').pack(fill=tk.X)
        self.campos['descripcion'] = ttk.Entry(frame_datos, width=40)
        self.campos['descripcion'].pack(pady=5)

        # Precio Venta
        ttk.Label(frame_datos, text="Precio Venta", anchor='w').pack(fill=tk.X)
        self.campos['precio_venta'] = ttk.Entry(frame_datos, width=40)
        self.campos['precio_venta'].pack(pady=5)

        # Precio Costo (opcional)
        ttk.Label(frame_datos, text="Precio Costo", anchor='w').pack(fill=tk.X)
        self.campos['precio_costo'] = ttk.Entry(frame_datos, width=40)
        self.campos['precio_costo'].pack(pady=5)

        # Stock
        ttk.Label(frame_datos, text="Stock", anchor='w').pack(fill=tk.X)
        self.campos['stock'] = ttk.Entry(frame_datos, width=40)
        self.campos['stock'].pack(pady=5)

        # Fecha de vencimiento
        ttk.Label(frame_datos, text="Fecha de Vencimiento YYYY-MM-DD", anchor='w').pack(fill=tk.X)
        self.campos['vencimiento'] = ttk.Entry(frame_datos, width=40)
        self.campos['vencimiento'].pack(pady=5)

        # Ruta de Imagen
        ttk.Label(frame_datos, text="Ruta de Imagen (opcional)", anchor='w').pack(fill=tk.X)
        self.campos['imagen'] = ttk.Entry(frame_datos, width=40)
        self.campos['imagen'].pack(pady=5)

        # Botón calcular margen (opcional)
        ttk.Label(frame_datos, text="Margen de Ganancia (%)", anchor='w').pack(fill=tk.X)
        self.margen_input = ttk.Entry(frame_datos, width=40)
        self.margen_input.pack(pady=5)
        self.margen_input.bind("<KeyRelease>", self.calcular_precio_venta)

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

        if not self.producto_actual:
            messagebox.showinfo("Producto no encontrado", "Puede registrar uno nuevo.")
        else:
            # Solo actualiza los campos si hay producto existente
            self.campos['nombre'].delete(0, tk.END)
            self.campos['nombre'].insert(0, self.producto_actual['nombre'])

            self.campos['categoria'].delete(0, tk.END)
            self.campos['categoria'].insert(0, self.producto_actual.get('categoria', 'otros'))

            self.campos['descripcion'].delete(0, tk.END)
            if self.producto_actual.get('descripcion'):
                self.campos['descripcion'].insert(0, self.producto_actual['descripcion'])

            self.campos['precio_venta'].delete(0, tk.END)
            self.campos['precio_venta'].insert(0, str(self.producto_actual['precio']))

            self.campos['stock'].delete(0, tk.END)
            self.campos['stock'].insert(0, str(self.producto_actual['stock']))

            self.campos['vencimiento'].delete(0, tk.END)
            if self.producto_actual.get('fecha_vencimiento'):
                self.campos['vencimiento'].insert(0, str(self.producto_actual['fecha_vencimiento']))

            self.campos['imagen'].delete(0, tk.END)
            if self.producto_actual.get('ruta_imagen'):
                self.campos['imagen'].insert(0, self.producto_actual['ruta_imagen'])

            # Mostrar imagen si existe
            self.mostrar_imagen(self.producto_actual['ruta_imagen'])

        self.codigo_barras.delete(0, tk.END)
        self.codigo_barras.focus_set()

    def mostrar_imagen(self, ruta_imagen):
        """Muestra una miniatura del producto si tiene imagen"""
        if hasattr(self, 'label_imagen'):
            self.label_imagen.destroy()

        if ruta_imagen:
            try:
                img = Image.open(ruta_imagen).resize((80, 80))
                img_tk = ImageTk.PhotoImage(img)
                self.label_imagen = ttk.Label(self, image=img_tk)
                self.label_imagen.image = img_tk
                self.label_imagen.pack(pady=10)
            except Exception as e:
                print(f"❌ No se pudo cargar la imagen: {e}")

    def calcular_precio_venta(self, event=None):
        """Calcula precio_venta desde costo + margen"""
        try:
            costo = float(self.campos['precio_costo'].get() or 0.0)
            margen = float(self.margen_input.get() or 20.0)  # Margen por defecto: 20%
        except ValueError:
            return

        precio_venta = round(costo * (1 + margen / 100), 2)
        self.campos['precio_venta'].delete(0, tk.END)
        self.campos['precio_venta'].insert(0, str(precio_venta))

    def guardar_producto(self):
        codigo = self.codigo_barras.get().strip()
        nombre = self.campos['nombre'].get().strip()
        categoria = self.campos['categoria'].get().strip() or "otros"
        descripcion = self.campos['descripcion'].get().strip() or None
        precio_venta_str = self.campos['precio_venta'].get().strip()
        stock_str = self.campos['stock'].get().strip()
        vencimiento = self.campos['vencimiento'].get().strip() or None
        imagen = self.campos['imagen'].get().strip() or None
        precio_costo_str = self.campos['precio_costo'].get().strip() or None

        if not nombre or not precio_venta_str or not stock_str:
            messagebox.showerror("Datos incompletos", "Nombre, Precio y Stock son obligatorios.")
            return

        try:
            precio_venta = float(precio_venta_str)
            stock = int(stock_str)
            precio_costo = float(precio_costo_str) if precio_costo_str else None
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
                    precio = %s, stock = %s, fecha_vencimiento = %s, ruta_imagen = %s,
                    precio_costo = COALESCE(%s, precio_costo)
                WHERE codigo_barras = %s
            """, (
                nombre, categoria, descripcion,
                precio_venta, stock, vencimiento,
                imagen, precio_costo, codigo
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
        else:
            # Registrar producto nuevo
            cursor.execute("""
                INSERT INTO productos 
                (codigo_barras, nombre, categoria, descripcion, precio, stock, fecha_vencimiento, ruta_imagen, creado_por, precio_costo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                codigo, nombre, categoria, descripcion,
                precio_venta, stock, vencimiento,
                imagen, 1, precio_costo
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto registrado correctamente.")

        conn.close()
        self.limpiar_formulario()

    def limpiar_formulario(self):
        self.codigo_barras.delete(0, tk.END)
        for campo in ['nombre', 'categoria', 'descripcion', 'precio_venta', 'stock', 'vencimiento', 'imagen']:
            self.campos[campo].delete(0, tk.END)
        if hasattr(self, 'label_imagen'):
            self.label_imagen.destroy()
        self.codigo_barras.focus_set()