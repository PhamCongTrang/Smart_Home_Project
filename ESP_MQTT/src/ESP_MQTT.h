// Hoc ARM
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

#define ssid_1 "TCP"
#define password_1 "trangcongpham"
#define mqtt_server_1 "192.168.22.43"

#define ssid_2 "STM32F103C8T6"
#define password_2 "phong409"
#define mqtt_server_2 "192.168.0.104"

#define ssid_3 "Hust_TVTQB_Dien-Dien-tu"
#define mqtt_server_3 "192.168.66.163"

#define mqtt_topic_pub "local/topic1"
#define mqtt_topic_sub "local/topic2"
#define mqtt_user ""
#define mqtt_pwd ""
// JSON
DynamicJsonDocument PubDoc(1024);
DynamicJsonDocument SubDoc(1024);
int interval_time_inside = 1000;
int socket_cmd;
const uint16_t mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char pub_payload[50], sub_payload[50];
int temperature_inside = 0, humidity_inside = 0;

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
// Hàm call back để nhận dữ liệu
void callback(char *topic, byte *payload, unsigned int length)
{
    // Serial.print("Message arrived [");
    // Serial.print(topic);
    // Serial.print("] ");
    for (unsigned int i = 0; i < length; i++)
    {
        sub_payload[i] = (char)payload[i];
    }
    deserializeJson(SubDoc, sub_payload);
    int temp = SubDoc["interval_time_inside"];
    if ( temp != 0)
    {
        interval_time_inside = temp;
    }
    socket_cmd = SubDoc["socket_cmd"];
}
void reconnect()
{
    while (!client.connected())
    {
        Serial.print("Attempting MQTT connection...");
        WiFi.mode(WIFI_STA);
        if (client.connect("ESP8266Client", mqtt_user, mqtt_pwd))
        {
            Serial.println("connected");
            // Khi kết nối sẽ publish thông báo
            client.publish(mqtt_topic_pub, "ESP_reconnected");
            // ... và nhận lại thông tin này
            client.subscribe(mqtt_topic_sub);
        }
        else
        {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            // Đợi 5s
            delay(5000);
        }
    }
}
void setup()
{
    Serial.begin(115200);
    Auto_Connect_Wifi();
    client.setCallback(callback);
    srand(time(NULL));
}
void loop()
{
    // Kiểm tra kết nối
    WiFi.mode(WIFI_STA);
    if (!client.connected())
    {
        reconnect();
    }
    client.loop();
    temperature_inside = rand() % 10 + 10;
    humidity_inside = rand() % 10 + 50;
    PubDoc["temperature_inside"] = temperature_inside;
    PubDoc["humidity_inside"] = humidity_inside;
    serializeJson(PubDoc, pub_payload);
    // snprintf(pub_payload, 75, "{\"temperature_in\": %d, \"humidity_in\": %d}", temperature_inside, humidity_inside);
    Serial.print("Publish message: ");
    Serial.println(pub_payload);
    client.publish(mqtt_topic_pub, pub_payload);
    Serial.print("Receive: ");
    Serial.print("interval_time_inside:"); Serial.print(interval_time_inside); Serial.print(",socket_cmd:"); Serial.println(socket_cmd);
    delay(interval_time_inside);
}