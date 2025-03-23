import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QInputDialog
)
from wallet import Wallet
from balance import CryptoBalance
from send_transaction import CryptoTransaction

class WalletApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Крипто-кошелек")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Поля для кошелька
        self.wallet_label = QLabel("Адрес: -")
        self.private_key_label = QLabel("Приватный ключ: -")
        self.generate_wallet_btn = QPushButton("Создать кошелек")
        self.generate_wallet_btn.clicked.connect(self.generate_wallet)

        # Поля для проверки баланса
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Введите адрес для проверки баланса")
        self.check_balance_btn = QPushButton("Проверить баланс")
        self.check_balance_btn.clicked.connect(self.check_balance)
        self.balance_label = QLabel("Баланс: 0 BTC")

        # Поля для отправки транзакций
        self.send_tx_btn = QPushButton("Отправить транзакцию")
        self.send_tx_btn.clicked.connect(self.send_transaction)

        # Добавляем все элементы на экран
        layout.addWidget(self.wallet_label)
        layout.addWidget(self.private_key_label)
        layout.addWidget(self.generate_wallet_btn)
        layout.addWidget(self.address_input)
        layout.addWidget(self.check_balance_btn)
        layout.addWidget(self.balance_label)
        layout.addWidget(self.send_tx_btn)

        self.setLayout(layout)

    def generate_wallet(self):
        """Генерируем новый кошелек и отображаем адрес"""
        wallet = Wallet()
        self.wallet_label.setText(f"Адрес: {wallet.address}")
        self.private_key_label.setText(f"Приватный ключ: {wallet.private_key}")

    def check_balance(self):
        """Получаем баланс по введенному адресу"""
        address = self.address_input.text()
        if address:
            wallet = CryptoBalance(address)
            balance = wallet.get_balance()
            self.balance_label.setText(f"Баланс: {balance} BTC")
        else:
            QMessageBox.warning(self, "Ошибка", "Введите адрес кошелька!")

    def send_transaction(self):
        """Отправка транзакции в Testnet"""
        raw_tx, ok = QInputDialog.getText(self, "Отправить транзакцию", "Введите сырую транзакцию:")
        if ok and raw_tx:
            result = CryptoTransaction.send_raw_transaction(raw_tx)
            QMessageBox.information(self, "Результат", result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WalletApp()
    window.show()
    sys.exit(app.exec())
