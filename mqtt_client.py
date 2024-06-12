import paho.mqtt.client as mqtt

class MqttClient:
    def __init__(self, mqtt_server, port):
        self.mqtt_server = mqtt_server
        self.port = port
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        
        self.client.connect(mqtt_server, port, 60)
        self.client.loop_start()

    # Hàm callback khi kết nối tới broker thành công
    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("Kết nối thành công với mã trả về: " + str(rc))
        

    def subscribe(self, topic):
        self.client.subscribe(topic)
        print(f"Đã đăng ký lắng nghe topic: {topic}")

    def publish(self, topic, data):
        self.client.publish(topic, data)
        print(f"Đã gửi tin nhắn tới {topic}: {data}")

    def set_callback(self, callback):
        self.client.on_message = callback

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Đã ngắt kết nối khỏi broker")

