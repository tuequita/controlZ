from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password = "123"[:72]  # siempre truncar a 72 bytes
hashed = pwd_context.hash(password)
print("Hash generado:", hashed)
