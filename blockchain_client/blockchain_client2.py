from flask import Flask ,render_template, jsonify,request
import Crypto
import Crypto.Random
import binascii
from Crypto.PublicKey import RSA
from collections import OrderedDict
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA

class Transaction:
    def __init__ (self,sender_public_key,sender_private_key,recipient_public_key,amount):
        self.sender_public_key = sender_public_key
        self.sender_private_key = sender_private_key
        self.recipient_public_key = recipient_public_key
        self.amount = amount
    def to_dict(self):
        return OrderedDict({
            'sender_public_key':self.sender_public_key,
            'sender_private_key':self.sender_private_key,
            'recipient_public_key':self.recipient_public_key,
            'amount':self.amount

        })
    def sign_transaction(self):
        """
        Sign transaction with private key
        """
        private_key = RSA.importKey(binascii.unhexlify(self.sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template ('./index.html')

@app.route("/generate/transaction",methods=['POST'])
def generate_transaction():
	
	sender_address = request.form['sender_address']
	sender_private_key = request.form['sender_private_key']
	recipient_address = request.form['recipient_address']
	value = request.form['amount']

	transaction = Transaction(sender_address, sender_private_key, recipient_address, value)

	response = {'transaction': transaction.to_dict(), 'signature': transaction.sign_transaction()}

	return jsonify(response), 200

@app.route("/make/transaction")
def make_transaction():
    return render_template ('./make_transaction.html')

@app.route("/view/transaction")
def view_transaction():
    return render_template ('./view_transaction.html')

@app.route("/wallet/new")
def new_wallet():
    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(1024,random_gen)
    public_key = private_key.public_key()
    respons= {
        'private_key':binascii.hexlify(private_key.export_key(format('DER'))).decode('ascii'),
        'public_key':binascii.hexlify(public_key.export_key(format('DER'))).decode('ascii')
    }
    return jsonify(respons)



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p','--port',type=int)
    args = parser.parse_args()
    port = args.port
    app.run(host='127.0.0.1',port=8080,debug=True)