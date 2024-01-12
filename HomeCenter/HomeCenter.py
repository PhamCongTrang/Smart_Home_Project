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
# Check Internet
import requests
Internet_State = 0
def check_internet_connection():
    try:
        # Send a request to a known server (Google's public DNS server)
        response = requests.get("http://www.google.com", timeout=5)
        # If the status code is 200, the request was successful
        return response.status_code == 200
    except requests.ConnectionError:
        # Connection error means no internet connection
        return False

# Check internet connection
if check_internet_connection():
    print("Internet connection is available.")
    Internet_State = 1
else:
    print("No internet connection.")
    Internet_State = -1
# Khai bao cac bien Global, la cac message
temperature_inside = 0
humidity_inside = 0
temperature_outside = 0
humidity_outside = 0
socket_cmd_set = 0
socket_cmd_get = 0
pump_cmd_set = 0
pump_cmd_get = 0
interval_time_inside_set = 1000
interval_time_outside_set = 1000
temperature_threshold_inside_set = 0
temperature_threshold_outside_set = 0

zero_Doc = '{}'
inside_sub_doc = json.loads(zero_Doc)
outside_sub_doc = json.loads(zero_Doc)
# inside_pub_doc = json.loads(zero_Doc)
# outside_pub_doc = json.loads(zero_Doc)
thingsboard_sub_doc = json.loads(zero_Doc)
# thingsboard_pub_doc = json.loads(zero_Doc)
outside_cmd_payload = 1 #kieu byte
# pub doc is not necessary
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
########################################################################################
###                                    FORWARD                                       ###
###                                    PROGRAM                                       ###
###                        DATA FROM DEVICE TO THINGSBOARD                           ###
########################################################################################
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

    # global temperature_inside
    # global humidity_inside
    global socket_cmd_get
    global pump_cmd_get
    inside_sub_doc = json.loads(msg.payload)
    temperature_inside = inside_sub_doc["temperature_inside"]
    humidity_inside = inside_sub_doc["humidity_inside"]
    # socket_cmd_get = inside_sub_doc["socket_cmd_get"]
    socket_cmd_get = inside_sub_doc.get("socket_cmd_get",0)
    external_pub_payload = f'{{"temperature_inside":{temperature_inside},"humidity_inside":{humidity_inside},"temperature_outside":{temperature_outside},"humidity_outside":{humidity_outside}}}'
    if socket_cmd_get != 0:
        if socket_cmd_get == 1:
            socket_cmd_get = random.randint(1, 1000)
        if socket_cmd_get == -1:
            socket_cmd_get = random.randint(-1000, -1)
        response_payload = f'{{"socket_cmd_get":{socket_cmd_get}}}'
    if pump_cmd_get != 0:
        if pump_cmd_get == 1:
            pump_cmd_get = random.randint(1, 1000)
        if pump_cmd_get == -1:
            pump_cmd_get = random.randint(-1000, -1)
        response_payload = f'{{"pump_cmd_get":{pump_cmd_get}}}'
    if Internet_State == 1:
        external_pub_client.publish(telemetry_pub_topic, external_pub_payload, qos = 2)
        if socket_cmd_get != 0 or pump_cmd_get != 0:
            external_sub_client.publish(response_topic, response_payload, qos = 1)
            print(response_payload)
    print(external_pub_payload) #nguyen nhan khac cung lam timeline thingsboard khong ve do thi
    
