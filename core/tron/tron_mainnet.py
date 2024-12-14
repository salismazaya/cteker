from .core import TronCore, TronMainnetClientMixin

class TronMainnet(TronMainnetClientMixin, TronCore):
    def get_id(self):
        return 'tron-mainnet'
    
    def add_explorer(self, tx_hash: str):
        return 'https://tronscan.org/#/transaction/' + tx_hash

    def get_name(self):
        return "TRON"
    
    def get_symbol(self):
        return "TRX"
    
    def get_binance_ticker(self):
        return 'TRXUSDT'