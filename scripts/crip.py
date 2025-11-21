from passlib.context import CryptContext

# Cambiamos bcrypt por pbkdf2_sha256
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

password = "123"
hashed = pwd_context.hash(password)
print("Hash generado:", hashed)
print("Verificación:", pwd_context.verify(password, hashed))
