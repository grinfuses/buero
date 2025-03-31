import time
from typing import List, Dict, Any
from ..utils.crypto import calculate_hash, calculate_block_hash, mine_block

class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.chain: List[Dict[str, Any]] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Dict[str, Any]] = []
        self.mining_reward = 10.0  # Recompensa por minar un bloque
        
        # Crear el bloque génesis
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Crea el primer bloque de la cadena."""
        genesis_block = {
            'index': 0,
            'timestamp': time.time(),
            'transactions': [],
            'previous_hash': '0',
            'nonce': 0
        }
        genesis_block['hash'] = calculate_block_hash(genesis_block)
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Dict[str, Any]:
        """Obtiene el último bloque de la cadena."""
        return self.chain[-1]
    
    def mine_pending_transactions(self, miner_address: str):
        """Mina un nuevo bloque con las transacciones pendientes."""
        # Crear el bloque con las transacciones pendientes
        block = {
            'index': len(self.chain),
            'timestamp': time.time(),
            'transactions': self.pending_transactions,
            'previous_hash': self.get_latest_block()['hash'],
            'nonce': 0
        }
        
        # Minar el bloque
        mined_block = mine_block(block, self.difficulty)
        
        # Añadir el bloque a la cadena
        self.chain.append(mined_block)
        
        # Limpiar transacciones pendientes
        self.pending_transactions = []
        
        # Añadir recompensa de minería
        self.add_transaction(None, miner_address, self.mining_reward)
    
    def add_transaction(self, sender: str, recipient: str, amount: float):
        """Añade una nueva transacción al pool de transacciones pendientes."""
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': time.time()
        }
        self.pending_transactions.append(transaction)
    
    def get_balance(self, address: str) -> float:
        """Calcula el balance de una dirección."""
        balance = 0.0
        
        # Revisar todas las transacciones en la cadena
        for block in self.chain:
            for transaction in block['transactions']:
                if transaction['recipient'] == address:
                    balance += transaction['amount']
                if transaction['sender'] == address:
                    balance -= transaction['amount']
        
        # Revisar transacciones pendientes
        for transaction in self.pending_transactions:
            if transaction['recipient'] == address:
                balance += transaction['amount']
            if transaction['sender'] == address:
                balance -= transaction['amount']
        
        return balance
    
    def is_chain_valid(self) -> bool:
        """Verifica si la cadena de bloques es válida."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verificar hash del bloque actual
            if current_block['hash'] != calculate_block_hash(current_block):
                return False
            
            # Verificar hash del bloque anterior
            if current_block['previous_hash'] != previous_block['hash']:
                return False
            
            # Verificar que el hash cumple con la dificultad
            if not current_block['hash'].startswith('0' * self.difficulty):
                return False
        
        return True 