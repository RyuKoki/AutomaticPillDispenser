// libraries
#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include "SSD1306Wire.h"

/* INITIALIZE */
// initialize client and server
WiFiClient espClient;
PubSubClient client(espClient);
const char* mqtt_server = "192.168.43.93";
long lastMsg = 0;
// initialize LED display
// :params => (ADDRESS, SDA, SCL)
SSD1306Wire display(0x3c, 5, 4);
// initialize pin
#define LED_PIN   (16)

// blink led function
void blink_led(unsigned int times, unsigned int duration) {
  for (int i=0; i<times; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(duration);
    digitalWrite(LED_PIN, LOW);
    delay(duration);
  }
}

// show messages on OLED
void show_text(String msg) {
  display.setFont(ArialMT_Plain_24);
  display.setTextAlignment(TEXT_ALIGN_CENTER);
  display.drawString(64, 22, msg);
}

// set-up WiFi function
void CONNECT_WIFI() {
  const char* WIFI_NAME = "xxx";
  const char* WIFI_PASS = "xxx";
  // WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_NAME, WIFI_PASS);
  // try to connect WiFi
  int c = 0;
  while (WiFi.status() != WL_CONNECTED) {
    blink_led(2, 200);
    delay(1000);
    Serial.print(".");
    c = c + 1;
    if (c > 10) {
      ESP.restart();
    }
  }
  // connect WiFi successful
  Serial.println("");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println("!!!!!!!!!! WiFi Connected !!!!!!!!!!");
}

// function for connecting MQTT server
void connect_mqttServer() {
  // reconnected
  while (!client.connected()) {
    // re-check WiFi
    if (WiFi.status() != WL_CONNECTED) {
      CONNECT_WIFI();
    }
    // try to connect to MQTT server
    Serial.print("Try to connect to MQTT server...");
    if (client.connect("ESP32_client1")) {
      Serial.println("Connected");
      // subcribe the topics
      // client.subscribe("rpi/broadcast");
      client.subscribe("dispenser/slot1");
    } else {
      // the attempt is not successful
      Serial.print("Failed, rc= ");
      Serial.print(client.state());
      Serial.println(" trying again in 2 seconds.");
      blink_led(3, 200);
      delay(2000);
    }
  }
}

void drawProgressBarDemo(int counter) {
  int progress = (int) 100/counter;
  int counting = progress;
  while (counting <= 100) {
    display.clear();
    display.drawProgressBar(0, 32, 120, 10, counting);
    display.setTextAlignment(TEXT_ALIGN_CENTER);
    display.drawString(64, 15, String(counting) + "%");
    display.display();
    delay(1000);
    counting += progress;
  }
}

// this function will be executed whenever there is data available on subscribed topics
void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;

  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();
  // Check if a message is received on the topic "rpi/broadcast"
  // if (String(topic) == "rpi/broadcast") {
  if (String(topic) == "dispenser/slot1") {
    drawProgressBarDemo(messageTemp.toInt());
    display.clear();
    show_text("Done!!!");
    display.display();
    // client.publish("dispenser/response/slot1", "Done");
    delay(3000);
    display.clear();
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  // connecting to WiFi
  CONNECT_WIFI();
  // initialize OLED
  display.init();
  display.flipScreenVertically();
  // initialize MQTT connection
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

// int state = 0;
void loop() {
  if (!client.connected()) {
    connect_mqttServer();
  }
  client.loop();
}
