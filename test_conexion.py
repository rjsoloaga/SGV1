from config_db import conectar

def test_conexion():
    conn = conectar()
    if conn:
        print("✅ Conexión exitosa")
        conn.close()
    else:
        print("❌ No se pudo conectar a la base de datos")

if __name__ == "__main__":
    test_conexion()