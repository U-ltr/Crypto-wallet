import requests

class CryptoBalance:
    API_URL = "https://blockstream.info/testnet/api/address/"

    def __init__(self, address):
        self.address = address

    def get_balance(self):
        """Получает баланс кошелька в сети Testnet"""
        try:
            response = requests.get(self.API_URL + self.address)
            if response.status_code == 200:
                data = response.json()
                balance = data.get("chain_stats", {}).get("funded_txo_sum", 0)
                return balance / 100_000_000  # Переводим сатоши в BTC
            else:
                return "Ошибка при получении баланса"
        except Exception as e:
            return f"Ошибка: {e}"

# Пример использования
if __name__ == "__main__":
    test_address = "tb1qexampletestaddress..."  # ( пока думаю где лучше взять тестовый адресс)
    wallet = CryptoBalance(test_address)
    print(f"Баланс: {wallet.get_balance()} BTC")