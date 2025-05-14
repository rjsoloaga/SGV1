import bcrypt

# Usuarios y contraseñas predefinidos (sin input)
usuarios = {
    "root": "root",
    "admin": "admin"
}

print("\n=== GENERADOR DE HASHES (BCRYPT) ===")
print("=== Usuarios y contraseñas predefinidos ===\n")

# Generar hashes
for username, password in usuarios.items():
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    print(f"Usuario: {username}")
    print(f"Hash:    {hashed}\n")

# SQL listo para copiar
print("=== SQL PARA INSERTAR ===")
print("INSERT INTO tu_tabla (nombre, username, password, rol) VALUES")
for username, password in usuarios.items():
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    print(f"    ('Javier', '{username}', '{hashed}', 'admin'),")
print(";")