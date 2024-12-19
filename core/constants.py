from typing import Final
from pathlib import Path
import json, os, multiprocessing

DEBUG = os.environ.get('DEBUG', 'True') == 'True'
CPU_COUNT = multiprocessing.cpu_count()

EVM_PRIVATE_KEY: Final = os.environ.get('EVM_PRIVATE_KEY')
TRON_PRIVATE_KEY: Final = os.environ.get('TRON_PRIVATE_KEY')
TRON_GRID_API_KEY: Final = os.environ.get('TRON_GRID_API_KEY')
TONAPI_API_KEY: Final = os.environ.get('TONAPI_API_KEY')
TON_MNEMONIC: Final = os.environ.get('TON_MNEMONIC')
SECRET_KEY: Final = os.environ['SECRET_KEY']

with open(Path(__file__).parent.joinpath('evm/abis/aggregator.abi.json')) as f:
    EVM_AGGREGATOR_CONTRACT_ABI: Final = json.loads(f.read())

with open(Path(__file__).parent.joinpath('evm/abis/erc20.abi.json')) as f:
    EVM_ERC20_CONTRACT_ABI: Final = json.loads(f.read())

