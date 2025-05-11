# models/venta.py

import random
import time
from config_db import conectar
from datetime import datetime

def registrar_venta(id_usuario):
    conn = conectar()
    if not conn:
        return None

    cursor = conn.cursor()
    try:
        fecha_venta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            INSERT INTO ventas (fecha_venta, total, id_usuario)
            VALUES (%s, 0.0, %s)
        """, (fecha_venta, id_usuario))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"❌ Error al registrar venta: {e}")
        return None
    finally:
        conn.close()


def actualizar_total_venta(venta_id, subtotal):
    conn = conectar()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE ventas SET total = total + %s WHERE id_venta = %s",
                       (float(subtotal), venta_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ Error al actualizar total: {e}")
        return False
    finally:
        conn.close()

def registrar_detalle_venta(conn, venta_id, producto, cantidad, precio_unitario, subtotal):
    """
    Registra un producto en el detalle_venta
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO detalle_venta 
            (id_venta, codigo_barras, cantidad, precio_unitario, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """, (venta_id, producto['codigo_barras'], cantidad, precio_unitario, subtotal))
        return True
    except Exception as e:
        print(f"❌ Error al registrar detalle_venta: {e}")
        return False
    
def marcar_venta_como_pagada(venta_id):
    conn = conectar()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE ventas 
            SET metodo_pago = 'Mercado Pago', estado_pago = 'pagado'
            WHERE id_venta = %s
        """, (venta_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ Error al marcar como pagado: {e}")
        return False
    finally:
        conn.close()

def actualizar_estado_venta(venta_id, estado_pago, metodo_pago):
    """
    En producción actualiza la BD con el nuevo estado de pago
    Aquí simulamos o mostramos mensaje en consola
    """
    print(f"✔️ Venta #{venta_id} actualizada a '{estado_pago}'")
    # Aquí puedes guardar en MySQL si ya tenés conexión hecha

def verificar_estado_pago(venta_id):
    """
    En producción usarías Webhooks o polling a la API de MP
    Aquí simulamos que el pago llegó después de un tiempo
    """
    print(f"🔍 Verificando pago de venta #{venta_id}...")
    time.sleep(5)  # Simula espera de 5 segundos
    return "aprobado"  # Simulación de pago recibido