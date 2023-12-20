// Hoc ARM
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
// #include <string>
// using std::string;
// #define ssid "Hust_TVTQB_Dien-Dien-tu"
#define ssid "TCP"
#define password "trangcongpham"
// #define ssid "STM32F103C8T6"
// #define password "phong409"
// Thông tin về MQTT Broker
#define mqtt_server "192.168.168.43"
#define mqtt_topic_pub "local/topic1"
#define mqtt_topic_sub "local/topic2"

#define mqtt_user "ESP8266" 
#define mqtt_pwd "localbroker"

const uint16_t mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);
char tenwifi[] = "hello";
long lastMsg = 0;
char msg[50];
int value = 0;

// Hàm kết nối wifi
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
// Hàm call back để nhận dữ liệu
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (unsigned int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    WiFi.mode(WIFI_STA);
    if (client.connect("ESP8266Client",mqtt_user, mqtt_pwd)) {
      Serial.println("connected");
      // Khi kết nối sẽ publish thông báo
      client.publish(mqtt_topic_pub, "ESP_reconnected");
      // ... và nhận lại thông tin này
      client.subscribe(mqtt_topic_sub);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Đợi 5s
      delay(5000);
    }
  }
}
void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port); 
  client.setCallback(callback);
  srand(time(NULL));
}
void loop() {
  // Kiểm tra kết nối
  WiFi.mode(WIFI_STA);
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  value = rand()%30+10;
  snprintf (msg, 75, "%d", value);
  Serial.print("Publish message: ");
  Serial.println(msg);
  client.publish(mqtt_topic_pub, msg);
  delay(1000);
}