import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from grafana_api.grafana_face import GrafanaFace

# InfluxDB connection settings
influxdb_host = 'localhost'
influxdb_port = 8086
influxdb_database = 'mydb'

# Grafana connection settings
grafana_url = 'http://localhost:3000'
grafana_api_key = 'YOUR_API_KEY'

# Create InfluxDB client
influxdb_client = InfluxDBClient(host=influxdb_host, port=influxdb_port)

# Create Grafana client
grafana_client = GrafanaFace(auth=grafana_api_key, host=grafana_url)

def store_influxdb(topic, message):
    json_body = [
        {
            "measurement": "sensor_data",
            "tags": {
                "topic": topic
            },
            "fields": {
                "value": float(message)
            }
        }
    ]
    influxdb_client.write_points(json_body, database=influxdb_database)
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to "SensorPolytech/+" to capture all parameters
    client.subscribe("SensorPolytech/+")

def on_message(client, userdata, msg):
    print("Topic: " + msg.topic + " - Message: " + str(msg.payload))
    store_influxdb(msg.topic, str(msg.payload))

# Create MQTT client
mqtt_client = mqtt.Client()

# Set up callback functions
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the MQTT broker
mqtt_client.connect("test.mosquitto.org", 1883, 60)

# Start the MQTT client loop
mqtt_client.loop_start()
