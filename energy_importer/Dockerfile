FROM python:3.10-slim
WORKDIR /app

# Installiere Systembibliotheken für Pandas & InfluxDB
RUN apt-get update && apt-get install -y \
	gcc \
	libsqlite3-dev \
	python3-dev \
	&& rm -rf /var/lib/apt/lists/*

# Installiere Python-Pakete direkt hier
RUN pip install --no-cache-dir pandas influxdb-client

COPY app.py .
CMD ["python", "app.py"]