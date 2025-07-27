from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point, WritePrecision
#
from src.config import (
    INFLUX_DB_HOST,
    INFLUX_DB_TOKEN,
    INFLUX_DB_ORG,
    INFLUX_DB_BUCKET
)

class InfluxDBHandler:
    """InfluxDB-Handler for storing weather data."""

    def __init__(self) -> None:
        self.client = InfluxDBClient(
            url=INFLUX_DB_HOST,
            token=INFLUX_DB_TOKEN,
            org=INFLUX_DB_ORG
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        
        # Validate connection immediately
        self.client.ping()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def write_weather_point(self, measurement:str, tags:dict, fields:dict, timestamp=None) -> None:
        """Write weather-point."""
        point = Point(measurement)
        
        for k, v in tags.items():
            point = point.tag(k, v)

        for k, v in fields.items():
            point = point.field(k, v)

        if timestamp:
            point = point.time(timestamp, WritePrecision.S)

        self.write_api.write(bucket=INFLUX_DB_BUCKET, record=point)

    def close(self):
        self.client.close()