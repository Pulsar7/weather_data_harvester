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
from src.custom_exceptions import (WeatherDataParsingError, 
                                   OpenWeatherMapAPIError,
                                   GetWeatherDataError)

logger = logging.getLogger(__name__)

def get_weather_data_source_url() -> str:
    """Get parsed weather-data source URL."""
    return urlparse(OPENWEATHERMAP_API_URL).netloc

def get_current_timestamp() -> str:
    """Get current timestamp in ISO8601 format."""
    return datetime.now(pytz.timezone(TIMEZONE)).isoformat()

def fetch_weather_data() -> dict:
    """
    Fetch weather-data of given location from the Openweathermap-API.
    
    Raises:
        OpenWeatherMapAPIError: On API/network errors or invalid/empty responses.
        WeatherDataParsingError: On JSON parse failure.
        GetWeatherDataError: On unexpected errors.
    """
    # HTTP GET-Request
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
                logger.debug(f"Response body: {resp.text}")
                raise OpenWeatherMapAPIError(f"Got invalid HTTP-status-code: {resp.status_code}")
            
            try:
                data = resp.json()
            except ValueError as _e:
                logger.debug(f"Raw response: {resp.text}")
                raise WeatherDataParsingError("Failed to parse received data as JSON!") from _e
            
            if not isinstance(data, dict) or not data:
                logger.debug(f"Raw response: {resp.text}")
                raise OpenWeatherMapAPIError("Got invalid or empty response from API!")
    
    except (OpenWeatherMapAPIError, WeatherDataParsingError):
        raise # re-raise them unchanged
    
    except (requests.ConnectionError, requests.RequestException) as _e:
        raise OpenWeatherMapAPIError("Network connection error") from _e
        
    except Exception as _e:
        raise GetWeatherDataError("An unexpected error occured while receiving weather-data from API!") from _e
    
    
    # Successfully gathered weather-data from API.
    return data