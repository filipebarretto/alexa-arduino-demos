/*
 * 
 * 
 * 
 * 
*/

#include "WiFi.h"
#include <PubSubClient.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>


#include "wifi_config.h"
#include "credentials.h"

// MQTT SETTINGS
const int MQTT_PORT = 8883;
const char MQTT_SUB_TOPIC[] = "iot_arduino_demos_actuators";

WiFiClientSecure net;
PubSubClient client(net);
StaticJsonDocument<200> json;


// SETUP PINS
const int RED_LED_PIN = 5;
const int GREEN_LED_PIN = 18;
const int YELLOW_LED_PIN = 19;

// DEFAULTS
const int INTERVAL = 1000;
const int BLINK_RATE = 1000;

// ACTUATORS COMMANDS
const String RED_LIGHT_ON = "red_light_on";
const String RED_LIGHT_OFF = "red_light_off";
const String RED_LIGHT_BLINK = "red_light_blink";
const String YELLOW_LIGHT_ON = "yellow_light_on";
const String YELLOW_LIGHT_OFF = "yellow_light_off";
const String GREEN_LIGHT_ON = "green_light_on";
const String GREEN_LIGHT_OFF = "green_light_off";
const String RESET = "reset";


void pubSubErr(int8_t MQTTErr) {
  if (MQTTErr == MQTT_CONNECTION_TIMEOUT)
    Serial.print("Connection tiemout");
  else if (MQTTErr == MQTT_CONNECTION_LOST)
    Serial.print("Connection lost");
  else if (MQTTErr == MQTT_CONNECT_FAILED)
    Serial.print("Connect failed");
  else if (MQTTErr == MQTT_DISCONNECTED)
    Serial.print("Disconnected");
  else if (MQTTErr == MQTT_CONNECTED)
    Serial.print("Connected");
  else if (MQTTErr == MQTT_CONNECT_BAD_PROTOCOL)
    Serial.print("Connect bad protocol");
  else if (MQTTErr == MQTT_CONNECT_BAD_CLIENT_ID)
    Serial.print("Connect bad Client-ID");
  else if (MQTTErr == MQTT_CONNECT_UNAVAILABLE)
    Serial.print("Connect unavailable");
  else if (MQTTErr == MQTT_CONNECT_BAD_CREDENTIALS)
    Serial.print("Connect bad credentials");
  else if (MQTTErr == MQTT_CONNECT_UNAUTHORIZED)
    Serial.print("Connect unauthorized");
}

void connect_to_mqtt(bool nonBlocking = false) {
  Serial.print("MQTT connecting ");
  while (!client.connected()) {
    if (client.connect(THINGNAME)) {
      Serial.println("connected!");
      if (!client.subscribe(MQTT_SUB_TOPIC))
        pubSubErr(client.state());
    }
    else {
      Serial.print("failed, reason -> ");
      pubSubErr(client.state());
      if (!nonBlocking) {
        Serial.println(" < try again in 5 seconds");
        delay(5000);
      }
      else {
        Serial.println(" <");
      }
    }
    if (nonBlocking)
      break;
  }
}

void messageReceived(char *topic, byte *payload, unsigned int length) {
  Serial.print("Received [");
  Serial.print(topic);
  Serial.print("]: ");

  char inData[length];
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    inData[i] = (char)payload[i];
  }
  Serial.println();

  DeserializationError error = deserializeJson(json, inData);

  const char* command = json["command"];
  Serial.println(command);
  execute_command(command);
}


void connect_to_wifi() {
  while (WiFi.status() != WL_CONNECTED)  {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("WiFi connected"); 
  Serial.print("My IP address is: ");
  Serial.println(WiFi.localIP());

}

void checkWiFiThenMQTT(void) {
  Serial.println("Checking WiFi...");
  connect_to_wifi();
  connect_to_mqtt();
}

void reset() {
  active = false;
  digitalWrite(RED_LED_PIN, LOW);
  digitalWrite(YELLOW_LED_PIN, LOW);
  digitalWrite(GREEN_LED_PIN, LOW);
}


void blink_led(int pin) {
  active = true;
  while(active) { 
    digitalWrite(pin, HIGH);
    delay(BLINK_RATE);
    digitalWrite(pin, LOW);
    delay(BLINK_RATE);
    blink_led(pin);
  }
}


void execute_command(String command) {
  if (command.equals(RED_LIGHT_ON)) {
    Serial.println("TURNING RED LIGHT ON...");
    digitalWrite(RED_LED_PIN, HIGH);
  } else if (command.equals(RED_LIGHT_OFF)) {
    Serial.println("TURNING RED LIGHT OFF...");
    digitalWrite(RED_LED_PIN, LOW);
  } else if (command.equals(RED_LIGHT_BLINK)) {
    Serial.println("BLINKING RED LIGHT...");
    //blink_led(RED_LED_PIN);
  } else if (command.equals(YELLOW_LIGHT_ON)) {
    Serial.println("TURNING YELLOW LIGHT ON...");
    digitalWrite(YELLOW_LED_PIN, HIGH);
  } else if (command.equals(YELLOW_LIGHT_OFF)) {
    Serial.println("TURNING YELLOW LIGHT OFF...");
    digitalWrite(YELLOW_LED_PIN, LOW);
  } else if (command.equals(GREEN_LIGHT_ON)) {
    Serial.println("TURNING GREEN LIGHT ON...");
    digitalWrite(GREEN_LED_PIN, HIGH);
  } else if (command.equals(GREEN_LIGHT_OFF)) {
    Serial.println("TURNING GREEN LIGHT OFF...");
    digitalWrite(GREEN_LED_PIN, LOW);
  } else if (command.equals(RESET)) {
    Serial.println("RESETING...");
    reset();
  } else {
    Serial.println("INVALID COMMAND.");
  }
}


void setup() {
  Serial.begin(9600);

  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pass); 
  WiFi.setHostname("NodeMCU_01");
  
  connect_to_wifi();

  net.setCACert(cacert);
  net.setCertificate(client_cert);
  net.setPrivateKey(privkey);

  client.setServer(MQTT_HOST, MQTT_PORT);
  client.setCallback(messageReceived);
  
  connect_to_mqtt();
  
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(YELLOW_LED_PIN, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {

  if (!client.connected()) {
    checkWiFiThenMQTT();
  } else {
    client.loop();  
  }
  
}
