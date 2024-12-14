from .core import TronCore, TronNileTestnetClientMixin

class TronNileTestnet(TronNileTestnetClientMixin, TronCore):
    def get_id(self):
        return 'tron-nile-testnet'
    
    def add_explorer(self, tx_hash: str):
        return 'https://nile.tronscan.org/#/transaction/' + tx_hash
    
    def get_name(self):
        return "TRON"
    
    def get_symbol(self):
        return "TRX"
    
    def get_binance_ticker(self):
        return 'TRXUSDT'