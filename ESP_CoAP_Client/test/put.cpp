#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <coap-simple.h>
#include <time.h>


const char* ssid     = "Hust_TVTQB_Dien-Dien-tu";
const char* password = "12345678";

// CoAP client response callback
void callback_response(CoapPacket &packet, IPAddress ip, int port);

// UDP and CoAP class
WiFiUDP udp;
Coap coap(udp);

// CoAP client response callback
void callback_response(CoapPacket &packet, IPAddress ip, int port) {
  Serial.println("[Coap Response got]\n");

  char p[packet.payloadlen + 1];
  memcpy(p, packet.payload, packet.payloadlen);
  p[packet.payloadlen] = NULL;

  Serial.println(p);
}

void setup() {
  Serial.begin(9600);

  WiFi.begin(ssid);
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());



  // client response callback.
  // this endpoint is single callback.
  Serial.println("Setup Response Callback");
   coap.response(callback_response);

  // start coap server/client
  coap.start();
}

void loop() {
  // send GET or PUT coap request to CoAP server.
  // To test, use libcoap, microcoap server...etc
  // int msgid = coap.put(IPAddress(10, 0, 0, 1), 5683, "light", "1");
  Serial.println("Send Request");
  srand(time(NULL));
  int number = rand() % 41 - 20;
  char numberString[20];
  sprintf(numberString, "%d", number);

  // int msgid = coap.get(IPAddress(192, 168, 66, 233), 5683, "whoami");
  int msgid1 = coap.put(IPAddress(192, 168, 66, 243), 5683, "put", numberString);

  delay(1000);
  coap.loop();
}
