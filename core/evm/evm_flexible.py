from .core import EvmCore, EvmTokenCore

class EvmFlexible(EvmCore):
    def __init__(self, _id: str, name: str, symbol: str, binance_ticker: str, http_rpc_url: str, base_explorer_prefix_url: str):
        self._id = _id
        self._name = name
        self._symbol = symbol
        self._binance_ticker = binance_ticker
        self._http_rpc_url = http_rpc_url
        self._base_explorer_prefix_url = base_explorer_prefix_url
        super().__init__()
    
    def get_id(self):
        return self._id

    def get_name(self):
        return self._name
    
    def get_symbol(self):
        return self._symbol
    
    def get_binance_ticker(self):
        return self._binance_ticker
    
    def get_http_rpc(self):
        return self._http_rpc_url
    
    def add_explorer(self, tx_hash: str):
        return self._base_explorer_prefix_url + tx_hash


class EvmFlexibleToken(EvmTokenCore, EvmFlexible):
    def __init__(self, _id: str, name: str, symbol: str, token_address: str, binance_ticker: str, http_rpc_url: str, base_explorer_prefix_url: str):
        super().__init__(_id, name, symbol, binance_ticker, http_rpc_url, base_explorer_prefix_url)
        self._token_address = token_address
    
    def get_token_address(self):
        return self._token_address