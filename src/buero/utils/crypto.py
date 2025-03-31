import hashlib
import json
from typing import Dict, Any
from cryptography.hazmat.primitives import serialization, hashes, padding
from cryptography.hazmat.primitives.asymmetric import ec, padding as asymmetric_padding
from cryptography.hazmat.backends import default_backend
import base64

def generate_key_pair():
    """Genera un par de claves usando la curva SECP256K1."""
    private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
    public_key = private_key.public_key()
    return private_key, public_key

def get_public_key_bytes(public_key):
    """Obtiene los bytes de la clave pública en formato DER."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def get_private_key_bytes(private_key):
    """Obtiene los bytes de la clave privada."""
    return private_key.private_numbers().private_value.to_bytes(32, 'big')

def sign_message(private_key, message: str) -> str:
    """Firma un mensaje usando la clave privada."""
    message_bytes = message.encode('utf-8')
    signature = private_key.sign(
        message_bytes,
        ec.ECDSA(hashes.SHA256())
    )
    return base64.b64encode(signature).decode('utf-8')

def verify_signature(public_key, message: str, signature: str) -> bool:
    """Verifica la firma de un mensaje usando la clave pública."""
    try:
        message_bytes = message.encode('utf-8')
        signature_bytes = base64.b64decode(signature)
        public_key.verify(
            signature_bytes,
            message_bytes,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except:
        return False

def calculate_hash(data: Dict[str, Any]) -> str:
    """Calcula el hash SHA-256 de un diccionario."""
    data_string = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_string.encode()).hexdigest()

def calculate_block_hash(block: Dict[str, Any]) -> str:
    """Calcula el hash de un bloque."""
    block_copy = block.copy()
    if 'hash' in block_copy:
        del block_copy['hash']
    return calculate_hash(block_copy)

def mine_block(block: Dict[str, Any], difficulty: int) -> Dict[str, Any]:
    """Realiza la minería de un bloque usando Proof of Work."""
    block_copy = block.copy()
    nonce = 0
    
    while True:
        block_copy['nonce'] = nonce
        block_hash = calculate_block_hash(block_copy)
        
        if block_hash.startswith('0' * difficulty):
            block_copy['hash'] = block_hash
            return block_copy
        
        nonce += 1 