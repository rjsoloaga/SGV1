import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkthemes import ThemedTk

root = ThemedTk(theme="equilux")
root.title("Ventana Base - SGV1")
root.geometry("800x600")

# Ejemplo de botones con estilo
frame = ttk.Frame(root)
frame.pack(pady=20)

ttk.Label(frame, text="Bienvenido al Sistema", bootstyle="light", font=("Arial", 16)).pack()

ttk.Button(frame, text="Registrar Venta", bootstyle="success", width=25).pack(pady=10)
ttk.Button(frame, text="Gestión de Inventario", bootstyle="info", width=25).pack(pady=10)
ttk.Button(frame, text="Cerrar Sesión", bootstyle="danger", width=25).pack(pady=10)

root.mainloop()