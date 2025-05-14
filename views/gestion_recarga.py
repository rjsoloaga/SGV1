# views/gestion_recarga.py

import tkinter as tk
from tkinter import ttk, messagebox
from models.producto import obtener_producto_por_codigo
from config_db import conectar


class GestionRecarga:
    def __init__(self, root):
        self.root = root
        self.root.title("Recargar Stock")
        self.root.geometry("400x300")

        frame_entrada = ttk.Frame(root)
        frame_entrada.pack(pady=10)

        ttk.Label(frame_entrada, text="Código de Barras", font=("Arial", 12)).pack()
        self.codigo_barras = ttk.Entry(frame_entrada, width=30)
        self.codigo_barras.pack(pady=5)
        self.codigo_barras.bind("<Return>", lambda e: self.buscar_producto())
        self.codigo_barras.focus_set()

        self.nombre_label = ttk.Label(root, text="", bootstyle="light")
        self.nombre_label.pack(pady=5)

        ttk.Label(root, text="Cantidad a recargar", bootstyle="light").pack()
        self.entry_cantidad = ttk.Entry(root, width=20)
        self.entry_cantidad.pack(pady=5)

        ttk.Label(root, text="Nueva Fecha de Vencimiento (opcional)", bootstyle="light").pack()
        self.entry_fecha = ttk.Entry(root, width=20)
        self.entry_fecha.pack(pady=5)

        ttk.Button(root, text="Actualizar Stock", width=20, bootstyle="success",
                  command=self.guardar_recarga).pack(pady=10)

        self.producto = None

    def buscar_producto(self, event=None):
        codigo = self.codigo_barras.get().strip()
        if not codigo:
            return

        self.producto = obtener_producto_por_codigo(codigo)
        if self.producto:
            self.nombre_label.config(text=f"{self.producto['nombre']} - Stock actual: {self.producto['stock']}")
            self.entry_cantidad.focus_set()
        else:
            messagebox.showerror("Error", "Producto no encontrado")
            self.codigo_barras.delete(0, tk.END)
            self.codigo_barras.focus_set()

    def guardar_recarga(self):
        codigo = self.codigo_barras.get().strip()
        cantidad_str = self.entry_cantidad.get().strip()
        nueva_fecha = self.entry_fecha.get().strip()

        if not codigo or not cantidad_str:
            messagebox.showwarning("Faltan datos", "Ingrese código y cantidad a recargar.")
            return

        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Ingrese una cantidad válida.")
            return

        conn = conectar()
        if not conn:
            return

        cursor = conn.cursor()
        try:
            if nueva_fecha:
                cursor.execute("""
                    UPDATE productos 
                    SET stock = stock + %s, fecha_vencimiento = %s
                    WHERE codigo_barras = %s
                """, (cantidad, nueva_fecha, codigo))
            else:
                cursor.execute("""
                    UPDATE productos 
                    SET stock = stock + %s
                    WHERE codigo_barras = %s
                """, (cantidad, codigo))

            conn.commit()
            messagebox.showinfo("Éxito", f"{cantidad} unidades agregadas al producto.")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo recargar el stock:\n{e}")
        finally:
            conn.close()