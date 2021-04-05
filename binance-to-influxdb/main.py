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



if __name__ == "__main__":
    log_config = os.environ.get("LOG_CONFIG")
    if log_config:
        setup_logging(configFile=log_config)
    else:
        setup_logging()
    
    from app.coroutines import create_coros

    with open('config.yaml') as f:
        config = yaml.safe_load(f)

    coroutines = create_coros(config)
    loop = asyncio.get_event_loop()

    try:
        for coro in coroutines.values():
            asyncio.ensure_future(coro.market_stream())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print('Closing loop...')
        loop.close()


    