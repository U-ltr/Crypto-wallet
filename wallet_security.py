from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import base64
import os

# Длина ключа AES-256
KEY_LENGTH = 32
SALT_SIZE = 16
IV_SIZE = AES.block_size

def generate_key(password: str, salt: bytes) -> bytes:
    """ Генерирует ключ на основе пароля с использованием PBKDF2. """
    return PBKDF2(password, salt, dkLen=KEY_LENGTH)

def encrypt_key(private_key: str, password: str) -> str:
    """ Шифрует приватный ключ с использованием AES. """
    salt = os.urandom(SALT_SIZE)  # Генерируем соль
    key = generate_key(password, salt)

    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv  # Вектор инициализации

    # Дополняем ключ до кратного 16 байт
    private_key_bytes = private_key.encode()
    padded_private_key = private_key_bytes + b" " * (16 - len(private_key_bytes) % 16)

    encrypted_bytes = cipher.encrypt(padded_private_key)
    encrypted_data = salt + iv + encrypted_bytes  # Объединяем все данные

    return base64.b64encode(encrypted_data).decode()

def decrypt_key(encrypted_key: str, password: str) -> str:
    """ Расшифровывает приватный ключ. """
    encrypted_data = base64.b64decode(encrypted_key)

    salt = encrypted_data[:SALT_SIZE]
    iv = encrypted_data[SALT_SIZE:SALT_SIZE + IV_SIZE]
    encrypted_bytes = encrypted_data[SALT_SIZE + IV_SIZE:]

    key = generate_key(password, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted_bytes = cipher.decrypt(encrypted_bytes)
    return decrypted_bytes.strip().decode()

if __name__ == "__main__":
    private_key = "my_super_secret_key_123456"
    password = "mypassword"

    encrypted = encrypt_key(private_key, password)
    print(f"Зашифровано: {encrypted}")

    decrypted = decrypt_key(encrypted, password)
    print(f"Расшифровано: {decrypted}")
