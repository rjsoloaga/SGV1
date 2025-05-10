# models/producto.py

from config_db import conectar


def obtener_producto_por_codigo(codigo_barras):
    conn = conectar()
    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM productos WHERE codigo_barras = %s", (codigo_barras,))
        return cursor.fetchone()
    except Exception as e:
        print(f"❌ Error al buscar producto: {e}")
        return None
    finally:
        conn.close()