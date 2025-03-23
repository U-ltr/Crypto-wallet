import requests

class CryptoTransaction:
    BROADCAST_API = "https://blockstream.info/testnet/api/tx"

    @staticmethod
    def send_raw_transaction(raw_tx):
        """Отправка сырой транзакции в блокчейн Testnet"""
        try:
            response = requests.post(CryptoTransaction.BROADCAST_API, data=raw_tx)
            if response.status_code == 200:
                return f"Транзакция отправлена: {response.text}"
            else:
                return f"Ошибка: {response.text}"
        except Exception as e:
            return f"Ошибка: {e}"

# Пример использования
if __name__ == "__main__":
    raw_tx = "0200000001abcdef..."  # Здесь должна быть реальная подписанная транзакция(пока хз где взять)
    result = CryptoTransaction.send_raw_transaction(raw_tx)
    print(result)