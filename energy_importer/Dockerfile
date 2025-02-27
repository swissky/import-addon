FROM python:3.10-slim
WORKDIR /app

# Installiere benötigte Systempakete für Pandas & SQLite
RUN apt-get update && apt-get install -y \
	gcc \
	libsqlite3-dev \
	python3-dev \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
CMD ["python", "app.py"]