from flask import Flask ,render_template, jsonify
import Crypto
import Crypto.Random
import binascii
from Crypto.PublicKey import RSA



class Tarnsaction:
    def __init__ (self,sender_address,sender_private_key,receipient_address,value):
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.receipient_address = receipient_address
        self.value = value



app = Flask(__name__)

@app.route("/")
def index():
    return render_template ('./index.html')

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
    parser.add_argument('-p','--port',default=8081,type=int)
    args = parser.parse_args()
    port = args.port
    app.run(host='127.0.0.1',port=port,debug=True)