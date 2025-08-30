class InfluxDBAddingError(Exception):
    """Raised when weather-data couldn't be added to InfluxDB."""
    pass

class GetWeatherDataError(Exception):
    """Raised when something went wrong while harvesting weather-data."""
    pass

class WeatherDataParsingError(GetWeatherDataError):
    """Raised when weather-data couldn't be parsed."""
    pass

class OpenWeatherMapAPIError(GetWeatherDataError):
    """Raised when communication with the Openweathermap-API failed."""
    pass