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
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
# Initialize empty lists for timestamps and data values
timestamps = {'inside': [], 'outside': []}
temperature_values = {'inside': [], 'outside': []}
humidity_values = {'inside': [], 'outside': []}

# Create a figure with two subplots (temperature and humidity)
fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
# Initialize empty lines for temperature and humidity plots
temp_line_inside, = axs[0].plot([], [],  linestyle='-', color='b', label='Inside Temperature')
temp_line_outside, = axs[0].plot([], [], linestyle='-', color='r', label='Outside Temperature')

hum_line_inside, = axs[1].plot([], [],  linestyle='--', color='g', label='Inside Humidity')
hum_line_outside, = axs[1].plot([], [], linestyle='--', color='orange', label='Outside Humidity')

# Function to update the plot with new data
async def update_plot(frame):
    # Set labels and title
    axs[0].set_ylabel('Temperature (°C)')
    axs[0].set_title('Inside and Outside Temperature')
    axs[0].set_ylim(0, 65)

    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Humidity (%)')
    axs[1].set_title('Inside and Outside Humidity')
    axs[1].set_ylim(0, 110)

    # Display legends
    axs[0].legend(loc='upper right')
    axs[1].legend(loc='upper right')

    # Format x-axis as time
    axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    axs[1].xaxis.set_major_locator(mdates.SecondLocator(interval=10))

    global temperature_inside, humidity_inside, temperature_outside, humidity_outside
    # Append the current timestamp and data values
    current_time = datetime.now()
    timestamps['inside'].append(current_time)
    timestamps['outside'].append(current_time)
    temperature_values['inside'].append(temperature_inside)
    temperature_values['outside'].append(temperature_outside)
    humidity_values['inside'].append(humidity_inside)
    humidity_values['outside'].append(humidity_outside)

    # Limit the number of data points to show (optional)
    max_data_points = 50
    for key in timestamps:
        if len(timestamps[key]) > max_data_points:
            timestamps[key].pop(0)
            temperature_values[key].pop(0)
            humidity_values[key].pop(0)

    # Update temperature and humidity plots
    temp_line_inside.set_data(timestamps['inside'], temperature_values['inside'])
    temp_line_outside.set_data(timestamps['outside'], temperature_values['outside'])
    hum_line_inside.set_data(timestamps['inside'], humidity_values['inside'])
    hum_line_outside.set_data(timestamps['outside'], humidity_values['outside'])

    # Adjust plot limits
    axs[0].relim()
    axs[0].autoscale_view()
    axs[1].relim()
    axs[1].autoscale_view()

    #Annote
    axs[0].annotate(
        f'Current Inside Temp: {temperature_inside:.2f}°C\nCurrent Outside Temp: {temperature_outside:.2f}°C',
        xy=(0.4, 0.85),
        xycoords='axes fraction',
        fontsize=10,
        color='black',
        bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='lightgray'))

    axs[1].annotate(
        f'Current Inside Humi: {temperature_inside:.2f}°C\nCurrent Outside Humi: {temperature_outside:.2f}°C',
        xy=(0.4, 0.85),
        xycoords='axes fraction',
        fontsize=10,
        color='black',
        bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='lightgray'))
# Khai bao cac bien Global, la cac message
temperature_inside = 0
humidity_inside = 0
temperature_outside = 0
humidity_outside = 0

temperature_threshold_inside_set = 30
temperature_threshold_outside_set = 40

zero_Doc = '{}'
inside_sub_doc = json.loads(zero_Doc)

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

def on_connect_local_subscribe(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to subscribe local MQTT broker")
        client.subscribe("local/plotter")
    else:
        print(f"Connection failed with error code {rc}")

def on_message_local_subscribe(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")

    inside_sub_doc = json.loads(msg.payload)
    temperature_inside = inside_sub_doc["temperature_inside"]
    humidity_inside = inside_sub_doc["humidity_inside"]
    temperature_outside = inside_sub_doc["temperature_outside"]
    humidity_outside = inside_sub_doc["humidity_outside"]

    external_pub_payload = f'{{"temperature_inside":{temperature_inside},"humidity_inside":{humidity_inside},"temperature_outside":{temperature_outside},"humidity_outside":{humidity_outside}}}'
    
    print(external_pub_payload) #nguyen nhan khac cung lam timeline thingsboard khong ve do thi
    animation = FuncAnimation(fig, update_plot, interval=1000, cache_frame_data=False)  # Update every 1000 milliseconds (1 second)
    # Show the plot
    plt.show()

def on_disconnect(client, userdata, rc):
    print(f"Disconnected from MQTT broker")

##------------------CONNECT TO LOCAL CLIENT------------------------------------##
# 1. FORWARD
local_broker_address = local_ip
local_sub_topic = "local/plotter"
local_sub_client = mqtt.Client("plotter")
local_sub_client.on_connect = on_connect_local_subscribe
local_sub_client.on_disconnect = on_disconnect
local_sub_client.on_message = on_message_local_subscribe
local_sub_client.connect(local_broker_address, 1883, 60)
local_sub_client.loop_start()

async def main():
    animation = FuncAnimation(fig, update_plot, interval=1000, cache_frame_data=False)  # Update every 1000 milliseconds (1 second)
    # Show the plot
    plt.show()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

try:
    while True:
        # Sleep for some time before publishing the next data (e.g., every 5 seconds)
        time.sleep(1)

except KeyboardInterrupt:
    # Disconnect on keyboard interrupt
    print("Disconnected from Thingboard MQTT broker")