#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <coap-simple.h>
#include <time.h>
#include <ArduinoJson.h>

#define ssid_1 "TCP"
#define password_1 "trangcongpham"
#define server_ip_1 192, 168, 22, 43

#define ssid_2 "STM32F103C8T6"
#define password_2 "phong409"
#define server_ip_2 192, 168, 0, 104

#define ssid_3 "Hust_TVTQB_Dien-Dien-tu"
#define server_ip_3 192, 168, 66, 163

// JSON
DynamicJsonDocument PubDoc(1024);
DynamicJsonDocument SubDoc(1024);
int interval_time_outside = 1000;
int pump_cmd = 0;

char pub_payload[50], sub_payload[50];
int temperature_outside = 0, humidity_outside = 0;
// CoAP client response callback
void callback_response(CoapPacket &packet, IPAddress ip, int port);

// UDP and CoAP class
WiFiUDP udp;
Coap coap(udp);

// CoAP client response callback
void callback_response(CoapPacket &packet, IPAddress ip, int port)
{

    memcpy(sub_payload, packet.payload, packet.payloadlen);
    sub_payload[packet.payloadlen] = NULL;
    Serial.print("Sub Payload: "); Serial.println(sub_payload);
    deserializeJson(SubDoc, sub_payload);
    interval_time_outside = SubDoc["interval_time_outside"];
    pump_cmd = SubDoc["pump_cmd"];
    Serial.print("Receive: ");
    Serial.print("interval_time_outside:"); Serial.print(interval_time_outside); Serial.print(",pump_cmd:"); Serial.println(pump_cmd);
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
#define server_ip server_ip_1
        break;
    case 2:
#define server_ip server_ip_2
        break;
    case 3:
#define server_ip server_ip_3
        break;
    }
    return try_wifi;
}
void setup()
{
    Serial.begin(115200);

    Auto_Connect_Wifi();

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
    // send GET or PUT coap request to CoAP server.
    // To test, use libcoap, microcoap server...etc
    // int msgid = coap.put(IPAddress(10, 0, 0, 1), 5683, "light", "1");
    // Serial.println("Send Request");
    temperature_outside = rand() % 15 + 10;
    humidity_outside = rand() % 10 + 70;
    PubDoc["temperature_outside"] = temperature_outside;
    PubDoc["humidity_outside"] = humidity_outside;
    serializeJson(PubDoc, pub_payload);
    Serial.print("Send: ");
    Serial.println(pub_payload);
    // char numberString[20];
    // sprintf(numberString, "%d", number);
    // Serial.print("Put: ");
    // Serial.println(numberString);
    // int msgid = coap.get(IPAddress(192, 168, 66, 233), 5683, "whoami");
    coap.put(IPAddress(server_ip_1), 5683, "put", pub_payload);
    //   int msgid = coap.get(IPAddress(server_ip), 5683, "get"); // khong can get cung tu get

    delay(2000);
    coap.loop();
}
