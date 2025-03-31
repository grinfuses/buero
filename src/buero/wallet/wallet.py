from typing import Dict, Any, Tuple
import time
from ..utils.crypto import generate_key_pair, get_public_key_bytes, get_private_key_bytes, sign_message, verify_signature
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import hashlib
import base58
import json
from typing import Optional
import os

class Wallet:
    def __init__(self):
        # Generar una nueva clave privada aleatoria
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()
        self.address = self._generate_address()
    
    def _generate_address(self) -> str:
        """Genera la dirección de la cartera a partir de la clave pública."""
        public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        sha256_hash = hashlib.sha256(public_key_bytes).digest()
        ripemd160_hash = hashlib.new('ripemd160')
        ripemd160_hash.update(sha256_hash)
        ripemd160_hash = ripemd160_hash.digest()
        
        # Añadir prefijo de red (0x00 para mainnet)
        version = b'\x00'
        vh160 = version + ripemd160_hash
        
        # Calcular checksum
        double_sha256 = hashlib.sha256(hashlib.sha256(vh160).digest()).digest()
        checksum = double_sha256[:4]
        
        # Combinar y codificar en Base58
        binary_address = vh160 + checksum
        address = base58.b58encode(binary_address).decode('utf-8')
        
        return address
    
    def get_balance(self, blockchain) -> float:
        """Obtiene el balance de la cartera."""
        balance = 0.0
        
        # Recompensa por minar
        for block in blockchain.chain:
            if block.get('miner') == self.address:
                balance += 10.0  # Recompensa por minar
        
        # Transacciones recibidas
        for block in blockchain.chain:
            for transaction in block.get('transactions', []):
                if transaction.get('recipient') == self.address:
                    balance += float(transaction.get('amount', 0))
        
        # Transacciones enviadas
        for block in blockchain.chain:
            for transaction in block.get('transactions', []):
                if transaction.get('sender') == self.address:
                    balance -= float(transaction.get('amount', 0))
        
        return balance
    
    def send_transaction(self, recipient: str, amount: float, blockchain) -> bool:
        """Envía una transacción a otra cartera."""
        if amount <= 0:
            return False
            
        balance = self.get_balance(blockchain)
        if balance < amount:
            return False
            
        transaction = {
            'sender': self.address,
            'recipient': recipient,
            'amount': amount,
            'timestamp': time.time()
        }
        
        # Firmar la transacción
        message = f"{self.address}{recipient}{amount}{transaction['timestamp']}"
        transaction['signature'] = sign_message(self.private_key, message)
        
        blockchain.add_transaction(self.address, recipient, amount)
        return True
    
    def verify_transaction(self, transaction: Dict[str, Any]) -> bool:
        """Verifica una transacción usando la clave pública."""
        if 'signature' not in transaction:
            return False
        
        message = f"{transaction['sender']}{transaction['recipient']}{transaction['amount']}{transaction['timestamp']}"
        return verify_signature(self.public_key, message, transaction['signature'])
    
    def export_private_key(self) -> bytes:
        """Exporta la clave privada en formato bytes."""
        return self.private_key.private_numbers().private_value.to_bytes(32, 'big')
    
    def export_public_key(self) -> bytes:
        """Exporta la clave pública en formato DER."""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
    @staticmethod
    def import_wallet(private_key_bytes: bytes) -> 'Wallet':
        """Importa una cartera desde una clave privada."""
        try:
            # Crear una nueva instancia de Wallet
            wallet = Wallet()
            # Reemplazar la clave privada generada con la proporcionada
            wallet.private_key = ec.derive_private_key(
                int.from_bytes(private_key_bytes, 'big'),
                ec.SECP256K1(),
                default_backend()
            )
            wallet.public_key = wallet.private_key.public_key()
            wallet.address = wallet._generate_address()
            return wallet
        except Exception as e:
            print(f"Error importing wallet: {e}")
            return None 