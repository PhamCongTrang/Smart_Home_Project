#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <coap-simple.h>
#include <time.h>
#include <ArduinoJson.h>

#define ssid_1 "TCP"
#define password_1 "trangcongpham"
#define server_ip_1 192, 168, 97, 43

#define ssid_2 "STM32F103C8T6"
#define password_2 "phong409"
#define server_ip_2 192, 168, 0, 104

#define ssid_3 "Hust_TVTQB_Dien-Dien-tu"
#define server_ip_3 192, 168, 66, 214
const int ledPin = D7;
const int buttonPin = D5;
// JSON
DynamicJsonDocument PubDoc(1024);
DynamicJsonDocument SubDoc(1024);
int interval_time_outside_set = 1000;

int pump_cmd_set = 0;
int pump_cmd_set_old = 0;
int pump_cmd_get = 0;
int pump_cmd_get_old = 0;
int button_cmd = 0;

int pump_state = -1;
unsigned long button_timer, publish_timer, pump_timer;
char pub_payload[70];
int temperature_outside = 18, humidity_outside = 50;
int ip1, ip2, ip3, ip4;
void separate_ip(int x, int y, int z, int t, int *ptr_ip1, int *ptr_ip2, int *ptr_ip3, int *ptr_ip4)
{
    *ptr_ip1 = x;
    *ptr_ip2 = y;
    *ptr_ip3 = z;
    *ptr_ip4 = t;
}
// CoAP client response callback
void callback_response(CoapPacket &packet, IPAddress ip, int port);

// UDP and CoAP class
WiFiUDP udp;
Coap coap(udp);

// CoAP client response callback
void callback_response(CoapPacket &packet, IPAddress ip, int port)
{
    char sub_payload[70];
    memcpy(sub_payload, packet.payload, packet.payloadlen);
    sub_payload[packet.payloadlen] = NULL;
    // packet.payloadlen = 0;
    //free(packet.payload);
    Serial.print("Sub Payload: "); Serial.println(sub_payload);
    deserializeJson(SubDoc, sub_payload);
    int temp = SubDoc["interval_time_outside_set"];
    if (temp != 0)
    {
        interval_time_outside_set = temp;
    }
    //pump_cmd_set = 0;
    temp = SubDoc["pump_cmd_set"];
    if(temp != pump_cmd_set_old)
    {
        pump_cmd_set = temp;
        pump_cmd_set_old = temp;
    }
    else 
        pump_cmd_set = 0;
}
// Hàm kết nối wifi
int wifi_1()
{
    Serial.println("");
    Serial.print("Connecting to ");
    Serial.println(ssid_1);
    WiFi.begin(ssid_1, password_1);
    for (int i = 0; i < 20 && WiFi.status() != WL_CONNECTED; i++)
    {
        delay(500);
        Serial.print(".");
    }
    if (WiFi.status() == WL_CONNECTED)
    {
        Serial.println("");
        Serial.println("WiFi connected");
        Serial.println("IP address: ");
        Serial.println(WiFi.localIP());
        return 1;
    }
    else
        return 0;
}
int wifi_2()
{
    Serial.println("");
    Serial.print("Connecting to ");
    Serial.println(ssid_2);
    WiFi.begin(ssid_2, password_2);
    for (int i = 0; i < 20 && WiFi.status() != WL_CONNECTED; i++)
    {
        delay(500);
        Serial.print(".");
    }
    if (WiFi.status() == WL_CONNECTED)
    {
        Serial.println("");
        Serial.println("WiFi connected");
        Serial.println("IP address: ");
        Serial.println(WiFi.localIP());
        return 2;
    }
    else
        return 0;
}
int wifi_3()
{
    Serial.println("");
    Serial.print("Connecting to ");
    Serial.println(ssid_3);
    WiFi.begin(ssid_3);
    for (int i = 0; i < 20 && WiFi.status() != WL_CONNECTED; i++)
    {
        delay(500);
        Serial.print(".");
    }
    if (WiFi.status() == WL_CONNECTED)
    {
        Serial.println("");
        Serial.println("WiFi connected");
        Serial.println("IP address: ");
        Serial.println(WiFi.localIP());
        return 3;
    }
    else
        return 0;
}
int Auto_Connect_Wifi()
{
    int try_wifi = 0;
    while (1 == 1)
    {
        try_wifi = wifi_1();
        if (try_wifi != 0)
            break;
        try_wifi = wifi_2();
        if (try_wifi != 0)
            break;
        try_wifi = wifi_3();
        if (try_wifi != 0)
            break;
    }
    switch (try_wifi)
    {
    case 1:
        separate_ip(server_ip_1, &ip1, &ip2, &ip3, &ip4);
        break;
    case 2:
        separate_ip(server_ip_2, &ip1, &ip2, &ip3, &ip4);
        break;
    case 3:
        separate_ip(server_ip_3, &ip1, &ip2, &ip3, &ip4);
        break;
    }
    return try_wifi;
}
void setup()
{
    Serial.begin(115200);
    pinMode(ledPin, OUTPUT);
    pinMode(buttonPin, INPUT);
    Auto_Connect_Wifi();
    digitalWrite(ledPin, LOW);
    // client response callback.
    // this endpoint is single callback.
    Serial.println("server_ip:");
    Serial.println("Setup Response Callback");
    coap.response(callback_response);
    srand(time(NULL));
    // start coap server/client
    coap.start();
}

