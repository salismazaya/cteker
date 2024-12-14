from core.evm.evm_flexible import EvmFlexible
from core.tron.tron_nile_testnet import TronNileTestnet
from core.tron.tron_mainnet import TronMainnet

networks = [
    EvmFlexible("sepolia", "Sepolia", "ETH", "ETHUSDT", "https://ethereum-sepolia-rpc.publicnode.com", "https://sepolia.etherscan.io/tx/"),
    EvmFlexible("holesky", "Holesky", "ETH", "ETHUSDT", "https://ethereum-holesky-rpc.publicnode.com", "https://holesky.etherscan.io/tx/"),
    TronNileTestnet(),
    TronMainnet(),
]