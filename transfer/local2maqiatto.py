import paho.mqtt.client as mqtt

# Define the callback functions for the subscribe client
def on_connect_subscribe(client, userdata, flags, rc):
    print(f"Connected to Subscribe Broker with result code {rc}")
    client.subscribe("local/topic1")

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload}")
    
    # Publish the received message to another topic on the publish broker
    publish_client.publish("phamcongtranghd@gmail.com/data", msg.payload)

# Define the callback function for the publish client
def on_connect_publish(client, userdata, flags, rc):
    print(f"Connected to Publish Broker with result code {rc}")

# Create subscribe and publish clients
subscribe_client = mqtt.Client()
subscribe_client.on_connect = on_connect_subscribe
subscribe_client.on_message = on_message

publish_client = mqtt.Client()
publish_client.on_connect = on_connect_publish

# Set the credentials and connection information for both brokers
#subscribe_client.username_pw_set("subscribe_username", "subscribe_password")
subscribe_client.connect("192.168.168.43", 1883, 60)

publish_client.username_pw_set("phamcongtranghd@gmail.com", "externalbroker")
publish_client.connect("maqiatto.com", 1883, 60)

# Start the loop for both clients
subscribe_client.loop_start()
publish_client.loop_start()

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    # Disconnect clients on keyboard interrupt
    subscribe_client.disconnect()
    publish_client.disconnect()