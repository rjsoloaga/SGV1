# views/cierre_caja.py

import tkinter as tk
from ttkbootstrap import ttk
from models.caja_model import obtener_resumen_caja


class VentanaCierreCaja(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)

        resumen = obtener_resumen_caja()

        ttk.Label(self, text="Cierre de Caja", bootstyle="inverse", font=("Arial", 16)).pack(pady=20)

        frame_datos = ttk.Frame(self)
        frame_datos.pack(padx=20, pady=10)

        ttk.Label(frame_datos, text="Ventas del Día:", width=25, anchor='w').grid(row=0, column=0, sticky='w')
        ttk.Label(frame_datos, text=f"${resumen['total']:.2f}", width=20, anchor='e').grid(row=0, column=1, sticky='e')

        ttk.Label(frame_datos, text="En Efectivo:", width=25, anchor='w').grid(row=1, column=0, sticky='w')
        ttk.Label(frame_datos, text=f"${resumen['efectivo']:.2f}", width=20, anchor='e').grid(row=1, column=1, sticky='e')

        ttk.Label(frame_datos, text="Mercado Pago:", width=25, anchor='w').grid(row=2, column=0, sticky='w')
        ttk.Label(frame_datos, text=f"${resumen['mercado_pago']:.2f}", width=20, anchor='e').grid(row=2, column=1, sticky='e')

        ttk.Label(frame_datos, text="Cantidad de Ventas:", width=25, anchor='w').grid(row=3, column=0, sticky='w')
        ttk.Label(frame_datos, text=resumen['ventas_totales'], width=20, anchor='e').grid(row=3, column=1, sticky='e')

        ttk.Button(
            self,
            text="Cerrar Sesión",
            command=self.cerrar_sesion,
            bootstyle="danger"
        ).pack(pady=10)

    def cerrar_sesion(self):
        self.master.destroy()
        from views.login import VentanaLogin
        VentanaLogin(tk.Toplevel(), self.usuario)