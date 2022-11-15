from flask import Flask ,render_template




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
    return " "