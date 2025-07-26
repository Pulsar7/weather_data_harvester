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
        self.write_api = self.client.write_api()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def write_weather_point(self, location:str, fields:dict, timestamp=None) -> None:
        point = Point("weather").tag("location", location)

        for k, v in fields.items():
            point = point.field(k, v)

        if timestamp:
            point = point.time(timestamp, WritePrecision.S)

        self.write_api.write(bucket=INFLUX_DB_BUCKET, record=point)

    def close(self):
        self.client.close()