from dotenv import load_dotenv
from pathlib import Path

env_path_file = Path(__file__).parent.parent / '.env'

load_dotenv(env_path_file)

import sys
from pathlib import Path

sys.path[0] = Path(sys.path[0]).parent.as_posix()

from helpers.networks import get_network_by_id

import asyncio

async def main():
    network = get_network_by_id('ton-testnet')
    print(network.get_address())
    # print(await network.get_balance())
    # print(await network.wallet.deploy())
    txs = await asyncio.gather(
        network.transfer('0QCSES0TZYqcVkgoguhIb8iMEo4cvaEwmIrU5qbQgnN8fo2A', 0.01),
        network.transfer('0QCSES0TZYqcVkgoguhIb8iMEo4cvaEwmIrU5qbQgnN8fo2A', 0.01),
        network.transfer('0QCSES0TZYqcVkgoguhIb8iMEo4cvaEwmIrU5qbQgnN8fo2A', 0.01),
        network.transfer('0QCSES0TZYqcVkgoguhIb8iMEo4cvaEwmIrU5qbQgnN8fo2A', 0.03),

    )
    print(txs)

asyncio.run(main())
