import datetime
import json

from logging import getLogger


class StreamHandler:
    def __init__(self, batch):
        self.logger = getLogger(self.__class__.__name__)
        self.prev_point = None
        self.batch = batch

    def consume(self, recv):
        data = json.loads(recv)
        point = {
            "measurement": data["s"],
            "tags": {
                "interval": data["k"]["i"]
            },
            "time": datetime.datetime.utcfromtimestamp(data["k"]["t"]/1000),
            "fields": {
                "open": float(data["k"]["o"]),
                "close": float(data["k"]["c"]),
                "high": float(data["k"]["h"]),
                "low": float(data["k"]["l"]),
                "volume": float(data["k"]["v"])
            }
        }
        self.batch.add(point)