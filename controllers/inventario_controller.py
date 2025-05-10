from models.producto import registrar_producto, obtener_todos_los_productos
from tkinter import messagebox

def agregar_producto(codigo, nombre, descripcion, precio, stock, vencimiento, imagen, creado_por):
    if not codigo or not nombre or not precio or not stock:
        messagebox.showwarning("Faltan datos", "Todos los campos obligatorios deben estar completos.")
        return False

    try:
        precio = float(precio)
        stock = int(stock)
    except ValueError:
        messagebox.showerror("Datos inválidos", "Precio y stock deben ser números válidos.")
        return False

    return registrar_producto(codigo, nombre, descripcion, precio, stock, vencimiento, imagen, creado_por)

def listar_productos():
    return obtener_todos_los_productos()