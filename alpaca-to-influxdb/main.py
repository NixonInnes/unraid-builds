import os
import asyncio
import logging
import logging.config
import yaml


if os.path.exists('.env'):
    try:
        from dotenv import load_dotenv
        load_dotenv(".env")
        print('Loaded .env environment file')
    except:
        print('Unable to load .env environment file!')


def setup_logging(
    configFile='logging.yaml',
    logLevel=logging.INFO,
):
    """Setup logging configuration

    """
    if os.path.exists(configFile):
        with open(configFile, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logLevel)



if __name__ == '__main__':
    log_config = os.environ.get("LOG_CONFIG")
    if log_config:
        setup_logging(configFile=log_config)
    else:
        setup_logging()

    from app.stream import market_stream
    from app.handler import StreamHandler

    with open('config.yaml') as f:
        config = yaml.safe_load(f)

    handler = StreamHandler(config)
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(market_stream(config, handler.consume))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing loop...")
        loop.close()



