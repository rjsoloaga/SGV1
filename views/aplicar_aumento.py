# views/aplicar_aumento.py

import tkinter as tk
from tkinter import ttk, messagebox
from config_db import conectar


class AplicarAumento:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicar Aumento por Categoría")
        self.root.geometry("400x250")

        ttk.Label(root, text="Categoría", bootstyle="light", font=("Arial", 12)).pack(pady=5)
        self.categoria = ttk.Entry(root, width=30)
        self.categoria.insert(0, "lácteos")
        self.categoria.pack(pady=5)

        ttk.Label(root, text="Porcentaje de Aumento (%)", bootstyle="light", font=("Arial", 12)).pack(pady=5)
        self.porcentaje = ttk.Entry(root, width=30)
        self.porcentaje.pack(pady=5)

        ttk.Button(root, text="Aplicar Aumento", width=20, bootstyle="danger",
                   command=self.aplicar_aumento).pack(pady=10)

    def aplicar_aumento(self):
        categoria = self.categoria.get().strip()
        porcentaje_str = self.porcentaje.get().strip()

        if not categoria or not porcentaje_str:
            messagebox.showwarning("Faltan datos", "Ingrese categoría y porcentaje")
            return

        try:
            porcentaje = float(porcentaje_str)
            if porcentaje < 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Porcentaje inválido")
            return

        conn = conectar()
        if not conn:
            return

        cursor = conn.cursor()
        try:
            cursor.execute(f"""
                UPDATE productos 
                SET precio = precio * (1 + {porcentaje}/100), 
                    precio_costo = precio_costo * (1 + {porcentaje}/100)
                WHERE categoria = '{categoria}'
            """)
            conn.commit()
            messagebox.showinfo("Éxito", f"Aumento del {porcentaje}% aplicado a '{categoria}'")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo aplicar el aumento:\n{e}")
        finally:
            conn.close()