##############################################################################
##                     CONTROL PROGRAM OFFLINE                              ##
##############################################################################
def on_message_local_subscribe_offline(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")

    global temperature_inside, humidity_inside, temperature_outside, humidity_outside, socket_cmd, pump_cmd, interval_time_inside, interval_time_outside
    global temperature_threshold_inside_set, temperature_threshold_outside_set
    global outside_cmd_payload
    inside_sub_doc = json.loads(msg.payload)
    temperature_inside = inside_sub_doc["temperature_inside"]
    humidity_inside = inside_sub_doc["humidity_inside"]

    external_pub_payload = f'{{"temperature_inside":{temperature_inside},"humidity_inside":{humidity_inside},"temperature_outside":{temperature_outside},"humidity_outside":{humidity_outside}}}'
    print(external_pub_payload) #nguyen nhan khac cung lam timeline thingsboard khong ve do thi
    
    
    if temperature_outside > temperature_threshold_outside_set:
        pump_cmd_set = 1
    elif temperature_outside < temperature_threshold_outside_set - 5:
        pump_cmd_set = -1

    if temperature_inside > temperature_threshold_inside_set:
        socket_cmd_set = -1
    elif temperature_inside < temperature_threshold_inside_set - 5:
        socket_cmd_set = 1


    local_pub_payload = f'{{"interval_time_inside_set":1000,"socket_cmd_set":{socket_cmd_set}}}'
    outside_cmd_payload = bytes(f'{{"interval_time_outside_set":1000,"pump_cmd_set": {pump_cmd_set}}}','utf-8')#problem here // COAP message 

    print(local_pub_payload)
    print(outside_cmd_payload)
    local_pub_client.publish(local_pub_topic, local_pub_payload, qos=1)

########################################################################################
###                                    REVERSE                                       ###
###                                    PROGRAM                                       ###
###                        DATA FROM THINGSBOARD TO DEVICE                           ###
########################################################################################
def on_connect_local_publish(client, userdata, flags, rc):

    if rc == 0:
        print("Connected to publish local MQTT broker")
        local_pub_client.publish(local_pub_topic, "HELLO", qos=1)
    else:
        print(f"Connection failed with error code {rc}")

def on_connect_external_subscribe(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to subscribe Thingsboard MQTT broker")
        client.subscribe(telemetry_sub_topic) # client.sub
    else:
        print(f"Connection failed with error code {rc}")

def on_message_external_subscribe(client, userdata, msg):
    # msg.payload = msg.payload.decode("utf-8")
    print(f"Received message on topic {msg.topic}: {msg.payload}")

    global socket_cmd_set, pump_cmd_set
    global interval_time_inside_set, interval_time_outside_set
    global temperature_threshold_inside_set, temperature_threshold_outside_set
    
    global outside_cmd_payload
    thingsboard_sub_doc = json.loads(msg.payload)
    if thingsboard_sub_doc["params"] is not None:
        if thingsboard_sub_doc["method"] == "socket_cmd_set":
            socket_cmd_set = thingsboard_sub_doc["params"]
        else:
            socket_cmd_set = 0
        if thingsboard_sub_doc["method"] == "pump_cmd_set":
            pump_cmd_set = thingsboard_sub_doc["params"]
        else:
            pump_cmd_set = 0
        if thingsboard_sub_doc["method"] == "interval_time_inside_set":
            interval_time_inside_set = int(thingsboard_sub_doc["params"])
        if thingsboard_sub_doc["method"] == "interval_time_outside_set":
            interval_time_outside_set = int(thingsboard_sub_doc["params"])
        if thingsboard_sub_doc["method"] == "temperature_threshold_inside_set":
            itemperature_threshold_inside_set = int(thingsboard_sub_doc["params"])
        if thingsboard_sub_doc["method"] == "temperature_threshold_outside_set":
            temperature_threshold_outside_set = int(thingsboard_sub_doc["params"])
    # socket_cmd = thingsboard_sub_doc["socket_cmd"]
    # pump_cmd = thingsboard_sub_doc["pump_cmd"]
    # interval_time_inside = thingsboard_sub_doc["interval_time_inside"]
    # interval_time_outside = thingsboard_sub_doc["interval_time_outside"]

    response_topic = "v1/devices/me/rpc/response/" + msg.topic.split("/")[-1]
    client.publish(response_topic, "Response payload")
    

    local_pub_payload = f'{{"interval_time_inside_set": {interval_time_inside_set},"socket_cmd_set": {socket_cmd_set}}}'
    outside_cmd_payload = bytes(f'{{"interval_time_outside_set": {interval_time_outside_set},"pump_cmd_set": {pump_cmd_set}}}','utf-8')#problem here // COAP message 
    # outside_cmd_payload = msg.payload
    
    print(local_pub_payload)
    print(outside_cmd_payload)
    
    local_pub_client.publish(local_pub_topic, local_pub_payload, qos=1)

def on_disconnect(client, userdata, rc):
    print(f"Disconnected from MQTT broker")
    temp = 1

########################################################################################
###                              CHECK INTERNET CONECTION                            ###
###                                        AND                                       ###
###                               INIT MQTT CONECTION                                ###
########################################################################################
if Internet_State == 1:
    ##--------------------CONNECT TO EXTERNAL CLIENT------------------------------##
    # 1. FORWARD
    # a. Publish to sensors
    # Thingboard MQTT broker details
    external_pub_broker_address = "thingsboard.hust-2slab.org"
    external_pub_username = "iot_g17_1"
    external_pub_password = "12345678"
    external_pub_client_id = "homecenter"
    # MQTT topic for publishing telemetry data
    telemetry_pub_topic = "v1/devices/me/sensor"
    # Create MQTT client
    external_pub_client = mqtt.Client(external_pub_client_id)
    external_pub_client.username_pw_set(external_pub_username, external_pub_password)
    external_pub_client.on_connect = on_connect_external_publish
    external_pub_client.on_disconnect = on_disconnect
    external_pub_client.connect(external_pub_broker_address, 1883, 60)
    external_pub_client.loop_start()

    # b. Publish to response cmd
    # response_broker_address = "thingsboard.hust-2slab.org"t
    # response_username = "iot_g17_2"
    # response_password = "12345678"
    # response_client_id = "command"
    response_topic = "v1/devices/me/cmd"
    # response_client = mqtt.Client(response_client_id)
    # response_client.username_pw_set(response_username, response_password)
    # response_client.on_connect = on_connect_external_publish
    # response_client.on_disconnect = on_disconnect
    # response_client.connect(response_broker_address, 1883, 60)
    # response_client.loop_start()

    # 2. REVERSE
    # Thingboard MQTT broker details
    external_sub_broker_address = "thingsboard.hust-2slab.org"
    external_sub_username = "iot_g17_2" # fix 3 dong nay, cho Hoang cung cap user, password, id
    external_sub_password = "12345678"
    external_sub_client_id = "command"
    # MQTT topic for publishing telemetry data
    telemetry_sub_topic = "v1/devices/me/rpc/request/+" # de y topic
    # Create MQTT client
    external_sub_client = mqtt.Client(external_sub_client_id)
    external_sub_client.username_pw_set(external_sub_username, external_sub_password)
    external_sub_client.on_connect = on_connect_external_subscribe
    external_sub_client.on_disconnect = on_disconnect
    external_sub_client.on_message = on_message_external_subscribe
    external_sub_client.connect(external_sub_broker_address, 1883, 60)
    external_sub_client.loop_start()

    ##------------------CONNECT TO LOCAL CLIENT------------------------------------##
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
if Internet_State == -1:
    ##------------------ONLY CONNECT TO LOCAL CLIENT-----------------------------##
    # 1. FORWARD
    local_broker_address = local_ip
    # non user
    # non password
    # non id
    local_sub_topic = "local/topic1"
    local_sub_client = mqtt.Client("local1")
    local_sub_client.on_connect = on_connect_local_subscribe
    local_sub_client.on_disconnect = on_disconnect
    local_sub_client.on_message = on_message_local_subscribe_offline
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

########################################################################################
###                                      COAP PROTOCOL                               ###
###                                                                                  ###
###                                                                                  ###
########################################################################################
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
        # print('PUT payload CoAP: %s' % coap_payload) #bat dong nay se lam thingsboard khong ve duoc do thi
        global temperature_outside
        global humidity_outside
        global pump_cmd_get
        outside_sub_doc = json.loads(coap_payload)
        temperature_outside = outside_sub_doc["temperature_outside"]
        humidity_outside = outside_sub_doc["humidity_outside"]
        pump_cmd_get = outside_sub_doc["pump_cmd_get"] 
        # humidity_inside = coap_payload
        # self.set_content(request.payload)
        # return aiocoap.Message(code=aiocoap.CHANGED, payload = outside_cmd_payload)
        self.set_content(outside_cmd_payload)
        # print(outside_cmd_payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload = outside_cmd_payload) #not put function convert string to bytes here
class server_get(resource.Resource):

    async def render_get(self, request):
        return aiocoap.Message(payload = self.content)
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