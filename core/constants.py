from typing import Final
from pathlib import Path
import json, os, multiprocessing

EVM_PRIVATE_KEY: Final = os.environ['EVM_PRIVATE_KEY']
TRON_PRIVATE_KEY: Final = os.environ['TRON_PRIVATE_KEY']
TRON_GRID_API_KEY: Final = os.environ['TRON_GRID_API_KEY']
TONAPI_API_KEY: Final = os.environ['TONAPI_API_KEY']
TON_MNEMONIC: Final = os.environ['TON_MNEMONIC']
SECRET_KEY: Final = os.environ['SECRET_KEY']

with open(Path(__file__).parent.joinpath('evm/abis/aggregator.abi.json')) as f:
    EVM_AGGREGATOR_CONTRACT_ABI: Final = json.loads(f.read())

with open(Path(__file__).parent.joinpath('evm/abis/erc20.abi.json')) as f:
    EVM_ERC20_CONTRACT_ABI: Final = json.loads(f.read())

CPU_COUNT = multiprocessing.cpu_count()
