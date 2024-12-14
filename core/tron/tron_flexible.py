from .core import TronTokenCore, TronNileTestnetClientMixin, TronMainnetClientMixin

class TronNilTestnetTokenFlexible(TronNileTestnetClientMixin, TronTokenCore):
    def __init__(self, _id: str, token_address: str, name: str, symbol: str, binance_ticker: str):
        self._id = _id
        self._symbol = symbol
        self._name = name
        self._binance_ticker = binance_ticker
        self._token_address = token_address
        super().__init__()

    def get_id(self):
        return self._id
    
    def get_token_address(self):
        return self._token_address

    def get_name(self):
        return self._name
    
    def get_symbol(self):
        return self._symbol
    
    def get_binance_ticker(self):
        return self._binance_ticker

class TronMainnetTokenFlexible(TronMainnetClientMixin, TronNilTestnetTokenFlexible):
    pass