import pytz
import logging
import requests
from datetime import datetime
from urllib.parse import urlparse
#
from src.config import (
    OPENWEATHERMAP_API_URL,
    OPENWEATHERMAP_API_TOKEN,
    OPENWEATHERMAP_LOCATION_NAME,
    PROXY_URL,
    REQUESTS_TIMEOUT,
    TIMEZONE
)

def get_weather_data_source_url() -> str:
    """Get parsed weather-data source URL."""
    return urlparse(OPENWEATHERMAP_API_URL).netloc

def get_current_timestamp() -> str:
    """Get current timestamp in ISO8601 format."""
    return datetime.now(pytz.timezone(TIMEZONE)).isoformat()

def get_weather_data() -> tuple[dict|None, bool]:
    """Get weather-data of given location."""
    # Get HTTP-Request
    try:
        with requests.Session() as session:
            # Set proxy-settings
            if PROXY_URL:
                session.proxies = {
                    'http': PROXY_URL,
                    'https': PROXY_URL
                }
            
            url:str = f"{OPENWEATHERMAP_API_URL % (OPENWEATHERMAP_LOCATION_NAME, OPENWEATHERMAP_API_TOKEN)}"
            resp = session.get(url=url, timeout=REQUESTS_TIMEOUT)
            if resp.status_code != 200:
                logging.error(f"Got invalid HTTP-status-code: {resp.status_code}")
                logging.debug(f"Response body: {resp.text}")
                return (None, False)
            
            try:
                data = resp.json()
            except ValueError as _e:
                logging.error(f"Failed to parse JSON: {_e}")
                logging.debug(f"Raw response: {resp.text}")
                return (None, False)
            
            if not isinstance(data, dict) or not data:
                logging.error(f"Got invalid or empty response from API: {type(data)} -> {data}")
                return (None, False)
            
            return (data, True)
            
    except (requests.ConnectionError, requests.RequestException) as _e:
        logging.error(f"OpenWeatherMap-API-Error: {type(_e).__name__}: {_e}")
    except Exception as _e:
        logging.error(f"An unexpected error occured: {type(_e).__name__}: {_e}")
    
    return (None, False)