void loop()
{
    if (millis() - button_timer > interval_time_outside_set)
    {
        button_cmd = digitalRead(buttonPin);
        if (button_cmd == 1)
        {
            Serial.println("BUTTON PRESSED");
            button_timer = millis();
        }

        // Control
        if (button_cmd == 1)
            pump_state = -pump_state;
        else if (pump_cmd_set != 0)
            pump_state = pump_cmd_set;
        // Control pump
        if (pump_state == 1)
            digitalWrite(ledPin, HIGH);
        if (pump_state == -1 || pump_state == 0)
            digitalWrite(ledPin, LOW);

        if (pump_state == pump_cmd_get_old)
            pump_cmd_get = 0;
        else
        {
            pump_cmd_get_old = pump_state;
            pump_cmd_get = pump_state;
        }
            
    }
    if(millis() - publish_timer > interval_time_outside_set)
    {
        publish_timer = millis();
        //pump_cmd_set = 0;
        coap.loop();
        //if(pump_cmd_set == pump_state) pump_cmd_set = 0;

        Serial.print("Receive: ");
        Serial.print("interval_time_outside_set:");
        Serial.print(interval_time_outside_set);
        Serial.print(",pump_cmd_set:");
        Serial.println(pump_cmd_set);
        // Simulate temperature and humidity

        temperature_outside += rand() % 4 - 1;
        if (pump_state == 1)
            temperature_outside -= 4 * interval_time_outside_set / 1000;
        if (temperature_outside > 50)
            temperature_outside = 50;
        if (temperature_outside < 5)
            temperature_outside = 5;
        humidity_outside += rand() % 7 - 3;
        if (humidity_outside > 100)
            humidity_outside = 100;
        if (humidity_outside < 0)
            humidity_outside = 0;

        // Creat message
        PubDoc["temperature_outside"] = temperature_outside;
        PubDoc["humidity_outside"] = humidity_outside;
        PubDoc["pump_cmd_get"] = pump_cmd_get;
        serializeJson(PubDoc, pub_payload);
        Serial.print("Send: ");
        Serial.println(pub_payload);
        // char numberString[20];
        // sprintf(numberString, "%d", number);
        // Serial.print("Put: ");
        // Serial.println(numberString);
        // int msgid = coap.get(IPAddress(192, 168, 66, 233), 5683, "whoami");
        coap.put(IPAddress(ip1, ip2, ip3, ip4), 5683, "put", pub_payload);
        //   int msgid = coap.get(IPAddress(server_ip), 5683, "get"); // khong can get cung tu get
        // if (pump_cmd_set == 1)
        //     digitalWrite(ledPin, LOW);
        // if (pump_cmd_set == -1 || pump_cmd_set == 0)
        //     digitalWrite(ledPin, HIGH);
        // delay(interval_time_outside_set);
        
    }
}
