# config_db.py

from dotenv import load_dotenv
import os
import mysql.connector
from tkinter import messagebox


load_dotenv() # Aca cargamos las las credenciales del archivo .env


def conectar():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT", 3306),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return conn
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos:\n{e}")
        return None