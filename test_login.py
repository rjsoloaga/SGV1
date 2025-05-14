# test_login.py

from models.usuario import validar_credenciales

def probar_login(usuario, clave):
    resultado = validar_credenciales(usuario, clave)
    if resultado:
        print("✅ Credenciales válidas:", resultado['nombre'])
    else:
        print("❌ Credenciales inválidas")

probar_login("admin", "admin")