import os
import asyncio
import websockets
from threading import Thread
from logging import getLogger

logger = getLogger(os.path.basename(__file__))

async def market_stream(symbol, interval, consumer):
    uri = f'wss://stream.binance.com:9443/ws/{symbol}@kline_{interval}'
    logger.info(f'Connecting to {uri} ...')
    async with websockets.connect(uri, ssl=True) as ws:
        logger.info('Connected')
        while True:
            recv = await ws.recv()
            logger.debug(f'RECV: {recv}')
            consumer(recv)
