# views/reportes.py

import tkinter as tk
from ttkbootstrap import ttk


class VentanaReportes:
    def __init__(self, root):
        self.root = root
        self.root.title("Reportes del Sistema")
        self.root.geometry("700x500")

        ttk.Label(self.root, text="Módulo de Reportes", bootstyle="inverse", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self.root, text="Cerrar", bootstyle="secondary", command=root.destroy).pack(pady=10)