import sys
from pathlib import Path

sys.path[0] = Path(sys.path[0]).parent.as_posix()

from helpers.networks import get_network_by_id

import asyncio

async def main():
    network = get_network_by_id('holesky')
    print(await network.get_price())

asyncio.run(main())
