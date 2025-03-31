from typing import Dict, Optional
from .wallet import Wallet
import json
import os
import base64

class WalletManager:
    def __init__(self, storage_dir: str = "wallets"):
        self.storage_dir = storage_dir
        self.wallets: Dict[str, Wallet] = {}
        self._ensure_storage_dir()
        self._load_wallets()

    def _ensure_storage_dir(self):
        """Asegura que el directorio de almacenamiento existe."""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def _load_wallets(self):
        """Carga las carteras existentes del almacenamiento."""
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(self.storage_dir, filename), 'r') as f:
                        wallet_data = json.load(f)
                        private_key_bytes = base64.b64decode(wallet_data['private_key'])
                        wallet = Wallet.import_wallet(private_key_bytes)
                        self.wallets[wallet.address] = wallet
                except Exception as e:
                    print(f"Error loading wallet {filename}: {e}")

    def create_wallet(self) -> Wallet:
        """Crea una nueva cartera y la guarda."""
        wallet = Wallet()  # Esto generará una nueva clave privada aleatoria
        self.wallets[wallet.address] = wallet
        self._save_wallet(wallet)
        return wallet

    def get_wallet(self, address: str) -> Optional[Wallet]:
        """Obtiene una cartera por su dirección."""
        return self.wallets.get(address)

    def _save_wallet(self, wallet: Wallet):
        """Guarda una cartera en el almacenamiento."""
        try:
            wallet_data = {
                'address': wallet.address,
                'private_key': base64.b64encode(wallet.export_private_key()).decode(),
                'public_key': base64.b64encode(wallet.export_public_key()).decode()
            }
            filename = f"{wallet.address}.json"
            filepath = os.path.join(self.storage_dir, filename)
            with open(filepath, 'w') as f:
                json.dump(wallet_data, f)
            print(f"Wallet saved to {filepath}")
        except Exception as e:
            print(f"Error saving wallet: {e}")

    def list_wallets(self, blockchain) -> list:
        """Lista todas las carteras disponibles con sus balances."""
        return [{
            'address': addr,
            'balance': wallet.get_balance(blockchain)
        } for addr, wallet in self.wallets.items()] 