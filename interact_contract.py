from web3 import Web3
import json
from wallet_security import decrypt_key

# Подключение к Ethereum Testnet
INFURA_URL = "https://sepolia.infura.io/v3/f420c33f830c4bc5b2aee035b36152ec"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Загружаем контракт
with open("deployed_contract.json", "r") as f:
    contract_data = json.load(f)

contract_address = contract_data["contract_address"]
abi = contract_data["abi"]

contract = web3.eth.contract(address=contract_address, abi=abi)

# Загружаем приватный ключ
PASSWORD = "strongpassword123"
with open("encrypted_wallet.json", "r") as f:
    data = json.load(f)

private_key = decrypt_key(data["encrypted_key"], PASSWORD)
wallet_address = web3.eth.account.from_key(private_key).address

# Читаем данные из контракта
stored_value = contract.functions.get().call()
print(f"Хранимое значение: {stored_value}")

# Отправляем новую транзакцию (изменяем значение)
new_value = 42
nonce = web3.eth.get_transaction_count(wallet_address)

tx = contract.functions.set(new_value).build_transaction(
    {"from": wallet_address, "nonce": nonce, "gas": 200000, "gasPrice": web3.to_wei(10, "gwei")}
)

# Подписываем и отправляем
signed_tx = web3.eth.account.sign_transaction(tx, private_key)
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

print(f"Значение обновлено! Hash: {web3.to_hex(tx_hash)}")

# Проверяем новое значение
stored_value = contract.functions.get().call()
print(f"Новое значение: {stored_value}")