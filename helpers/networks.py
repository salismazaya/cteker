import core.core
from networks.default import networks as default_networks
from typing import List

try:
    custom_networks = __import__("networks.custom_networks", fromlist = ['networks'])
    custom_networks = custom_networks.networks
except:
    custom_networks = []

NETWORKS: List[core.core.Core] = default_networks + custom_networks

def get_network_by_id(_id: str) -> 'core.core.Core':
    for network in NETWORKS:
        if network.get_id() == _id:
            return network
    else:
        raise ValueError(f'network with id {_id} not found')