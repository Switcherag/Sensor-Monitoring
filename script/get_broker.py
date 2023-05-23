import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to the "SensorPolytech" topic
    client.subscribe("SensorPolytech")

def on_message(client, userdata, msg):
    print("Topic: " + msg.topic + " - Message: " + str(msg.payload))

# Create an MQTT client
client = mqtt.Client()

# Set up callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect("test.mosquitto.org", 1883, 60)

# Start the loop to process incoming messages
client.loop_forever()
