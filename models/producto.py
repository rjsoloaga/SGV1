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
    finally:
        conn.close()

def guardar_producto(producto):
    conn = conectar()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE productos 
            SET nombre = %s, categoria = %s, descripcion = %s, precio = %s, stock = %s 
            WHERE codigo_barras = %s
        """, (
            producto['nombre'], producto['categoria'], producto['descripcion'],
            producto['precio'], producto['stock'], producto['codigo_barras']
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ Error al guardar producto: {e}")
        return False
    finally:
        conn.close()