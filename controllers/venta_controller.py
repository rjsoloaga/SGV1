# controllers/venta_controller.py

from models.producto import obtener_producto_por_codigo
from models.venta import registrar_detalle_venta
from config_db import conectar
import mercadopago
from config_mp import ACCESS_TOKEN
from tkinter import messagebox


def agregar_producto_a_venta(venta_id, codigo_barras, cantidad=1):
    conn = conectar()
    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM productos WHERE codigo_barras = %s", (codigo_barras,))
        producto = cursor.fetchone()

        if not producto:
            messagebox.showerror("Error", f"Producto {codigo_barras} no encontrado")
            return None

        precio_unitario = float(producto['precio'])

        if producto['stock'] < cantidad:
            messagebox.showwarning("Stock insuficiente", f"No hay suficientes unidades de {producto['nombre']}.")
            return None

        subtotal = precio_unitario * cantidad

        cursor.execute("UPDATE productos SET stock = stock - %s WHERE codigo_barras = %s",
                       (cantidad, codigo_barras))

        registrar_detalle_venta(conn, venta_id, producto, cantidad, precio_unitario, subtotal)
        actualizar_total_venta(venta_id, subtotal)  # Actualiza el total en BD
        conn.commit()
        return producto
    except Exception as e:
        print(f"❌ Error al procesar producto: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def generar_pago_mercadopago(total, venta_id):
    if total <= 0:
        return None

    sdk = mercadopago.SDK(ACCESS_TOKEN)

    preference_data = {
        "items": [
            {
                "title": f"Venta #{venta_id}",
                "quantity": 1,
                "unit_price": float(total),
                "currency_id": "ARS"
            }
        ],
        "purpose": "wallet_purchase",
        "external_reference": f"{venta_id}_{int(total * 100)}",
        "back_urls": {
            "success": "https://tu-sistema.com/pago-exitoso ",
            "failure": "https://tu-sistema.com/pago-fallido ",
            "pending": "https://tu-sistema.com/pago-pendiente "
        },
        "auto_return": "approved",
        "binary_mode": True
    }

    try:
        response = sdk.preference().create(preference_data)
        preference = response.get("response", {})
        init_point = preference.get("init_point")
        return init_point
    except Exception as e:
        print(f"❌ Error al crear pago en MP: {e}")
        return None