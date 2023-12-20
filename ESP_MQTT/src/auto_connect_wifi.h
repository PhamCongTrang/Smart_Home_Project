#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define ssid_1 "TCP"
#define password_1 "trangcongpham"
#define mqtt_server_1 "192.168.168.43"

#define ssid_2 "STM32F103C8T6"
#define password_2 "phong409"
#define mqtt_server_2 "192.168.0.104"

#define ssid_3 "Hust_TVTQB_Dien-Dien-tu"
#define mqtt_server_3 "192.168.168.43"

int Auto_Connect_Wifi()
{
    int try_wifi = 0;
    while (1 == 1)
    {
        try_wifi = wifi_1();
        if(try_wifi != 0) break;
        try_wifi = wifi_2();
        if(try_wifi != 0) break;
        try_wifi = wifi_3();
        if(try_wifi != 0) break;
    }
    switch (try_wifi)
    {
        case 1:
            client.setServer(mqtt_server_1, 1883); 
            break;
        case 2:
            client.setServer(mqtt_server_2, 1883); 
            break;
        case 3:
            client.setServer(mqtt_server_3, 1883); 
            break;
    }
    return try_wifi;
}
int wifi_1()
{
    Serial.print("Connecting to ");    Serial.println(ssid_1);
    WiFi.begin(ssid_1, password_1);
    for(int i = 0; i < 10 && WiFi.status() != WL_CONNECTED; i++)
    {
        delay(500); Serial.print(".");
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
    Serial.print("Connecting to ");    Serial.println(ssid_2);
    WiFi.begin(ssid_2, password_2);
    for(int i = 0; i < 10 && WiFi.status() != WL_CONNECTED; i++)
    {
        delay(500); Serial.print(".");
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
    Serial.print("Connecting to ");    Serial.println(ssid_1);
    WiFi.begin(ssid_3);
    for(int i = 0; i < 10 && WiFi.status() != WL_CONNECTED; i++)
    {
        delay(500); Serial.print(".");
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
