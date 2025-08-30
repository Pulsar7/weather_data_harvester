import os
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