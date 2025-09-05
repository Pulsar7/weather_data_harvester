import re
import os, sys
import logging
from dotenv import load_dotenv
#
from src.utils import get_absolute_dotenv_filepath

load_dotenv(dotenv_path=get_absolute_dotenv_filepath(), override=True)

### Get variables
INFLUX_DB_TOKEN:str|None = os.getenv('INFLUX_DB_TOKEN', '1337')
INFLUX_DB_HOST:str = os.getenv('INFLUX_DB_HOST', '127.0.0.1')
INFLUX_DB_ORG:str|None = os.getenv('INFLUX_DB_ORG', None)
INFLUX_DB_BUCKET:str|None = os.getenv('INFLUX_DB_BUCKET', None)
OPENWEATHERMAP_API_URL:str = os.getenv('OPENWEATHERMAP_API_URL', 'https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s')
OPENWEATHERMAP_API_TOKEN:str|None = os.getenv('OPENWEATHERMAP_API_TOKEN', None)
OPENWEATHERMAP_LOCATION_NAME:str = os.getenv('OPENWEATHERMAP_LOCATION_NAME', 'Berlin')
TIMEZONE:str = os.getenv('TIMEZONE', 'UTC')
PROXY_URL:str|None = os.getenv('PROXY_URL', None)
try:
    _req_timeout:int = int(os.getenv('REQUESTS_TIMEOUT', 10))
except (ValueError, TypeError):
    _req_timeout:int = 10
REQUESTS_TIMEOUT:int = _req_timeout
LOGGING_LEVEL:str = os.getenv('LOGGING_LEVEL', 'DEBUG')

### Functions


class ApiKeySanitizer(logging.Filter):
    def filter(self, record) -> bool:
        # Sanitize record.msg
        if record.msg:
            record.msg = re.sub(r"(appid=)[^&\s]+", r"\1[REDACTED]", str(record.msg))
        
        # Sanitize record.args, but only if they are strings
        if record.args:
            if isinstance(record.args, tuple):
                new_args = []
                for a in record.args:
                    if isinstance(a, str):
                        new_args.append(re.sub(r"(appid=)[^&\s]+", r"\1[REDACTED]", a))
                    else:
                        new_args.append(a)  # Keep numbers, etc. intact
                record.args = tuple(new_args)
            elif isinstance(record.args, str):
                record.args = re.sub(r"(appid=)[^&\s]+", r"\1[REDACTED]", record.args)
        return True
    
def configure_logger() -> None:
    """
    Configure logging module for this project.
    """
    # Prevent adding multiple handlers if this function is called multiple times
    if logging.getLogger().handlers:
        return
    
    # Create filter instance
    sanitizer = ApiKeySanitizer()

    # List of loggers to sanitize
    loggers_to_sanitize = ["urllib3.connectionpool", 
                           "requests.packages.urllib3.connectionpool",
                           "requests.packages.urllib3"]

    for name in loggers_to_sanitize:
        logger = logging.getLogger(name)
        logger.addFilter(sanitizer)
        logger.propagate = True
        # Optional: lower verbosity if you want
        #logger.setLevel(logging.DEBUG)

    
    handlers:list[logging.StreamHandler] = [logging.StreamHandler(sys.stdout)]  # stdout
    
    logging.basicConfig(
        level=LOGGING_LEVEL.upper(),
        format="(%(asctime)s) [%(levelname)s] %(name)s: %(message)s",
        handlers=handlers
    )
    
    