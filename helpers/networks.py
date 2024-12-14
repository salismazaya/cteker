import core.core
from networks.default import networks as default_networks
from networks.custom_networks import networks as custom_networs

NETWORKS = default_networks + custom_networs

def get_network_by_id(_id: str) -> 'core.core.Core':
    for network in NETWORKS:
        if network.get_id() == _id:
            return network
    else:
        raise ValueError(f'network with id {_id} not found')