from web3 import Web3
import json
from wallet_security import decrypt_key

# Подключение к Ethereum Testnet (Sepolia)
INFURA_URL = "https://sepolia.infura.io/v3/f420c33f830c4bc5b2aee035b36152ec"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Проверка подключения
if web3.is_connected():
    print("Успешно подключились к Testnet")
else:
    print("Ошибка подключения к сети")

# Загружаем зашифрованный приватный ключ
PASSWORD = "strongpassword123"

with open("encrypted_wallet.json", "r") as f:
    data = json.load(f)

private_key = decrypt_key(data["encrypted_key"], PASSWORD)

# Адрес кошелька
wallet_address = web3.eth.account.from_key(private_key).address
print(f"Кошелек: {wallet_address}")

# Проверяем баланс
balance = web3.eth.get_balance(wallet_address)
print(f"Баланс: {web3.from_wei(balance, 'ether')} ETH")

# Адрес получателя (например, другой кошелек Testnet)
receiver = "0xRecipientAddressHere"

# Создаем транзакцию
tx = {
    "nonce": web3.eth.get_transaction_count(wallet_address),
    "to": receiver,
    "value": web3.to_wei(0.01, "ether"),
    "gas": 21000,
    "gasPrice": web3.to_wei(10, "gwei"),
    "chainId": 11155111  # Sepolia Testnet
}

# Подписываем транзакцию
signed_tx = web3.eth.account.sign_transaction(tx, private_key)

# Отправляем транзакцию
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(f"Транзакция отправлена! Hash: {web3.to_hex(tx_hash)}")