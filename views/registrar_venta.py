# views/registrar_venta.py

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.venta_controller import agregar_producto_a_venta


class RegistrarVenta:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.venta_id = 1
        self.total = 0.0
        self.cantidad_seleccionada = 1
        self.lista_filas = []

        self.root.title("Registrar Venta")
        self.root.geometry("800x600")

        # Campo de código de barras
        frame_entrada = ttk.Frame(self.root)
        frame_entrada.pack(pady=10)

        ttk.Label(frame_entrada, text="Código de Barras", bootstyle="inverse", font=("Arial", 12)).pack(side=tk.LEFT)
        self.codigo_barras = ttk.Entry(frame_entrada, width=30, font=("Arial", 14))
        self.codigo_barras.pack(side=tk.LEFT, padx=5)
        self.codigo_barras.bind("<Return>", lambda e: self.agregar_producto())
        self.codigo_barras.focus_set()

        # Tabla de productos (simulada)
        frame_tabla = ttk.Frame(self.root)
        frame_tabla.pack(pady=10, fill=tk.BOTH, expand=True)

        self.frame_lista = ttk.Frame(frame_tabla)
        self.frame_lista.pack()

        # Encabezados
        cols = ['CANTIDAD', 'CÓDIGO', 'PRODUCTO', 'PRECIO UNITARIO', 'SUBTOTAL']
        for i, col in enumerate(cols):
            ttk.Label(
                self.frame_lista,
                text=col,
                bootstyle="inverse-light",
                width=15 if i == 0 else 20,
                anchor="center"
            ).grid(row=0, column=i, sticky='ew')

        self.lista_filas = [0]  # Incluye encabezado

        # Total y botones
        frame_acciones = ttk.Frame(self.root)
        frame_acciones.pack(pady=10)

        self.lbl_total = ttk.Label(frame_acciones, text="Total: $0.00", bootstyle="light", font=("Arial", 16))
        self.lbl_total.grid(row=0, column=0, padx=20)

        ttk.Button(frame_acciones, text="Finalizar Venta", width=20,
                  command=self.finalizar_venta, bootstyle="success").grid(row=0, column=1, padx=10)

        ttk.Button(frame_acciones, text="Cancelar Venta", width=20,
                  command=self.cancelar_venta, bootstyle="danger").grid(row=0, column=2, padx=10)

        self.root.bind("<Escape>", lambda e: self.cancelar_venta())
        self.root.bind("<t>", lambda e: self.finalizar_venta())

    def detectar_teclas(self, event):
        if event.char.lower() == 'x':
            self.pedir_cantidad()
            self.codigo_barras.delete(0, tk.END)
            return "break"

    def pedir_cantidad(self):
        pass  # Implementación opcional si usas cantidad variable

    def agregar_producto(self, event=None):
        codigo = self.codigo_barras.get().strip()
        if not codigo or codigo.lower() == 'x':
            return

        producto = agregar_producto_a_venta(self.venta_id, codigo, self.cantidad_seleccionada)

        if producto and 'nombre' in producto and 'precio' in producto:
            try:
                precio_unitario = float(producto['precio'])
            except:
                messagebox.showerror("Error", "Precio inválido del producto")
                self.codigo_barras.delete(0, tk.END)
                self.codigo_barras.focus_set()
                return

            subtotal = precio_unitario * self.cantidad_seleccionada
            fila = len(self.lista_filas)

            ttk.Label(self.frame_lista, text=str(self.cantidad_seleccionada), width=15, anchor="center").grid(
                row=fila + 1, column=0, sticky='ew')
            ttk.Label(self.frame_lista, text=codigo, width=20, anchor="center").grid(
                row=fila + 1, column=1, sticky='ew')
            ttk.Label(self.frame_lista, text=producto['nombre'], width=30, anchor="w").grid(
                row=fila + 1, column=2, sticky='ew')
            ttk.Label(self.frame_lista, text=f"${precio_unitario:.2f}", width=20, anchor="e").grid(
                row=fila + 1, column=3, sticky='ew')
            ttk.Label(self.frame_lista, text=f"${subtotal:.2f}", width=20, anchor="e").grid(
                row=fila + 1, column=4, sticky='ew')

            self.lista_filas.append(fila + 1)
            self.total += subtotal
            self.lbl_total.config(text=f"Total: ${self.total:.2f}")
            self.codigo_barras.delete(0, tk.END)
            self.codigo_barras.focus_set()
        else:
            messagebox.showerror("Error", "Producto no válido o sin datos completos.")
            self.codigo_barras.delete(0, tk.END)
            self.codigo_barras.focus_set()

    def finalizar_venta(self, event=None):
        if self.total <= 0:
            messagebox.showwarning("Venta vacía", "No hay productos agregados.")
            return

        metodo_pago = messagebox.askquestion("Método de Pago",
                                            "¿El pago será en efectivo?\n(Si no, se generará un QR)",
                                            icon='question',
                                            type=messagebox.YESNO)

        if metodo_pago == 'yes':
            messagebox.showinfo("Pago", "Venta finalizada. Pago en efectivo.")
        else:
            self.generar_qr_mercadopago()

        self.limpiar_venta()

    def generar_qr_mercadopago(self):
        from controllers.venta_controller import generar_pago_mercadopago
        init_point = generar_pago_mercadopago(self.total, self.venta_id)

        if init_point:
            import qrcode
            from PIL import ImageTk, Image

            qr = qrcode.make(init_point)
            qr.save("temp_qr.png")

            ventana_qr = tk.Toplevel(self.root)
            img = Image.open("temp_qr.png")
            img = img.resize((300, 300))
            img_tk = ImageTk.PhotoImage(img)

            label_imagen = ttk.Label(ventana_qr, image=img_tk)
            label_imagen.image = img_tk
            label_imagen.pack(pady=10)

            mensaje = f"Total a pagar: ${self.total:.2f}\n\nEscanee este QR con la app de Mercado Pago."
            ttk.Label(ventana_qr, text=mensaje, bootstyle="light", justify="center").pack(pady=5)

            ttk.Button(ventana_qr, text="Cerrar", command=ventana_qr.destroy, bootstyle="secondary").pack(pady=10)
        else:
            messagebox.showerror("Error", "No se pudo generar el QR.")

    def cancelar_venta(self, event=None):
        if messagebox.askokcancel("Cancelar Venta", "¿Está seguro de que quiere cancelar esta venta?"):
            self.limpiar_venta()

    def limpiar_venta(self):
        self.codigo_barras.delete(0, tk.END)
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        cols = ['CANTIDAD', 'CÓDIGO', 'PRODUCTO', 'PRECIO UNITARIO', 'SUBTOTAL']
        for i, col in enumerate(cols):
            ttk.Label(
                self.frame_lista,
                text=col,
                bootstyle="inverse-light",
                width=15 if i == 0 else 20,
                anchor="center"
            ).grid(row=0, column=i, sticky='ew')

        self.lista_filas.clear()
        self.lista_filas.append(0)  # Reiniciar encabezado
        self.total = 0.0
        self.lbl_total.config(text="Total: $0.00")
        self.codigo_barras.focus_set()