import os
import datetime
import json
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import WriteOptions


from logging import getLogger


class StreamHandler:
    def __init__(self, config):
        self.logger = getLogger(self.__class__.__name__)
        self.org = config["influx"]["org"]
        self.bucket = config["influx"]["bucket"]

        client = InfluxDBClient(
            url=config["influx"]["url"], 
            token=os.environ["INFLUX_TOKEN"]
        )
        write_options = WriteOptions(
            batch_size=config["influx"]["batch_size"],
            flush_interval=config["influx"]["interval"]
        )
        self.write_api = client.write_api(write_options=write_options)

    def consume(self, recv):
        data = json.loads(recv)
        points = []
        for d in data:
            if d["T"] == "b":
                point = {
                    "measurement": d["S"],
                    "tags": {
                        "interval": "1m"
                    },
                    "time": datetime.datetime.strptime(
                        d["t"], "%Y-%m-%dT%H:%M:%S%z"
                    ),
                    "fields": {
                        "open": float(d["o"]),
                        "close": float(d["c"]),
                        "high": float(d["h"]),
                        "low": float(d["l"]),
                        "volume": float(d["v"])
                    }
                }
                points.append(point)
        self.write(points)

    def write(self, points):
        self.write_api.write(
            self.bucket,
            self.org,
            points
        )