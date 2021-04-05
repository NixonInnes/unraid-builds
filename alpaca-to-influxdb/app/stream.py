import os
import asyncio
import websockets
import json
from logging import getLogger

logger = getLogger(os.path.basename(__file__))


async def market_stream(config, consumer):
    auth_msg = {
        "action": "auth",
        "key": os.environ["ALPACA_ID"],
        "secret": os.environ["ALPACA_KEY"]
    }

    sub_msg = {
        "action": "subscribe",
        "bars": config["tickers"]
    }
    
    uri_prefix = "wss://stream.data.alpaca.markets/v2/"
    if config["alpaca"]["account-type"] == "free":
        uri_suffix = "iex"
    elif config["alpaca"]["account-type"] == "unlimited":
        uri_suffix = "sip"
    else:
        raise Exception("Unknown account-type configuration. Please use 'free' or 'unlimited'.")
    uri = uri_prefix + uri_suffix


    async with websockets.connect(uri, ssl=True) as ws:
        await ws.send(json.dumps(auth_msg))
        await ws.send(json.dumps(sub_msg))
        while True:
            recv = await (ws.recv())
            logger.debug(f'RECV: {recv}')
            consumer(recv)