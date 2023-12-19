#include <iostream>
#include <mqtt/async_client.h>

// Địa chỉ IP và cổng của MQTT broker
const std::string brokerAddress = "tcp://127.0.0.1:1883";

// Tên client cho subscriber và publisher
const std::string clientIdSub = "CppSubscriber";
const std::string clientIdPub = "CppPublisher";

// Topics
const std::string topicSub = "topic1";
const std::string topicPub = "topic2";

// Callback khi nhận được tin nhắn từ topic1
class SubscribeCallback : public virtual mqtt::callback {
public:
    void message_arrived(mqtt::const_message_ptr msg) override {
        std::cout << "Received message on topic " << msg->get_topic() << ": " << msg->to_string() << std::endl;

        // Publish message to topic2
        publish(clientIdPub, topicPub, "Hello from C++ Publisher");
    }
};

// Callback khi gặp sự kiện kết nối với broker
class ConnectCallback : public virtual mqtt::callback {
public:
    void connected(const std::string& cause) override {
        std::cout << "Connected to MQTT broker: " << cause << std::endl;

        // Subscribe to topic1
        subscribe(clientIdSub, topicSub);
    }
};

// Hàm publish tin nhắn lên topic2
void publish(const std::string& clientId, const std::string& topic, const std::string& message) {
    mqtt::async_client client(brokerAddress, clientId);

    try {
        mqtt::connect_options connOpts;
        connOpts.set_clean_session(true);

        client.connect(connOpts)->wait();

        mqtt::message_ptr pubmsg = mqtt::make_message(topic, message);
        client.publish(pubmsg)->wait();

        client.disconnect()->wait();
    } catch (const mqtt::exception& exc) {
        std::cerr << "Error publishing message: " << exc.what() << std::endl;
    }
}

// Hàm subscribe vào topic1
void subscribe(const std::string& clientId, const std::string& topic) {
    mqtt::async_client client(brokerAddress, clientId);

    try {
        mqtt::connect_options connOpts;
        connOpts.set_clean_session(true);

        client.connect(connOpts)->wait();

        SubscribeCallback cb;
        client.set_callback(cb);

        client.subscribe(topic, 0)->wait();

        // Chờ vô hạn để giữ kết nối mở
        while (true) {
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
    } catch (const mqtt::exception& exc) {
        std::cerr << "Error subscribing to topic: " << exc.what() << std::endl;
    }
}

int main() {
    // Kết nối và subscribe
    ConnectCallback cb;
    mqtt::async_client client(brokerAddress, clientIdSub);
    client.set_callback(cb);

    try {
        mqtt::connect_options connOpts;
        connOpts.set_clean_session(true);

        client.connect(connOpts)->wait();

        // Chờ vô hạn để giữ kết nối mở
        while (true) {
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
    } catch (const mqtt::exception& exc) {
        std::cerr << "Error connecting to MQTT broker: " << exc.what() << std::endl;
        return 1;
    }

    return 0;
}
