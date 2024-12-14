from typing import Final
from pathlib import Path
import json, os

EVM_PRIVATE_KEY: Final = os.environ['EVM_PRIVATE_KEY']
TRON_PRIVATE_KEY: Final = os.environ['TRON_PRIVATE_KEY']
TRON_GRID_API_KEY: Final = os.environ['TRON_GRID_API_KEY']
SECRET_KEY: Final = os.environ['SECRET_KEY']

with open(Path(__file__).parent.joinpath('evm/abis/aggregator.abi.json')) as f:
    EVM_AGGREGATOR_CONTRACT_ABI: Final = json.loads(f.read())

with open(Path(__file__).parent.joinpath('evm/abis/erc20.abi.json')) as f:
    EVM_ERC20_CONTRACT_ABI: Final = json.loads(f.read())