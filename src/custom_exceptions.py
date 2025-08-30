class InfluxDBAddingError(Exception):
    """Raise when weather-data couldn't be added to InfluxDB."""
    pass

class WeatherDataParsingError(Exception):
    """Raise when weather-data couldn't be parsed."""
    pass