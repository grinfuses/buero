from flask import Flask, render_template, request, jsonify, session
from .wallet import Wallet
from .wallet_manager import WalletManager
from ..blockchain.blockchain import Blockchain
import json
import time

app = Flask(__name__)
app.secret_key = 'buero_secret_key'  # Necesario para manejar sesiones
blockchain = Blockchain()
wallet_manager = WalletManager()

@app.route('/')
def index():
    if 'wallet_address' not in session:
        # Crear una nueva cartera para esta sesión
        wallet = wallet_manager.create_wallet()
        session['wallet_address'] = wallet.address
        session.modified = True
    return render_template('index.html')

@app.route('/api/balance')
def get_balance():
    if 'wallet_address' not in session:
        return jsonify({'error': 'No wallet selected'}), 400
    
    wallet = wallet_manager.get_wallet(session['wallet_address'])
    if not wallet:
        return jsonify({'error': 'Wallet not found'}), 404
    
    balance = wallet.get_balance(blockchain)
    return jsonify({
        'balance': balance,
        'address': wallet.address
    })

@app.route('/api/send', methods=['POST'])
def send_transaction():
    if 'wallet_address' not in session:
        return jsonify({'error': 'No wallet selected'}), 400
    
    wallet = wallet_manager.get_wallet(session['wallet_address'])
    if not wallet:
        return jsonify({'error': 'Wallet not found'}), 404
    
    data = request.get_json()
    recipient = data.get('recipient')
    amount = float(data.get('amount'))
    
    if not recipient or amount <= 0:
        return jsonify({'error': 'Invalid transaction data'}), 400
    
    success = wallet.send_transaction(recipient, amount, blockchain)
    if success:
        return jsonify({'message': 'Transaction sent successfully'})
    else:
        return jsonify({'error': 'Insufficient funds'}), 400

@app.route('/api/mine', methods=['POST'])
def mine():
    if 'wallet_address' not in session:
        return jsonify({'error': 'No wallet selected'}), 400
    
    wallet = wallet_manager.get_wallet(session['wallet_address'])
    if not wallet:
        return jsonify({'error': 'Wallet not found'}), 404
    
    # Crear una nueva transacción de recompensa
    reward_tx = {
        'sender': "0",  # Dirección especial para recompensas de minado
        'recipient': wallet.address,
        'amount': 10.0,
        'timestamp': time.time()
    }
    
    # Minar el bloque
    blockchain.mine_pending_transactions(wallet.address)
    return jsonify({'message': 'Block mined successfully'})

@app.route('/api/chain')
def get_chain():
    return jsonify(blockchain.chain)

@app.route('/api/wallets')
def list_wallets():
    return jsonify(wallet_manager.list_wallets(blockchain))

@app.route('/api/wallet/select', methods=['POST'])
def select_wallet():
    data = request.get_json()
    address = data.get('address')
    
    if not address:
        return jsonify({'error': 'No address provided'}), 400
    
    wallet = wallet_manager.get_wallet(address)
    if not wallet:
        return jsonify({'error': 'Wallet not found'}), 404
    
    session['wallet_address'] = address
    session.modified = True
    return jsonify({
        'message': 'Wallet selected successfully',
        'address': address,
        'balance': wallet.get_balance(blockchain)
    })

@app.route('/api/wallet/new')
def create_wallet():
    wallet = wallet_manager.create_wallet()
    session['wallet_address'] = wallet.address
    session.modified = True
    return jsonify({
        'message': 'New wallet created',
        'address': wallet.address,
        'balance': wallet.get_balance(blockchain)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1988, debug=True) 