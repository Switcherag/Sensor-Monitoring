import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

# MQTT settings
mqtt_broker = "test.mosquitto.org"
mqtt_topic = "SensorPolytech"

# InfluxDB settings
influxdb_host = "localhost"
influxdb_port = 8086
influxdb_database = "mydatabase"

# Create an InfluxDB client
influxdb_client = InfluxDBClient('localhost', 8086, 'admin', 'Password1', 'mydb')
influxdb_client.ping()
influxdb_client.switch_database(influxdb_database)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " " + str(msg.payload))

    # Store the message in InfluxDB
    json_body = [
        {
            "measurement": "mqtt_messages",
            "tags": {
                "topic": msg.topic
            },
            "fields": {
                "payload": msg.payload.decode("utf-8")
            }
        }
    ]
    influxdb_client.write_points(json_body)

# Create an MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the MQTT broker
mqtt_client.connect(mqtt_broker, 1883, 60)

# Start the MQTT loop
mqtt_client.loop_forever()
