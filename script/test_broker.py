import paho.mqtt.client as mqtt

# Create an MQTT client
client = mqtt.Client()

# Connect to the broker
client.connect("test.mosquitto.org", 1883, 60)

# Publish a message to the "SensorPolytech" topic
topic = "SensorPolytech"
message = "Hello, MQTT!"
client.publish(topic, message)

# Disconnect from the broker
client.disconnect()