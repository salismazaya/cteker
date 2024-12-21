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
                    "https://sepolia.etherscan.io/tx/")
                    .as_redis_transaction_limitter('eth-sepolia', 5, 2),

        EvmFlexible("eth-holesky", "Holesky", "ETH", "ETHUSDT",
                     "https://ethereum-holesky-rpc.publicnode.com",
                     "https://holesky.etherscan.io/tx/")
                    .as_redis_transaction_limitter('eth-holesky', 5, 2),

        EvmFlexible("eth-mainnet", "Ethereum Mainnet", "ETH", "ETHUSDT",
                     "https://ethereum-rpc.publicnode.com",
                     "https://etherscan.io/tx/")
                    .as_redis_transaction_limitter('eth-mainnet', 5, 2),
        
        EvmFlexible("polygon-mainnet", "Polygon Mainnet", "POL", "POLUSDT",
                     "https://polygon-bor-rpc.publicnode.com",
                     "https://polygonscan.com/tx/")
                    .as_redis_transaction_limitter('polygon-mainnet', 5, 2),

        EvmFlexibleToken("eth-mainnet-usdt", "USDT Ethereum Mainnet", "USDT",
                    '0xdac17f958d2ee523a2206206994597c13d831ec7',
                    "USDCUSDT",
                     "https://ethereum-rpc.publicnode.com",
                     "https://etherscan.io/tx/")
                    .as_redis_transaction_limitter('eth-mainnet', 5, 2),
    ]
    # ======= END: ADD EVM NETWORKS HERE =======
    networks.extend(evm_networks)
    logger.info("EVM network active")
else:
    logger.info("EVM network NOT active")

if (not constants.TRON_PRIVATE_KEY is None) and (not constants.TRON_GRID_API_KEY is None):
    # ======= ADD TRON NETWORKS HERE =======
    tron_networks = [
        TronNileTestnet().as_redis_transaction_limitter('tron-testnet', 5, 10),
        
        TronMainnet().as_redis_transaction_limitter('tron-mainnet', 5, 10),

        TronMainnetTokenFlexible(
            "tron-mainnet-usdt",
            'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t',
            'USDT TRON Mainnet',
            'USDT',
            'USDCUSDT'
        ).as_redis_transaction_limitter('tron-mainnet', 5, 10),
    ]
    # ======= END: ADD TRON NETWORKS HERE =======
    networks.extend(tron_networks)
    logger.info("TRON network active")
else:
    logger.info("TRON network NOT active")

if (not constants.TON_MNEMONIC is None) and (not constants.TONAPI_API_KEY is None):
    # ======= ADD TON NETWORKS HERE =======
    ton_networks = [
        TonMainnet().as_redis_transaction_limitter('ton', 5, 10),
        
        TonTestnet().as_redis_transaction_limitter('ton', 5, 10),
    ]
    # ======= END: ADD TON NETWORKS HERE =======
    networks.extend(ton_networks)
    logger.info("TON network active")
else:
    logger.info("TON network active")
