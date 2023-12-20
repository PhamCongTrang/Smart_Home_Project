#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "TCP";
const char* password =  "trangcongpham";
const char* mqttServer = "maqiatto.com";
const int mqttPort = 1883;
const char* mqttUser = "phamcongtranghd@gmail.com";
const char* mqttPassword = "externalbroker";

long lastMsg = 0;
char msg[50];
int value = 0; 

WiFiClient espClient;
PubSubClient client(espClient);


void callback(char* topic, byte* payload, unsigned int length) {

  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }

  Serial.println();
  Serial.println("-----------------------");

}
void setup() {

  Serial.begin(115200);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");

    if (client.connect("ESP8266Client", mqttUser, mqttPassword )) {

      Serial.println("connected");

    } else {

      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);

    }
  }
  //Pub Hello to esp/test topic and sub this topic
  client.publish("phamcongtranghd@gmail.com/topic1", "Hello from ESP8266");
  client.subscribe("phamcongtranghd@gmail.com/topic2");

}
void loop() {
  client.loop();
  long now = millis();
  if (now - lastMsg > 8000) {
    lastMsg = now;
    ++value;
    snprintf (msg, 75, "hello world #%ld", value);
   
    //    client.publish(mqtt_topic_pub, msg);
    if (value < 10) {
      Serial.print("Publish message: ");
      Serial.println(msg);
      client.publish("esp/test", msg);
    }
  }
}