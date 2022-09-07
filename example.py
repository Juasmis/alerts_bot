import logging
from custom_loging_handler import api_logging_handler

api_url = "http://127.0.0.1:8000/generate_alert"

# Loggers configuration

# Basic logger configuration
logger = logging.getLogger("example")
streamHanlder = logging.StreamHandler()
streamHanlder.setFormatter("%(asctime)s - [%(levelname)s] - %(message)s")
logger.addHandler(streamHanlder)

# Api logger
logger_api = logging.getLogger('example_api')
api_handler = api_logging_handler(api_url)
logger_api.addHandler(api_handler)
logger_api.setLevel(logging.INFO)


if __name__ == '__main__':
    
    logger_api.info('Test info log message')
    logger_api.warning('Test warning log message')
    logger_api.error('Test error log message')