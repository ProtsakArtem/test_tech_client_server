from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Генерація приватного ключа
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Збереження приватного ключа
with open("server_private_key.pem", "wb") as key_file:
    key_file.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Генерація публічного ключа
public_key = private_key.public_key()

# Збереження публічного ключа
with open("server_public_key.pem", "wb") as key_file:
    key_file.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))
