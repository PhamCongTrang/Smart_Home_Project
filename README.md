# Smart_Home_Project
IoT Smart Home System Enhancement

The IoT Smart Home project has been enhanced to include ESP8266 devices both indoors and outdoors, measuring temperature and humidity. The data is sent to the Home Center, which runs on a computer. The computer communicates with Thingsboard for data visualization and management. Additionally, the Home Center sends control commands to ESP8266 devices for pump and socket control.
Overview

The enhanced IoT Smart Home system aims to provide comprehensive monitoring and control capabilities. ESP8266 devices placed indoors and outdoors capture temperature and humidity data, which is then transmitted to the Home Center. The Home Center acts as a central hub, communicating with Thingsboard for data visualization and sending control commands back to the ESP8266 devices.
Features

    Expanded Device Network: The system includes ESP8266 devices positioned both indoors and outdoors, broadening the coverage for temperature and humidity monitoring.

    Bi-Directional Communication: The Home Center establishes bidirectional communication with Thingsboard for data retrieval and visualization, as well as with ESP8266 devices for remote control.

    Control Commands: The Home Center sends control commands to ESP8266 devices, enabling users to remotely control pumps and sockets within the smart home.

Components

    ESP8266 Devices: Positioned strategically, these devices capture temperature and humidity data and act on control commands.

    Home Center (Computer): The computer serves as the central control unit, communicating with both Thingsboard and ESP8266 devices.

    Thingsboard Platform: Thingsboard continues to serve as the central platform for data storage, visualization, and management.

Getting Started

To set up the enhanced IoT Smart Home system, follow these steps:

    ESP8266 Configuration: Program the ESP8266 devices to capture temperature and humidity data and implement control command responses.

    Home Center Configuration: Set up the Home Center computer to communicate with Thingsboard. Write scripts or applications to manage data flow and control commands.

    Thingsboard Integration: Configure Thingsboard to receive data from the Home Center and create interactive dashboards for monitoring.

    Deployment: Install ESP8266 devices in desired locations. Ensure proper connectivity to the Home Center.

    Remote Control: Use Thingsboard to monitor real-time data and remotely control pumps and sockets via the Home Center.

ESP8266 Device Setup
Arduino Libraries Installation

    ArduinoJson Library:
        Open the Arduino IDE.
        Navigate to Sketch > Include Library > Manage Libraries.
        Search for "ArduinoJson" and install the library.

    ESP8266WiFi Library:
        In the Arduino IDE, go to Sketch > Include Library > Manage Libraries.
        Search for "ESP8266WiFi" and install the library.

    PubSubClient Library (for MQTT):
        Follow the same steps and install "PubSubClient" for MQTT communication.

    Coap-Simple Library (for CoAP):
        Download the Coap-Simple library from the official repository.
        Extract the downloaded folder and move it to the Arduino libraries folder.

Code Configuration

    Modify your ESP8266 Arduino sketches to include the necessary library headers, configure WiFi credentials, and integrate MQTT or CoAP communication logic.
Home Center Setup
Python Libraries Installation

    Paho-MQTT Library:

    bash

pip install paho-mqtt

Aiocoap Library:

bash

    pip install aiocoap

    Json Library:
        No separate installation is needed as JSON handling is included in the Python standard library.

Code Configuration

    Write Python scripts on the Home Center to establish MQTT or CoAP communication with ESP8266 devices. Use the Paho-MQTT and Aiocoap libraries for respective protocols.

Contribution

Contributions to the project are encouraged. Feel free to fork the repository, make enhancements, and submit pull requests.
Author

Pham Cong Trang - Vu Huy Hoang