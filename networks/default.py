from core.evm.evm_flexible import EvmFlexible, EvmFlexibleToken
from core.tron.tron_nile_testnet import TronNileTestnet
from core.tron.tron_mainnet import TronMainnet
from core.tron.tron_flexible import TronMainnetTokenFlexible
from core.ton.ton_mainnet import TonMainnet
from core.ton.ton_testnet import TonTestnet
from core import constants
from helpers.log import logger

networks = []

if not constants.EVM_PRIVATE_KEY is None:
    # ======= ADD EVM NETWORKS HERE =======
    evm_networks = [
        EvmFlexible("eth-sepolia", "Sepolia", "ETH", "ETHUSDT",
                    "https://ethereum-sepolia-rpc.publicnode.com",
                    "https://sepolia.etherscan.io/tx/"),

        EvmFlexible("eth-holesky", "Holesky", "ETH", "ETHUSDT",
                     "https://ethereum-holesky-rpc.publicnode.com",
                     "https://holesky.etherscan.io/tx/"),

        EvmFlexible("eth-mainnet", "Ethereum Mainnet", "ETH", "ETHUSDT",
                     "https://eth.drpc.org",
                     "https://etherscan.io/tx/"),
        
        EvmFlexible("polygon-mainnet", "Polygon Mainnet", "POL", "POLUSDT",
                     "https://polygon.meowrpc.com",
                     "https://polygonscan.com/tx/"),

        EvmFlexibleToken("eth-mainnet-usdt", "USDT Ethereum Mainnet", "USDT",
                    '0xdac17f958d2ee523a2206206994597c13d831ec7',
                    "USDCUSDT",
                     "https://eth.drpc.org",
                     "https://etherscan.io/tx/"),
    ]
    # ======= END: ADD EVM NETWORKS HERE =======
    networks.extend(evm_networks)
    logger.info("EVM network active")
else:
    logger.info("EVM network NOT active")

if (not constants.TRON_PRIVATE_KEY is None) and (not constants.TRON_GRID_API_KEY is None):
    # ======= ADD TRON NETWORKS HERE =======
    tron_networks = [
        TronNileTestnet(),
        TronMainnet(),
        TronMainnetTokenFlexible(
            "tron-mainnet-usdt",
            'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t',
            'USDT TRON Mainnet',
            'USDT',
            'USDCUSDT'
        )
    ]
    # ======= END: ADD TRON NETWORKS HERE =======
    networks.extend(tron_networks)
    logger.info("TRON network active")
else:
    logger.info("TRON network NOT active")

if (not constants.TON_MNEMONIC is None) and (not constants.TONAPI_API_KEY is None):
    # ======= ADD TON NETWORKS HERE =======
    ton_networks = [
        TonMainnet(),
        TonTestnet()
    ]
    # ======= END: ADD TON NETWORKS HERE =======
    networks.extend(ton_networks)
    logger.info("TON network active")
else:
    logger.info("TON network active")
