# ======== SETUP ========

from dotenv import load_dotenv
from pathlib import Path

env_path_file = Path(__file__).parent / '.env'

load_dotenv(env_path_file)

from helpers.networks import NETWORKS

_ = [_.get_id() for _ in NETWORKS]
if len(_) != len(set(_)):
    raise ValueError("network id contains duplicate")

from helpers.log import logger

logger.info("SETUP COMPLETED")

# ======== SETUP COMPLETED ========

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from helpers.networks import get_network_by_id
from helpers.redis import redis_client
from helpers.decorators import cache_redis, limit_concurrent_request
import validations.transfer
import exceptions.transaction
import hashlib, asyncio, traceback
from core import constants

app = FastAPI()

transfer_lock = asyncio.Lock()

@app.get('/networks')
@cache_redis(10)
@limit_concurrent_request(1)
# Limit concurrent requests to 1
# If caching is enabled, the limit will be disabled
async def fetch_networks():
    semaphore = asyncio.Semaphore(constants.CPU_COUNT)

    async def fetch(network):
        async with semaphore:
            return {
                'id': network.get_id(),
                'name': network.get_name(),
                'symbol': network.get_symbol(),
                'address': network.get_address(),
                'balance': await network.get_balance(),
                'price': await network.get_price(),
                'binance_ticker': network.get_binance_ticker()
            }
    
    try:
        networks = await asyncio.gather(*[fetch(network) for network in NETWORKS])
        response = {
            'status': 'ok',
            'data': {
                'networks': networks
            }
        }
        return response
    except:
        logger.exception("ERROR")

        response = {
            'status': 'bad',
            'message': 'failed fetch data'
        }
        
        return JSONResponse(response, status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.post('/transfer')
async def transfer(transfer: validations.transfer.Transfer):
    expected_signature = hashlib.sha256(f"{constants.SECRET_KEY}:{transfer.network_id}:{transfer.receipent}:{transfer.amount}:{transfer.unique}:{transfer.gas}".encode()).hexdigest()
    signature_key = f"signature_{transfer.unique}"

    async with transfer_lock:
        is_signature_exists = await redis_client.exists(signature_key)

    if is_signature_exists or \
        expected_signature.lower() != transfer.signature.lower():
        content = {
            'status': 'bad',
            'message': 'bad signature'
        }
        return JSONResponse(content, status_code = status.HTTP_400_BAD_REQUEST)

    try:
        network = get_network_by_id(transfer.network_id)
        tx_hash = await network.transfer(transfer.receipent, transfer.amount, gas = transfer.gas)
        tx_hash_prefixed = network.add_explorer(tx_hash)
    except (exceptions.transaction.TransactionFailed, ValueError) as e:
        logger.exception("ERROR")

        content = {
            'status': 'bad',
            'message': str(e)
        }
        return JSONResponse(content, status_code = status.HTTP_400_BAD_REQUEST)

    async with transfer_lock:
        await redis_client.set(signature_key, "true")

    return {
        'status': 'ok',
        'data': {
            'tx_hash': tx_hash_prefixed
        }
    }

@app.get('/networks/{network_id}')
@cache_redis(10)
@limit_concurrent_request(1)
# Limit concurrent requests to 1
# If caching is enabled, the limit will be disabled
async def get_network(network_id: str):
    try:
        network = get_network_by_id(network_id)
    except ValueError:
        logger.debug(f"network id {network_id} not found!")

        content = {
            'status': 'bad',
            'message': 'bad network_id'
        }

        return JSONResponse(content, status_code = status.HTTP_400_BAD_REQUEST)
    
    async def fetch(network):
        return {
            'id': network.get_id(),
            'name': network.get_name(),
            'symbol': network.get_symbol(),
            'address': network.get_address(),
            'balance': await network.get_balance(),
            'price': await network.get_price(),
            'binance_ticker': network.get_binance_ticker()
        }
    
    try:
        result = await fetch(network)
        return {
            'status': 'ok',
            'data': {
                'network': result
            }
        }
    except:
        logger.exception("ERROR")
        
        content = {
            'status': 'bad',
            'message': 'failed fetch data'
        }

        return JSONResponse(content, status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)