# models/caja_model.py

from config_db import conectar


def obtener_resumen_caja():
    conn = conectar()
    if not conn:
        return {
            "total": 0.0,
            "ventas_totales": 0,
            "efectivo": 0.0,
            "mercado_pago": 0.0
        }

    cursor = conn.cursor(dictionary=True)

    try:
        # Cantidad y total del día
        cursor.execute("""
            SELECT 
                SUM(total) AS total_dia,
                COUNT(*) AS ventas_totales
            FROM ventas
            WHERE DATE(fecha_venta) = CURDATE()
        """)
        ventas_diarias = cursor.fetchone()

        # Ventas en efectivo
        cursor.execute("""
            SELECT 
                SUM(total) AS efectivo_total
            FROM ventas
            WHERE metodo_pago = 'efectivo' AND DATE(fecha_venta) = CURDATE()
        """)
        pagos_efectivo = cursor.fetchone()

        # Ventas por Mercado Pago
        cursor.execute("""
            SELECT 
                SUM(total) AS mp_total
            FROM ventas
            WHERE metodo_pago = 'mercado_pago' AND DATE(fecha_venta) = CURDATE()
        """)
        pagos_mp = cursor.fetchone()

        return {
            "total": float(ventas_diarias.get("total_dia", 0) or 0),
            "ventas_totales": ventas_diarias.get("ventas_totales", 0),
            "efectivo": float(pagos_efectivo.get("efectivo_total", 0) or 0),
            "mercado_pago": float(pagos_mp.get("mp_total", 0) or 0)
        }
    finally:
        conn.close()