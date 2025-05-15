# models/venta.py

from config_db import conectar
from datetime import datetime


def crear_venta(usuario_id):
    conn = conectar()
    if not conn:
        return None

    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO ventas (id_usuario, total)
            VALUES (%s, %s)
        """, (usuario_id, 0.00))

        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"❌ Error al crear venta: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()


def registrar_detalle_venta(conn, venta_id, producto, cantidad, precio_unitario, subtotal):
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


def devolver_stock(codigo_barras, cantidad):
    """Devuelve stock cuando se elimina un producto antes de cerrar la venta"""
    conn = conectar()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE productos SET stock = stock + %s WHERE codigo_barras = %s",
                       (cantidad, codigo_barras))
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ Error al devolver stock: {e}")
        return False
    finally:
        conn.close()


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