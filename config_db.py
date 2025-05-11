# config_db.py

from dotenv import load_dotenv
import os
import mysql.connector
from tkinter import messagebox


load_dotenv()  # Cargamos las variables del .env


def conectar():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT", "3306"),  # Opcional, por defecto 3306
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        print("✅ Conexión exitosa a la base de datos")
        return conn
    except Exception as e:
        print(f"❌ Error al conectar a la BD: {e}")
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos:\n{e}")
        return None