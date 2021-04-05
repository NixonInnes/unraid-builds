import os
import asyncio
import time
import websockets
from logging import getLogger

from app.handler import StreamHandler
from app.batcher import Batcher


def create_coros(config):
    coros = {}
    try:
        token = os.environ['INFLUXDB_TOKEN']
    except KeyError:
        raise KeyError('INFLUXDB_TOKEN not found in environment variables')

    batch = Batcher(
        url=config["influx"]["url"],
        org=config["influx"]["org"],
        bucket=config["influx"]["bucket"],
        token=token,
        size=config["influx"]["batch_size"],
        flush_interval=config["influx"]["interval"]*1000
    )

    for stream_name, stream_conf in config['streams'].items():
        coros[stream_name] = StreamCoro(
            batch,
            symbol=stream_conf["symbol"],
            interval=stream_conf["interval"],    
            name=stream_name
        )
    return coros


class StreamCoro:
    def __init__(
            self,
            batch,
            symbol="",
            interval="",
            name=""
    ):
        self._name = name
        self.logger = getLogger(self.__class__.__name__ + f'[{name}]')
        self.symbol = symbol
        self.interval = interval
        self.handler = StreamHandler(batch)
        self.__stopped = False

    def stop(self):
        self.__stopped = True

    async def market_stream(self):
        uri = f'wss://stream.binance.com:9443/ws/{self.symbol}@kline_{self.interval}'
        self.logger.info(f'Connecting to {uri} ...')
        async with websockets.connect(uri, ssl=True) as ws:
            while not self.__stopped:
                recv = await ws.recv()
                self.logger.debug(f'Received: {recv}')
                self.handler.consume(recv)
