import os
import sqlite3
import pandas as pd
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Konfiguration aus Umgebungsvariablen
DB_PATH = "/config/home-assistant_v2.db"
CSV_FILE = "/config/import_data.csv"
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://192.168.1.xx:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "your-token")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "your-org")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "homeassistant")

def import_to_sqlite():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    df = pd.read_csv(CSV_FILE)
    
    for _, row in df.iterrows():
        timestamp = int(float(row["start_ts"]))
        state = row["state"]
        sum_value = row["sum"]
        
        cursor.execute("""
            INSERT INTO statistics (created, created_ts, metadata_id, start, start_ts, state, sum)
            VALUES (datetime('now'), ?, (SELECT id FROM statistics_meta WHERE statistic_id = 'sensor.gplugd_z_ei'), ?, ?, ?, ?)
        """, (timestamp, timestamp, timestamp, state, sum_value))
    
    conn.commit()
    conn.close()
    print("✅ Erfolgreich in SQLite importiert!")

def import_to_influxdb():
    client = influxdb_client.InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    df = pd.read_csv(CSV_FILE)
    
    for _, row in df.iterrows():
        point = influxdb_client.Point("energy_consumption") \
            .tag("sensor", "sensor.gplugd_z_ei") \
            .field("state", row["state"]) \
            .field("sum", row["sum"]) \
            .time(int(float(row["start_ts"])), influxdb_client.WritePrecision.S)
        
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
    
    client.close()
    print("✅ Erfolgreich in InfluxDB importiert!")

if __name__ == "__main__":
    target = os.getenv("TARGET", "both")
    if target in ["sqlite", "both"]:
        import_to_sqlite()
    if target in ["influxdb", "both"]:
        import_to_influxdb()