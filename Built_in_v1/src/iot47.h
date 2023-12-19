#include <ESP8266WiFi.h>
#include <PubSubClient.h>


// Thông tin về wifi
#define ssid "TCP"
#define password "trangcongpham"
#define mqtt_server "maqiatto.com"
const uint16_t mqtt_port = 1883; //Port của CloudMQTT TCP

WiFiClient espClient;
PubSubClient client(espClient);

// Hàm kết nối wifi
void setup_wifi() 
{
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
void callback(char* topic, byte* payload, unsigned int length) 
{
  Serial.print("Co tin nhan moi tu topic:");
  Serial.println(topic);
  for (unsigned int i = 0; i < length; i++) 
    Serial.print((char)payload[i]);
  Serial.println();
}
// Hàm reconnect thực hiện kết nối lại khi mất kết nối với MQTT Broker
void reconnect() 
{
  while (!client.connected()) // Chờ tới khi kết nối
  {
    // Thực hiện kết nối với mqtt user và pass
    if (client.connect("ESP8266_id1","ESP_offline",0,0,"ESP8266_id1_offline"))  //kết nối vào broker
    {
      Serial.println("Đã kết nối:");
      client.subscribe("ESP8266_read_data"); //đăng kí nhận dữ liệu từ topic ESP8266_read_data
    }
    else 
    {
      Serial.print("Lỗi:, rc=");
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
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port); 
  client.setCallback(callback);
}
void loop() 
{
  if (!client.connected())// Kiểm tra kết nối
    reconnect();
  client.loop();
  if(Serial.available() > 0)
  {
    delay(30);
    char inputString[30]="";
    int i=0;
    while(Serial.available() > 0)
    {
      char inChar = (char)Serial.read();
      inputString[i++] = inChar;
    }
    client.publish("ESP8266_sent_data", inputString); // gửi dữ liệu lên topic ESP8266_sent_data
  }
}