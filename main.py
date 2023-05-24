import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

import time
# MQTT settings
mqtt_broker = "test.mosquitto.org"
mqtt_topic = "SensorPolytech"
dbname = "mydb"
#Setup database
influxdb_client = InfluxDBClient('localhost', 8086, 'admin', 'Password1', 'mydb')
influxdb_client.create_database('mydb')
influxdb_client.get_list_database()
influxdb_client.switch_database('mydb')


# Check if the database exists
database_list = influxdb_client.get_list_database()
database_exists = any(db['name'] == dbname for db in database_list)

# Create the database if it does not exist
if not database_exists:
    influxdb_client.create_database(dbname)



influxdb_client.switch_database(dbname)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("SensorPolytech/+")


def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " " + str(msg.payload))

    # Get the current timestamp
    timestamp = int(time.time() * 1000)  # Convert to milliseconds

    # Store the message in InfluxDB
    json_body = [
        {
            "measurement": "mqtt_messages",
            "tags": {
                "topic": msg.topic
            },
            "time": timestamp,
            "fields": {
                "value": msg.payload.decode("utf-8")
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
