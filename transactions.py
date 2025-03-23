import ecdsa
import hashlib
import json

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount
        }

    def sign_transaction(self, private_key_hex):
        private_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)
        message = json.dumps(self.to_dict(), sort_keys=True).encode()
        signature = private_key.sign(message)
        return signature.hex()

if __name__ == "__main__":
    sender = "1ABCxyz..."
    recipient = "1DEFuvw..."
    amount = 10

    tx = Transaction(sender, recipient, amount)
    print("Транзакция:", tx.to_dict())