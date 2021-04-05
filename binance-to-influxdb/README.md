# Binance to InfluxDB
Binance to Influx is a container designed to be run on an [Unraid](https://www.unraid.net/) server via Docker. The purpose of the container is to simplify the ingestion of cryptocurrency market data, provided by the [Binance API](https://binance.com/), into your own [Influx database](https://www.influxdata.com/).  
The container collects the candles (klines) for each of the configured crypto symbols (e.g. BTCUSDT). 

## Contents
- [Prerequisites](#prerequisites)
- [Data](#data)
- [Configuration](#configuration)
  * [Config File](#config-file)
  * [Environment Variables](#environment-variables)

# Prerequisites
 - InfluxDB setup & token

# Data
The container collects candle data from the Binance API, for the configured symbols. The data is formatted and stored as a Point in the configured (see, [Configuration](#Configuration)) organisation and bucket of your InfluxDB in the following format:
```
{
    "measurement": <ticker>,
    "time": <candle time>,
    "tags":{"interval": <candle interval>},
    "fields": {
        "open": <open price>,
        "close": <close price>,
        "low": <low price>,
        "high": <high price>,
        "volume": <traded volume>
    }
}
```

# Configuration
A configuration file is stored within the container at `/config/config.yaml`. If no configuration is found when the container is launched, a sample configuration shall be created. In addition to the configuration file, an environment variable for your `INFLUX_TOKEN` needs to be specified. More detail for each is provided in the following sections:

## Config File 
`/config/config.yaml`  
The configuration file should be similar to below:
```yaml
influx:
  url: http://influxdb.nixserver.io
  org: Test
  bucket: testing
  batch_size: 50
  interval: 10
streams:
  ETHUSDT-1m:
    symbol: adausdt
    interval: 1m
  BTCUSDT-1m:
    symbol: btcusdt
    interval: 1m
```
The parameters within the configuration file are as defined:  
### influx
 - `url` - The URL address of your Influx database
 - `org` - The name of the organisation within your InfluxDB associated with the specified token (see: # Environment Variables)
 - `bucket` - The name of the bucked within your defined InfluxDB organisation
 - `batch_size` - Maximum size of the InfluxDB client batch before writing to the Influx database (for more information, see [Batching](#Batching))
 - `interval` - Maximum interval (in seconds) before a batch is written to the Influx database (for more information, see [Batching](#Batching))

#### Batching
Data from the Binance API is not written directly to the Influx database. Data points are batched together and written simultaneously to reduce the number of interactions with the database. The configuration allows for defining the maximum size the batch before writing to the Influx database (`batch_size`) and the maximum time before a batch is written to the Influx database (`interval`).    
The container collects 1 data point, per symbol, every 2 seconds.

### streams
This is a definition of the symbols and their intervals which you wish to collect the market data for. The format for defining them is as follows:
```
  <measurement name>:
    symbol: <symbol>
    interval: <candle interval>
```

>**NOTE**  
>The `interval` can be defined as any of the following: _1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w or 1M_

## Environment Variables
An environment variable needs to be defined in the container containing your InfluxDB token:
- `INFLUX_TOKEN` - InfluxDB organisation/bucket token

If you are installing the container on your Unraid server, these are set in the configuration page of the app.
