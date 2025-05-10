# config_db.py

from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

def conectar():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT", "3306"),  # Agregado
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if conn.is_connected():
            print("✅ Conexión exitosa a la base de datos")
        return conn
    except Exception as e:
        print(f"❌ Error al conectar a la BD: {e}")
        return None