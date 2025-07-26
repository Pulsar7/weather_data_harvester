import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./.env', override=True)

### Get variables
INFLUX_DB_TOKEN:str|None = os.getenv('INFLUX_DB_TOKEN', '1337')
INFLUX_DB_HOST:str = os.getenv('INFLUX_DB_HOST', '127.0.0.1')
INFLUX_DB_ORG:str|None = os.getenv('INFLUX_DB_ORG', None)
INFLUX_DB_BUCKET:str|None = os.getenv('INFLUX_DB_BUCKET', None)