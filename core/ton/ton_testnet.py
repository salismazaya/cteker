from .core import TonCore, TonTestnetClientMixin

class TonTestnet(TonTestnetClientMixin, TonCore):
    def get_id(self):
        return 'ton-testnet'
    
    def add_explorer(self, tx_hash: str):
        return 'https://testnet.tonviewer.com/transaction/' + tx_hash

    def get_name(self):
        return "TON TESTNET"
    
    def get_symbol(self):
        return "TON"
    
    def get_binance_ticker(self):
        return 'TONUSDT'
