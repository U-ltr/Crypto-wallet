import ecdsa
import hashlib
import base58
import os
import json
from wallet_security import encrypt_key, decrypt_key

PASSWORD = "strongpassword123"

# Генерируем приватный ключ ( это все можно брать напрямую от пользователя или генерить)
private_key = "0xabcdef1234567890"

# Шифруем и сохраняем
encrypted_key = encrypt_key(private_key, PASSWORD)
with open("encrypted_wallet.json", "w") as f:
    json.dump({"encrypted_key": encrypted_key}, f)
print(" Приватный ключ зашифрован и сохранен.")

# Расшифровываем из файла
with open("encrypted_wallet.json", "r") as f:
    data = json.load(f)
decrypted_key = decrypt_key(data["encrypted_key"], PASSWORD)
print("Расшифрованный ключ:", decrypted_key)

class Wallet:
    def __init__(self):
        # Генерация приватного ключа
        self.private_key = os.urandom(32)
        self.public_key = self.generate_public_key()
        self.address = self.generate_address()

    def generate_public_key(self):
        sk = ecdsa.SigningKey.from_string(self.private_key, curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        return vk.to_string()

    def generate_address(self):
        sha256_bpk = hashlib.sha256(self.public_key).digest()
        ripemd160_bpk = hashlib.new('ripemd160', sha256_bpk).digest()
        network_byte = b'\x00' + ripemd160_bpk
        checksum = hashlib.sha256(hashlib.sha256(network_byte).digest()).digest()[:4]
        return base58.b58encode(network_byte + checksum).decode()

    def get_private_key_hex(self):
        return self.private_key.hex()

    def get_public_key_hex(self):
        return self.public_key.hex()

    def get_address(self):
        return self.address


if __name__ == "__main__":
    wallet = Wallet()
    private_key = wallet.get_private_key_hex()
    encrypted_key = encrypt_key(private_key, PASSWORD)

    with open("encrypted_wallet.json", "w") as f:
        json.dump({"encrypted_key": encrypted_key}, f)

    print("Приватный ключ сохранён!")
    print("Адрес:", wallet.get_address())

#if __name__ == "__main__":
#    wallet = Wallet()
#    print("Приватный ключ:", wallet.get_private_key_hex())
#    print("Публичный ключ:", wallet.get_public_key_hex())
#    print("Адрес кошелька:", wallet.get_address())
