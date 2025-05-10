import bcrypt

password = input("Ingresa la contraseña para hashear: ").encode('utf-8')
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

print("\nHash generado:\n")
print(hashed.decode())