import paho.mqtt.client as mqtt
client1=mqtt.Client("P1")
client1.connect("192.168.66.243")
client1.publish("local/topic2","publish")
