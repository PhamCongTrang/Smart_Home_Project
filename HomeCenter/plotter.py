import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
import random
import time

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
def update_plot(frame):
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

    # Generate random temperature values for inside and outside
    inside_temperature = random.uniform(20, 50)
    outside_temperature = random.uniform(10, 50)
    inside_humidity  = random.uniform(0, 100)
    outside_humidity  = random.uniform(0, 100)

    # Append the current timestamp and data values
    current_time = datetime.now()
    timestamps['inside'].append(current_time)
    timestamps['outside'].append(current_time)
    temperature_values['inside'].append(inside_temperature)
    temperature_values['outside'].append(outside_temperature)
    humidity_values['inside'].append(inside_humidity)
    humidity_values['outside'].append(outside_humidity)

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
        f'Current Inside Temp: {inside_temperature:.2f}°C\nCurrent Outside Temp: {outside_temperature:.2f}°C',
        xy=(0.4, 0.85),
        xycoords='axes fraction',
        fontsize=10,
        color='black',
        bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='lightgray'))

    axs[1].annotate(
        f'Current Inside Humi: {inside_temperature:.2f}°C\nCurrent Outside Humi: {outside_temperature:.2f}°C',
        xy=(0.4, 0.85),
        xycoords='axes fraction',
        fontsize=10,
        color='black',
        bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='lightgray'))

# Set up the animation
animation = FuncAnimation(fig, update_plot, interval=1000, cache_frame_data=False)  # Update every 1000 milliseconds (1 second)
# Show the plot
plt.show()
# animation.save('animation.gif', writer='imagemagick', fps=30)