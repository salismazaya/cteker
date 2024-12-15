from .core import TonCore, TonMainnetClientMixin

class TonMainnet(TonMainnetClientMixin, TonCore):
    def get_id(self):
        return 'ton-mainnet'
    
    def add_explorer(self, tx_hash: str):
        return 'https://tonviewer.com/transaction/' + tx_hash

    def get_name(self):
        return "TON MAINNET"
    
    def get_symbol(self):
        return "TON"
    
    def get_binance_ticker(self):
        return 'TONUSDT'
    
    def get_address(self) -> str:
        return self.wallet.address.to_str(True, True, False, False)