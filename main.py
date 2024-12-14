# load .env
from dotenv import load_dotenv
from pathlib import Path


env_path_file = Path(__file__).parent / '.env'

load_dotenv(env_path_file)
# end load .env

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from helpers.networks import get_network_by_id
from core import constants
from helpers.redis import redis_client
import validations.transfer
import exceptions.transaction
import hashlib, asyncio

app = FastAPI()

transfer_lock = asyncio.Lock()

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
        content = {
            'status': 'bad',
            'message': str(e)
        }
        return JSONResponse(content, status_code = status.HTTP_400_BAD_REQUEST)

    async with transfer_lock:
        await redis_client.set(signature_key, "true")

    return {
        'status': 'ok',
        'tx_hash': tx_hash_prefixed
    }

@app.get('/price')
async def transfer(network_id: str):
    try:
        network = get_network_by_id(network_id)
        price = await network.get_price()
    except ValueError as e:
        content = {
            'status': 'bad',
            'message': str(e)
        }
        return JSONResponse(content, status_code = status.HTTP_400_BAD_REQUEST)

    return {
        'status': 'ok',
        'price': price,
        'ticker': network.get_binance_ticker()
    }