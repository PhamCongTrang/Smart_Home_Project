# IoT Smart Home System
## Overview

The enhanced IoT Smart Home system aims to provide comprehensive monitoring and control capabilities. ESP8266 devices placed indoors and outdoors capture temperature and humidity data, which is then transmitted to the Home Center. The Home Center acts as a central hub, communicating with Thingsboard for data visualization and sending control commands back to the ESP8266 devices.
## Features
Expanded Device Network: The system includes ESP8266 devices positioned both indoors and outdoors, broadening the coverage for temperature and humidity monitoring.

Bi-Directional Communication: The Home Center establishes bidirectional communication with Thingsboard for data retrieval and visualization, as well as with ESP8266 devices for remote control.

Control Commands: The Home Center sends control commands to ESP8266 devices, enabling users to remotely control pumps and sockets within the smart home.

## Components
ESP8266 Devices: Positioned strategically, these devices capture temperature and humidity data and act on control commands.

Home Center (Computer): The computer serves as the central control unit, communicating with both Thingsboard and ESP8266 devices.

Thingsboard Platform: Thingsboard continues to serve as the central platform for data storage, visualization, and management.
## Getting Started
To set up the enhanced IoT Smart Home system, follow these steps:

### 1. ESP8266 Device Setup

Arduino Libraries Installation

ArduinoJson Library:

    git clone https://github.com/bblanchon/ArduinoJson.git
  
ESP8266WiFi Library:
    
    git clone https://github.com/tzapu/WiFiManager.git
    
PubSubClient Library (for MQTT):

    git clone https://github.com/knolleary/pubsubclient.git

Coap-Simple Library (for CoAP):

    git clone https://github.com/hirotakaster/CoAP-simple-library

### 2. Home Center Setup
Python Libraries Installation

Paho-MQTT Library:

    pip install paho-mqtt

Aiocoap Library:

    pip install aiocoap

## Contribution
Contributions to the project are encouraged. Feel free to fork the repository, make enhancements, and submit pull requests.
## Author

Pham Cong Trang - Vu Huy Hoang
