# Weather-Data-Harvester


## Description

A simple API-client that gets current weather-data from the [openweathermap.org](https://openweathermap.org/)-API and stores it in an __InfluxDB__ time-series database.

> ⚠️ Warning: Using `DEBUG` logging level will expose sensitive data, such as your OpenWeatherMap API key, in the logs!

## Usage

```SHELL
git clone https://github.com/Pulsar7/weather_data_harvester.git
python3 -m venv .venv && source .venv/bin/activate
cd weather_data_harvester/
pip install -r requirements.txt
```

Copy `.sample.env` & adjust it to your own values:
```SHELL
cp .sample.env .env
nano .env
```

```SHELL
python3 harvester.py
```

## Example implementation

1. Create `InfluxDB` & `Grafana` docker-container.
2. Run `harvester.py` as __cronjob__ or __systemd__-timed-service (**recommended**)

Example `docker-compose.yaml`-file for __InfluxDB__ & __Grafana__:
```YAML
services:
  influxdb:
    image: influxdb:2.7
    container_name: influxdb
    ports:
      - "8086:8086"  # For Python script access
    volumes:
      - influxdb-data:/var/lib/influxdb2
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup
      - DOCKER_INFLUXDB_INIT_USERNAME=admin
      - DOCKER_INFLUXDB_INIT_PASSWORD=admin123
      - DOCKER_INFLUXDB_INIT_ORG=openweathermap-api-harvester
      - DOCKER_INFLUXDB_INIT_BUCKET=my-bucket
      - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-token
    restart: unless-stopped
    networks:
      - monitoring

  grafana:
    image: grafana/grafana-oss:latest
    container_name: grafana
    ports:
      - "3000:3000"  # Grafana UI
    volumes:
      - grafana-storage:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin123
    restart: unless-stopped
    networks:
      - monitoring

volumes:
  influxdb-data:
  grafana-storage:

networks:
  monitoring:
```
