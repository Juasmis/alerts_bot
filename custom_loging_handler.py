import logging
import requests

class api_logging_handler(logging.Handler):
    """Custom log handler to send log messages and alerts to API

    Args:
        logging (_type_): _description_
    """
    
    def __init__(self, api_url):
        # Initialize logger
        logging.Handler.__init__(self)
        
        # Set format
        # self.setFormatter("%(asctime)s - [%(levelname)s] - %(message)s")
        
        # Set API url
        self.api_url = api_url
        
    def emit(self, log_record):
        # Every time the logger is called it will format the message and send it to the API
                
        alert_data = {
            "level": log_record.levelname,
            "title": "hola",
            "message": log_record.msg,
            "source": log_record.name,
        }
    
        requests.post(self.api_url, json=alert_data)
