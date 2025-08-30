import pytz
import logging
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

def get_weather_data_source_url(openweathermap_api_url:str) -> str:
    """Get parsed weather-data source URL."""
    return urlparse(openweathermap_api_url).netloc

def get_current_timestamp(timezone:str) -> str:
    """
    Get current timestamp in ISO8601 format.
    
    If an invalid timezone is given, the fallback timezone `UTC` is being used.
    """
    try:
        timestamp:str = datetime.now(pytz.timezone(timezone)).isoformat()
    except pytz.UnknownTimeZoneError:
        logger.exception(f"Given timezone '{timezone}' is invalid!")
        logger.warning("Using fallback timezone UTC")
        timestamp:str = datetime.now(pytz.timezone("UTC")).isoformat()
    
    return timestamp

def get_absolute_dotenv_filepath() -> Path:
    """
    Get absolute filepath of the dotenv-file.
    """
    
    return Path(__file__).resolve().parent.parent / ".env"