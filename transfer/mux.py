#!/usr/bin/python3 
import paho.mqtt.client as mqtt

import datetime
import logging
import asyncio
import aiocoap.resource as resource
from aiocoap.numbers.contentformat import ContentFormat
import aiocoap
payload=""
class server_put(resource.Resource):
    def __init__(self):
        super().__init__()
        self.set_content(b"This is the resource's default content. It is padded "
                b"with numbers to be large enough to trigger blockwise "
                b"transfer.\n")

    def set_content(self, content):
        self.content = content
        while len(self.content) <= 1024:
            self.content = self.content + b"0123456789\n"

    async def render_put(self, request):
        payload = request.payload.decode('utf-8')
        print('PUT payload: %s' % payload)
        publish_client.publish("phamcongtranghd@gmail.com/data", payload)
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=b"server_receive_put")

class server_get(resource.Resource):

    async def render_get(self, request):
        return aiocoap.Message(payload=b"server_receive_get")

logging.getLogger().addHandler(logging.NullHandler())

# Define the callback functions for the subscribe client
def on_connect_subscribe(client, userdata, flags, rc):
    print(f"Connected to Subscribe Broker with result code {rc}")
    client.subscribe("local/topic1")

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload}")
    
    # Publish the received message to another topic on the publish broker
    publish_client.publish("phamcongtranghd@gmail.com/data", msg.payload)
    # publish_client.publish("phamcongtranghd@gmail.com/data", payload)

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
subscribe_client.connect("192.168.66.243", 1883, 60)

publish_client.username_pw_set("phamcongtranghd@gmail.com", "externalbroker")
publish_client.connect("maqiatto.com", 1883, 60)

# Start the loop for both clients
subscribe_client.loop_start()
publish_client.loop_start()


async def main():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(['put'], server_put())
    root.add_resource(['get'], server_get())
    await aiocoap.Context.create_server_context(root, bind=('192.168.66.243', 5683))
    # Run forever
    await asyncio.get_running_loop().create_future()
if __name__ == "__main__":
    asyncio.run(main())
# Keep the script running
# try:
#     while True:
#         pass
# except KeyboardInterrupt:
#     # Disconnect clients on keyboard interrupt
#     subscribe_client.disconnect()
#     publish_client.disconnect()