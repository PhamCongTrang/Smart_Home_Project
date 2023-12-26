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
#Json
import json
# Khai bao cac bien Global, la cac message
temperature_inside = 0
humidity_inside = 0
temperature_outside = 0
humidity_outside = 0
socket_cmd = 0
pump_cmd = 0
zero_Doc = '{}'
inside_sub_doc = json.loads(zero_Doc)
outside_sub_doc = json.loads(zero_Doc)
inside_pub_doc = json.loads(zero_Doc)
outside_pub_doc = json.loads(zero_Doc)
thingsboard_sub_doc = json.loads(zero_Doc)
thingsboard_pub_doc = json.loads(zero_Doc)
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
local_ip = get_local_ip()
print(f"LOCAL IP: {local_ip}")
#####-----------------FORWARD--------------------------------------#
def on_connect_external_publish(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to publish Thingsboard MQTT broker")
    else:
        print(f"Connection failed with error code {rc}")

def on_connect_local_subscribe(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to subscribe local MQTT broker")
        client.subscribe("local/topic1")
    else:
        print(f"Connection failed with error code {rc}")

def on_message_local_subscribe(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")

    global temperature_inside
    global humidity_inside
    inside_sub_doc = json.loads(msg.payload)
    temperature_inside = inside_sub_doc["temperature_inside"]
    humidity_inside = inside_sub_doc["humidity_inside"]

    external_pub_payload = f'{{"temperature_inside":{temperature_inside},"humidity_inside":{humidity_inside},"temperature_outside":{temperature_outside},"humidity_outside":{humidity_outside}}}'
    external_pub_client.publish(telemetry_pub_topic, external_pub_payload, qos = 1)
    print(external_pub_payload) #nguyen nhan khac cung lam timeline thingsboard khong ve do thi
#####-----------------REVERSE--------------------------------------#
def on_connect_local_publish(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to publish local MQTT broker")
        local_pub_client.publish(local_pub_topic, "HELLO", qos=1)
    else:
        print(f"Connection failed with error code {rc}")

def on_connect_external_subscribe(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to subscribe MAQIATTO MQTT broker")
        client.subscribe(telemetry_sub_topic) # client.sub
    else:
        print(f"Connection failed with error code {rc}")

def on_message_external_subscribe(client, userdata, msg):
    # msg.payload = msg.payload.decode("utf-8")
    print(f"Received message on topic {msg.topic}: {msg.payload}")

    global socket_cmd
    global pump_cmd
    socket_cmd = msg.payload
    pump_cmd = msg.payload
    # local_pub_payload = f'{{"humidity_in": {humidity_inside},"temperature_in": {temperature_inside}}}'
    local_pub_payload = socket_cmd
    print(local_pub_payload)
    local_pub_client.publish(local_pub_topic, local_pub_payload, qos=1)

def on_disconnect(client, userdata, rc):
    print(f"Disconnected from MQTT broker")
    temp = 1
##--------------------EXTERNAL CLIENT-----------------------------------------##
###############################################################################
# 1. FORWARD
# Thingboard MQTT broker details
external_pub_broker_address = "mqtt.thingsboard.cloud"
external_pub_username = "iot_g17"
external_pub_password = "12345678"
external_pub_client_id = "70k9jt9qh34w5njkdq4d"
# MQTT topic for publishing telemetry data
telemetry_pub_topic = "v1/devices/me/sensor"
# Create MQTT client
external_pub_client = mqtt.Client(external_pub_client_id)
external_pub_client.username_pw_set(external_pub_username, external_pub_password)
external_pub_client.on_connect = on_connect_external_publish
external_pub_client.on_disconnect = on_disconnect
external_pub_client.connect(external_pub_broker_address, 1883, 60)
external_pub_client.loop_start()
# 2. REVERSE
# Thingboard MQTT broker details
external_sub_broker_address = "maqiatto.com"
external_sub_username = "phamcongtranghd@gmail.com" # fix 3 dong nay, cho Hoang cung cap user, password, id
external_sub_password = "externalbroker"
external_sub_client_id = "mqttx_20002"
# MQTT topic for publishing telemetry data
telemetry_sub_topic = "phamcongtranghd@gmail.com/cmd" # de y topic
# Create MQTT client
external_sub_client = mqtt.Client(external_sub_client_id)
external_sub_client.username_pw_set(external_sub_username, external_sub_password)
external_sub_client.on_connect = on_connect_external_subscribe
external_sub_client.on_disconnect = on_disconnect
external_sub_client.on_message = on_message_external_subscribe
external_sub_client.connect(external_sub_broker_address, 1883, 60)
external_sub_client.loop_start()
##------------------LOCAL CLIENT----------------------------------------------##
################################################################################
# 1. FORWARD
local_broker_address = local_ip
# non user
# non password
# non id
local_sub_topic = "local/topic1"
local_sub_client = mqtt.Client("local1")
local_sub_client.on_connect = on_connect_local_subscribe
local_sub_client.on_disconnect = on_disconnect
local_sub_client.on_message = on_message_local_subscribe
local_sub_client.connect(local_broker_address, 1883, 60)
local_sub_client.loop_start()
# 2. REVERSE
local_broker_address = local_ip
# non user
# non password
# non id
local_pub_topic = "local/topic2"
local_pub_client = mqtt.Client("local2")
local_pub_client.on_connect = on_connect_local_publish
local_pub_client.on_disconnect = on_disconnect
# publish don't need on_message
local_pub_client.connect(local_broker_address, 1883, 60)
local_pub_client.loop_start()
###############################################################################
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
        # print('PUT payload CoAP: %s' % coap_payload) // bat dong nay se lam thingsboard khong ve duoc do thi
        global temperature_outside
        global humidity_outside
        inside_sub_doc = json.loads(coap_payload)
        temperature_outside = inside_sub_doc["temperature_outside"]
        humidity_outside = inside_sub_doc["humidity_outside"]
        # humidity_inside = coap_payload
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload = pump_cmd)

class server_get(resource.Resource):

    async def render_get(self, request):
        return aiocoap.Message(payload = pump_cmd)
logging.getLogger().addHandler(logging.NullHandler())

async def main():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(['put'], server_put())
    root.add_resource(['get'], server_get())
    await aiocoap.Context.create_server_context(root, bind=(local_ip, 5683))
    # Run forever
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
    try:
        while True:
            # Format the string with the random temperature
            # payload = f'{{"humidity_in": {random_humidity_inside},"temperature_in": {random_temperature_inside}, "humidity_out": {random_humidity_outside},"temperature_out": {random_temperature_outside}}}'
            # external_pub_payload = f'{{"humidity_in": {humidity_inside},"temperature_in": {temperature_inside}}}'
            # print(external_pub_payload)
            # # Publish telemetry data to Thingboard
            # external_pub_client.publish(telemetry_topic, external_pub_payload, qos=1)

            # Sleep for some time before publishing the next data (e.g., every 5 seconds)
            time.sleep(1)

    except KeyboardInterrupt:
        # Disconnect on keyboard interrupt
        external_pub_client.disconnect()
        print("Disconnected from Thingboard MQTT broker")