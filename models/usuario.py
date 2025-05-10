from config_db import conectar
import bcrypt

def registrar_usuario(nombre, username, password, rol):
    conn = conectar()
    if not conn:
        return False

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO usuarios (nombre, username, password, rol)
            VALUES (%s, %s, %s, %s)
        """, (nombre, username, hashed.decode('utf-8'), rol))
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ Error al registrar usuario: {e}")
        return False
    finally:
        conn.close()


def obtener_todos_los_usuarios():
    conn = conectar()
    if not conn:
        return []

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios


# 👇 Esta es la función que faltaba
def obtener_usuario_por_username(username):
    conn = conectar()
    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def validar_credenciales(usuario, clave):
    """
    Valida las credenciales contra la tabla usuarios
    Devuelve los datos del usuario si son válidas
    """
    conn = conectar()
    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT * FROM usuarios 
            WHERE username = %s AND password = SHA2(%s, 256)
        """
        cursor.execute(query, (usuario, clave))
        resultado = cursor.fetchone()
        return resultado
    except Exception as e:
        print(f"❌ Error al validar credenciales: {e}")
        return None
    finally:
        conn.close()