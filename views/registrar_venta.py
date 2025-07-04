# views/registrar_venta.py

import tkinter as tk
from ttkbootstrap import ttk
from tkinter import messagebox, simpledialog
from PIL import ImageTk, Image
import qrcode
import webbrowser


class RegistrarVenta(ttk.Frame):
    def __init__(self, master, usuario):
        super().__init__(master)
        self.usuario = usuario
        self.venta_id = 1
        self.total = 0.0
        self.cantidad_seleccionada = 1
        self.lista_filas = [0]  # Incluye encabezado

        # Campo de entrada para código de barras
        frame_entrada = ttk.Frame(self)
        frame_entrada.pack(pady=10)

        ttk.Label(frame_entrada, text="Código de Barras", bootstyle="inverse").pack(side=tk.LEFT)
        self.codigo_barras = ttk.Entry(frame_entrada, width=30, font=("Arial", 14))
        self.codigo_barras.pack(side=tk.LEFT, padx=5)
        self.codigo_barras.bind("<Return>", lambda e: self.agregar_producto())
        self.codigo_barras.bind("<Key>", self.detectar_teclas)  # Detecta 'x' para cantidad
        self.codigo_barras.focus_set()

        # Tabla de productos (con scroll)
        frame_tabla = ttk.Frame(self)
        frame_tabla.pack(pady=10, fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(frame_tabla)
        scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=canvas.yview)
        self.frame_lista = ttk.Frame(canvas)

        self.frame_lista.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.frame_lista, anchor="nw", width=760)
        canvas.configure(yscrollcommand=scrollbar_y.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

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

        self.lista_filas = [0]  # Reiniciar filas

        # Total y botones
        frame_acciones = ttk.Frame(self)
        frame_acciones.pack(pady=10)

        self.lbl_total = ttk.Label(frame_acciones, text="Total: $0.00", bootstyle="light", font=("Arial", 16))
        self.lbl_total.grid(row=0, column=0, padx=20)

        self.btn_finalizar = ttk.Button(
            frame_acciones,
            text="Finalizar Venta (T)",
            width=20,
            command=self.finalizar_venta,
            bootstyle="success"
        )
        self.btn_finalizar.grid(row=0, column=1, padx=10)

        ttk.Button(
            frame_acciones,
            text="Cancelar Venta (Esc)",
            width=20,
            command=self.cancelar_venta,
            bootstyle="danger"
        ).grid(row=0, column=2, padx=10)

        # Atajos globales
        self.root = master.winfo_toplevel()
        self.root.bind("<t>", lambda e: self.finalizar_venta())
        self.root.bind("<Escape>", lambda e: self.cancelar_venta())

    def detectar_teclas(self, event):
        """Detecta si se presiona 'x' para ingresar cantidad"""
        if event.char.lower() == 'x':
            self.pedir_cantidad()
            self.codigo_barras.delete(0, tk.END)
            return "break"

    def pedir_cantidad(self):
        """Ventana emergente para ingresar cantidad"""
        try:
            cantidad = simpledialog.askinteger(
                "Ingresar Cantidad",
                "¿Cuántas unidades desea cargar?",
                minvalue=1,
                maxvalue=999
            )
            if cantidad:
                self.cantidad_seleccionada = cantidad
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener la cantidad:\n{e}")

    def agregar_producto(self, event=None):
        codigo = self.codigo_barras.get().strip()
        if not codigo or codigo.lower() == 'x':
            return

        from controllers.venta_controller import agregar_producto_a_venta

        producto = agregar_producto_a_venta(self.venta_id, codigo, self.cantidad_seleccionada)

        if producto and 'nombre' in producto and 'precio' in producto:
            precio_unitario = float(producto['precio'])
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
            messagebox.showerror("Producto no encontrado", f"El producto con código '{codigo}' no existe.")
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
            messagebox.showinfo("Pago", "Venta cerrada. Pago en efectivo.")
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

            ttk.Button(
                ventana_qr, 
                text="Cerrar", 
                command=ventana_qr.destroy, 
                bootstyle="secondary"
            ).pack(pady=10)

            # Abre automáticamente el link en navegador (opcional)
            """import webbrowser
            webbrowser.open_new(init_point)""" #comento esto xq no quiero que abra el navegador
        else:
            from tkinter import messagebox
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