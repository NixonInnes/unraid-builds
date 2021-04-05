from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import WriteOptions

from logging import getLogger

class Batcher:
    def __init__(
        self,
        url,
        org,
        bucket,
        token,
        size=50,
        flush_interval=10_000
    ):
        self.logger = getLogger(self.__class__.__name__)
        self.org = org
        self.bucket = bucket
        client = InfluxDBClient(url=url, token=token)
        write_options = WriteOptions(
            batch_size=size,
            flush_interval=flush_interval
        )
        self.write_api = client.write_api(write_options=write_options)

    def add(self, point):
        self.write_api.write(
            self.bucket, 
            self.org, 
            [point], 
        )
