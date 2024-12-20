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
    network = get_network_by_id('eth-holesky')
    txs = []

    for _ in range(10):
        tx = network.transfer('0x59Ef8686E6065f38bD257976Da4d87300100d914', 0.00001)
        txs.append(tx)

    results = await asyncio.gather(*txs)
    print(results)

asyncio.run(main())
