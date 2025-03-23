from web3 import Web3
import json
from wallet_security import decrypt_key

# Подключение к Ethereum Testnet
INFURA_URL = "https://sepolia.infura.io/v3/f420c33f830c4bc5b2aee035b36152ec"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Загружаем контракт
with open("compiled_contract.json", "r") as f:
    contract_data = json.load(f)

abi = contract_data["abi"]
bytecode = contract_data["bytecode"]

# Загружаем приватный ключ
PASSWORD = "strongpassword123"
with open("encrypted_wallet.json", "r") as f:
    data = json.load(f)

private_key = decrypt_key(data["encrypted_key"], PASSWORD)
wallet_address = web3.eth.account.from_key(private_key).address


# Создаем транзакцию для развертывания
SimpleStorage = web3.eth.contract(abi=abi, bytecode=bytecode)
nonce = web3.eth.get_transaction_count(wallet_address)

tx = SimpleStorage.constructor().build_transaction(
    {"from": wallet_address, "nonce": nonce, "gas": 2000000, "gasPrice": web3.to_wei(10, "gwei")}
)

# Подписываем и отправляем
signed_tx = web3.eth.account.sign_transaction(tx, private_key)
tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)


print(f"Контракт отправлен! Hash: {web3.to_hex(tx_hash)}")

# Ждем подтверждения
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress
print(f"Контракт развернут: {contract_address}")

# Сохраняем адрес контракта
with open("deployed_contract.json", "w") as f:
    json.dump({"contract_address": contract_address, "abi": abi}, f)