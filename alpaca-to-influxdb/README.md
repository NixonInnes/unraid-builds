# Alpaca to InfluxDB
Alpaca to Influx is a container designed to be run on an [Unraid](https://www.unraid.net/) server via Docker. The purpose of the container is to simplify the ingestion of stock market data, provided by the [Alpaca API](https://alpaca.markets/), into your own [Influx database](https://www.influxdata.com/).  
The container collects the 1m candles (klines) for each of the configured market tickers. 

[[_TOC_]]

# Prerequisites
 - Alpaca account & API key
 - InfluxDB setup & token

>**NOTE**
>A free Alpaca account and paper trading API key will work just fine.

# Data
The container collects the 1m candles from the Alpaca API, for the configured tickers. The data is formatted and stored as a Point in the configured (see, [Configuration](#Configuration)) organisation and bucket of your InfluxDB in the following format:
```
{
    "measurement": <ticker>,
    "time": <candle time>,
    "tags":{"interval": "1m"},
    "fields": {
        "open": <open price>,
        "close": <close price>,
        "low": <low price>,
        "high": <high price>,
        "volume": <traded volume>
    }
}
```

>**NOTE**  
> The candle data is received after the candle completes (i.e. the 12:00 candle is received at 12:01:00). It is not updated "live", unlike the Binance to InfluxDB container. This is due to the way the Alpaca websocket functions. It is possible to obtain live quote data from the API, which may be included in a future release of this container.

# Configuration
A configuration file is stored within the container at `/config/config.yaml`. If no configuration is found when the container is launched, a sample configuration shall be created. In addition to the configuration file, environment variables for `ALPACA_ID`, `ALPACA_KEY` and `INFLUX_TOKEN` need to be specified. More detail for each is provided in the following sections:

## Config File (`/config/config.yaml`)
The configuration file should be similar to below:
```yaml
influx:
  url: http://influxdb.nixserver.io
  org: Test
  bucket: testing
  batch_size: 50
  interval: 10
alpaca:
  account-type: free
tickers:
  - AAPL
  - TSLA
```
The parameters within the configuration file are as defined:  
### influx:
 - `url` - The URL address of your Influx database
 - `org` - The name of the organisation within your InfluxDB associated with the specified token (see: # Environment Variables)
 - `bucket` - The name of the bucked within your defined InfluxDB organisation
 - `batch_size` - Maximum size of the InfluxDB client batch before writing to the Influx database (for more information, see [Batching](#Batching))
 - `interval` - Maximum interval (in seconds) before a batch is written to the Influx database (for more information, see [Batching](#Batching))

#### Batching
Data from the Alpaca API is not written directly to the Influx database. Data points are batched together and written simultaneously to reduce the number of interactions with the database.  
The container collects 1 data point, per ticker, per minute. 

### alpaca:
 - `account-type` - Either `free` or `unlimited`; the type of Alpaca account you have

### tickers:
This is a list of the market tickers you wish to collect the market data for.

## Environment Variables
Three environment variables need to be defined in the container, these are as follows:
- `ALPACA_ID` - Alpaca API Key ID
- `ALPACA_KEY` - Alpaca API Key Secret
- `INFLUX_TOKEN` - InfluxDB organisation/bucket token

If you are installing the container on your Unraid server, these are set in the configuration page of the app.

>**NOTE**
>You obtain your Alpaca API key by visiting the Live Trading page (paper accounts are fine), and creating an API Key in the right-hand menu (as of time of writing).