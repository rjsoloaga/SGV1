import tkinter as tk
from tkinter import ttk, messagebox
from controllers.usuario_controller import agregar_usuario, listar_usuarios

class GestionUsuarios:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Usuarios")
        self.root.geometry("700x500")

        tk.Label(root, text="Registrar Nuevo Usuario", font=("Arial", 16)).pack(pady=10)

        # Campos del formulario
        self.nombre = self.crear_campo("Nombre")
        self.username = self.crear_campo("Username")
        self.password = self.crear_campo("Contraseña", show="*")
        self.rol = ttk.Combobox(root, values=["admin", "vendedor"], width=38)
        self.rol.set("admin")
        tk.Label(root, text="Rol").pack()
        self.rol.pack(pady=5)

        tk.Button(root, text="Registrar Usuario", width=25,
                  command=self.guardar_usuario).pack(pady=10)

        # Listado de usuarios
        tk.Label(root, text="Usuarios Registrados", font=("Arial", 14)).pack(pady=10)
        self.lista_usuarios = tk.Listbox(root, width=80, height=10)
        self.lista_usuarios.pack(pady=5)

        self.cargar_lista_usuarios()

    def crear_campo(self, texto, show=None):
        tk.Label(self.root, text=texto).pack()
        entry = ttk.Entry(self.root, width=40, show=show)
        entry.pack(pady=5)
        return entry

    def guardar_usuario(self):
        nombre = self.nombre.get()
        username = self.username.get()
        password = self.password.get()
        rol = self.rol.get()

        if agregar_usuario(nombre, username, password, rol):
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.limpiar_campos()
            self.cargar_lista_usuarios()
        else:
            messagebox.showerror("Error", "No se pudo registrar el usuario.")

    def cargar_lista_usuarios(self):
        self.lista_usuarios.delete(0, tk.END)
        usuarios = listar_usuarios()
        for u in usuarios:
            self.lista_usuarios.insert(tk.END, f"{u['id_usuario']} - {u['nombre']} ({u['username']}) - {u['rol']}")

    def limpiar_campos(self):
        self.nombre.delete(0, tk.END)
        self.username.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.rol.set("vendedor")