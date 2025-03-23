from flask import Flask, jsonify
from wallet import Wallet

app = Flask(__name__)

wallet = Wallet()

@app.route("/wallet", methods=["GET"])
def get_wallet():
    return jsonify({
        "private_key": wallet.get_private_key_hex(),
        "public_key": wallet.get_public_key_hex(),
        "address": wallet.get_address()
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)