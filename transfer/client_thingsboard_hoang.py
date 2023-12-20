import paho.mqtt.client as mqtt
import json
import time
import random
import socket
# coap
import datetime
import logging
import asyncio
import aiocoap.resource as resource
from aiocoap.numbers.contentformat import ContentFormat
import aiocoap
# Khai bao cac bien Global, la cac message
temperature_inside = ""
humidity_inside = ""
temperature_outside = ""
humidity_outside = ""

def get_local_ip():
    try:
        # Get the local host name
        host_name = socket.gethostname()

        # Get the IP address of the local host
        local_ip = socket.gethostbyname(host_name)

        return local_ip

    except socket.error as e:
        print(f"Error: {e}")
        return None
local_broker_address = get_local_ip()
print(f"LOCAL IP: {local_broker_address}")
def on_connect_publish(client, userdata, flags, rc):
    if rc == 0:
        # print("Connected to publish MQTT broker")
        temp = 0
    else:
        print(f"Connection failed with error code {rc}")

def on_connect_subscribe(client, userdata, flags, rc):
    if rc == 0:
        # print("Connected to publish MQTT broker")
        temp = 1
        client.subscribe("local/topic1")
    else:
        print(f"Connection failed with error code {rc}")

def on_message(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    print(f"Received message on topic {msg.topic}: {msg.payload}")
    # if len(msg.payload) < 3:
    #     return msg.payload
    # else:
    #     return 0
    global temperature_inside
    temperature_inside = msg.payload
    external_payload = f'{{"humidity_in": {humidity_inside},"temperature_in": {temperature_inside}}}'
    # Print the result
    print(external_payload)
    # Publish telemetry data to Thingboard
    external_client.publish(telemetry_topic, external_payload, qos=1)
    # return msg.payload
    # Publish the received message to another topic on the publish broker
    # client.publish("phamcongtranghd@gmail.com/data", msg.payload)

def on_disconnect(client, userdata, rc):
    # print("Disconnected from MQTT broker")
    temp = 1
# Thingboard MQTT broker details
external_broker_address = "mqtt.thingsboard.cloud"
broker_port = 1883
username = "iot_g17"
password = "12345678"
external_client_id = "70k9jt9qh34w5njkdq4d"  # You can choose any unique client ID
# Mosquitto MQTT broker details
# local_broker_address = get_local_ip

# MQTT topic for publishing telemetry data
telemetry_topic = "v1/devices/me/sensor"

# Create MQTT client
external_client = mqtt.Client(external_client_id)
external_client.username_pw_set(username, password)
external_client.on_connect = on_connect_publish
external_client.on_disconnect = on_disconnect

local_client = mqtt.Client()
local_client.on_connect = on_connect_subscribe
local_client.on_disconnect = on_disconnect
local_client.on_message = on_message
# Connect to Thingboard MQTT broker
external_client.connect(external_broker_address, broker_port, 60)
external_client.loop_start()

local_client.connect(local_broker_address, 1883, 60)
local_client.loop_start()
# COAP
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
        coap_payload = request.payload.decode('utf-8')
        print('PUT payload CoAP: %s' % coap_payload)
        global humidity_inside
        humidity_inside = coap_payload
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=b"server_receive_put")

class server_get(resource.Resource):

    async def render_get(self, request):
        return aiocoap.Message(payload=b"server_receive_get")
logging.getLogger().addHandler(logging.NullHandler())

async def main():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(['put'], server_put())
    root.add_resource(['get'], server_get())
    await aiocoap.Context.create_server_context(root, bind=(local_broker_address, 5683))
    # Run forever
    await asyncio.Event().wait()
# while 1>0:
#     print("Wait")

if __name__ == "__main__":
    asyncio.run(main())
    try:
        while True:
            # Format the string with the random temperature
            # payload = f'{{"humidity_in": {random_humidity_inside},"temperature_in": {random_temperature_inside}, "humidity_out": {random_humidity_outside},"temperature_out": {random_temperature_outside}}}'
            external_payload = f'{{"humidity_in": {humidity_inside},"temperature_in": {temperature_inside}}}'
            print(external_payload)
            # Publish telemetry data to Thingboard
            external_client.publish(telemetry_topic, external_payload, qos=1)

            # Sleep for some time before publishing the next data (e.g., every 5 seconds)
            time.sleep(1)

    except KeyboardInterrupt:
        # Disconnect on keyboard interrupt
        external_client.disconnect()
        print("Disconnected from Thingboard MQTT broker")