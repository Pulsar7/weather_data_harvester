"""

    Weather-Data-Harvester
    
    # Python-Version: 3.10.12

"""
import os, sys
import time, logging
from influxdb_client.rest import ApiException
#
import src.utils as utils
import src.http_handler as http_handler
from src.db_handler import InfluxDBHandler
from src.config import (TIMEZONE, OPENWEATHERMAP_API_URL)
from src.custom_exceptions import (InfluxDBAddingError, 
                                   WeatherDataParsingError,
                                   OpenWeatherMapAPIError,
                                   GetWeatherDataError)

def get_weather_data() -> dict:
    """
    Get current weather data.
    
    Raises:
        WeatherDataParsingError: If no weather-data could be gathered or on JSON parse failure.
    """
    try:
        data:dict = http_handler.fetch_weather_data()
    except (OpenWeatherMapAPIError, WeatherDataParsingError, GetWeatherDataError) as _e:
        raise WeatherDataParsingError("Got no weather-data to work with!") from _e
    
    timestamp:str = utils.get_current_timestamp(timezone=TIMEZONE)
    logging.debug(f"Current timestamp: {timestamp}")
    
    try:
        weather_data:dict = {
            "country": data['sys']['country'],                                                  # country
            "location_name": data['name'],                                                      # location_name
            "timestamp": timestamp,                                                             # current string-timestamp
            "longitude": data['coord']['lon'],                                                  # longitude
            "latitude": data['coord']['lat'],                                                   # latitude
            "weather_id": data['weather'][0]['id'],                                             # weather_id
            "weather_main_text": data['weather'][0]['main'],                                    # weather_main_text
            "weather_description": data['weather'][0]['description'],                           # weather_description
            "temperature_real": float(data['main']['temp']),                                    # temperature_real
            "temperature_feels_like": float(data['main']['feels_like']),                        # temperature_feels_like
            "temperature_min": float(data['main']['temp_min']),                                 # temperature_min
            "temperature_max": float(data['main']['temp_max']),                                 # temperature_max
            "pressure": data['main']['pressure'],                                               # pressure
            "humidity": int(data['main']['humidity']),                                          # humidity
            "sea_level": data['main']['sea_level'],                                             # sea_level
            "ground_level": data['main']['grnd_level'],                                         # ground_level
            "wind_speed": float(data['wind']['speed']),                                         # wind_speed
            "wind_degree": int(data['wind']['deg']),                                            # wind_degree
            "weather_data_src_url": utils.get_weather_data_source_url(OPENWEATHERMAP_API_URL)   # source-url (domain)
        }
        
    except (ValueError, TypeError) as _e:
        raise WeatherDataParsingError("Weather-Data parsing error!") from _e
    
    return weather_data

def add_data_to_db(weather_data:dict) -> None:
    """Add weather-data to database."""
    try:
        with InfluxDBHandler() as db:
            # Separate tags from fields
            tags:dict = {
                "country": weather_data['country'],
                "location_name": weather_data['location_name'],
                "weather_main_text": weather_data['weather_main_text'],
                "weather_data_source": weather_data['weather_data_src_url']
            }
            
            # Write temperature-related fields
            db.write_weather_point(
                measurement="temperature",
                tags=tags,
                fields={
                    "temperature_real": weather_data["temperature_real"],
                    "temperature_min": weather_data["temperature_min"],
                    "temperature_max": weather_data["temperature_max"],
                    "temperature_feels_like": weather_data["temperature_feels_like"],
                },
                timestamp=weather_data['timestamp']
            )

            # Write humidity and pressure related fields
            db.write_weather_point(
                measurement="atmosphere",
                tags=tags,
                fields={
                    "humidity": weather_data["humidity"],
                    "pressure": weather_data["pressure"],
                    "sea_level": weather_data.get("sea_level"), 
                    "ground_level": weather_data.get("ground_level"),
                },
                timestamp=weather_data['timestamp']
            )

            # Write wind related fields
            db.write_weather_point(
                measurement="wind",
                tags=tags,
                fields={
                    "wind_speed": weather_data["wind_speed"],
                    "wind_degree": weather_data["wind_degree"],
                },
                timestamp=weather_data['timestamp']
            )

            # Write weather condition identifiers
            db.write_weather_point(
                measurement="weather_condition",
                tags=tags,
                fields={
                    "weather_id": weather_data.get("weather_id"),
                    "weather_description": weather_data.get("weather_description"),
                },
                timestamp=weather_data['timestamp']
            )
            
            # Coordinates rarely change for a location, so tags might be better
            coord_tags = {
                **tags,
                "longitude": str(weather_data.get("longitude", "")),
                "latitude": str(weather_data.get("latitude", ""))
            }
            db.write_weather_point(
                measurement="location",
                tags=coord_tags,
                fields={},  # no fields, just tags
                timestamp=weather_data['timestamp']
            )
            
            logging.debug(f"Stored data in InfluxDB: timestamp='{weather_data['timestamp']}'")
        logging.info("Weather-data has been successfully stored in database.")
    
    except ApiException as _e:
        raise InfluxDBAddingError("Communication error with the database!") from _e
    
    except (ValueError, TypeError) as _e:
        raise InfluxDBAddingError("Invalid InfluxDB configuration!") from _e
    
    except KeyError as _e:
        raise InfluxDBAddingError("Missing weather-data-key!") from _e
    
    except Exception as _e:
        raise InfluxDBAddingError("An unexpected error occured while adding weather-data to InfluxDB") from _e

def main() -> None:
    _start:float = time.time()
    logging.debug(f"Started at {_start}")
    
    try:
        weather_data:dict = get_weather_data()
    except WeatherDataParsingError:
        logging.exception("Couldn't get weather-data!")
        logging.critical("Cannot operate without weather-data!")
        sys.exit(1)
    
    try:
        add_data_to_db(weather_data)
    except InfluxDBAddingError:
        logging.exception("Couldn't add weather-data to InfluxDB!")
    
    _delta:float = time.time() - _start
    logging.debug(f"Closed. (Runtime={_delta} seconds)")
    

if __name__ == '__main__':
    filename:str = os.path.basename(__file__)
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='(%(asctime)s) %(levelname)s [%(threadName)s] %(name)s.%(funcName)s: %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S'  # ISO8601-ish without timezone
    )
    
    logger = logging.getLogger(__name__)
    
    logging.debug(f"Running from {filename}")
    
    main()