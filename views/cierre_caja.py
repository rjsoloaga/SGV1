# views/cierre_caja.py

import tkinter as tk
from ttkbootstrap import ttk
from tkinter import messagebox
from models.caja_model import obtener_resumen_caja


class VentanaCierreCaja(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)

        # Cargar datos del día
        self.resumen = obtener_resumen_caja()
        self.efectivo_sistema = self.resumen['efectivo']
        self.mp_sistema = self.resumen['mercado_pago']
        self.total_sistema = self.resumen['total']
        self.ventas_totales = self.resumen['ventas_totales']

        # Título
        ttk.Label(self, text="Cierre de Caja", bootstyle="inverse", font=("Arial", 16)).pack(pady=20)

        # Datos del sistema
        frame_datos = ttk.Frame(self)
        frame_datos.pack(padx=20, pady=10)

        ttk.Label(frame_datos, text="Ventas del Día:", width=25, anchor='w').grid(row=0, column=0, sticky='w')
        ttk.Label(frame_datos, text=f"${self.total_sistema:.2f}", width=20, anchor='e').grid(row=0, column=1, sticky='e')

        ttk.Label(frame_datos, text="En Efectivo:", width=25, anchor='w').grid(row=1, column=0, sticky='w')
        ttk.Label(frame_datos, text=f"${self.efectivo_sistema:.2f}", width=20, anchor='e').grid(row=1, column=1, sticky='e')

        ttk.Label(frame_datos, text="Mercado Pago:", width=25, anchor='w').grid(row=2, column=0, sticky='w')
        ttk.Label(frame_datos, text=f"${self.mp_sistema:.2f}", width=20, anchor='e').grid(row=2, column=1, sticky='e')

        ttk.Label(frame_datos, text="Cantidad de Ventas:", width=25, anchor='w').grid(row=3, column=0, sticky='w')
        ttk.Label(frame_datos, text=self.ventas_totales, width=20, anchor='e').grid(row=3, column=1, sticky='e')

        # Ingreso manual de efectivo
        frame_ingreso = ttk.Frame(self)
        frame_ingreso.pack(pady=20)

        ttk.Label(frame_ingreso, text="Efectivo Físico en Caja ($)", width=25, anchor='w').pack(side=tk.LEFT, padx=10)
        self.entry_efectivo = ttk.Entry(frame_ingreso, width=15)
        self.entry_efectivo.pack(side=tk.LEFT, padx=5)

        ttk.Button(
            frame_ingreso,
            text="Calcular Diferencia",
            command=self.calcular_diferencia,
            bootstyle="primary"
        ).pack(side=tk.RIGHT, padx=10)

        # Resultado final
        self.lbl_resultado = ttk.Label(self, text="", bootstyle="light")
        self.lbl_resultado.pack(pady=10)

    def calcular_diferencia(self):
        try:
            efectivo_fisico = float(self.entry_efectivo.get() or 0.0)
        except ValueError:
            messagebox.showerror("Error", "Ingrese solo números válidos.")
            return

        diferencia = round(efectivo_fisico - self.efectivo_sistema, 2)
        mensaje = f"""
        Total Sistema:   ${self.total_sistema:.2f}
        Efectivo Físico: ${efectivo_fisico:.2f}
        Efectivo Sistema: ${self.efectivo_sistema:.2f}
        
        Diferencia:      ${diferencia:.2f}
        """

        if diferencia < 0:
            mensaje += "\n⚠️ ¡Falta dinero en caja!"
        elif diferencia > 0:
            mensaje += "\n💡 Hay más efectivo del registrado."
        else:
            mensaje += "\n✅ Todo coincide."

        self.lbl_resultado.config(text=mensaje)

    def cerrar_sesion(self):
        self.master.destroy()
        from views.login import VentanaLogin
        VentanaLogin(tk.Toplevel(), self.usuario)