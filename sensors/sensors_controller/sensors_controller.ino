/*
 * 
 * 
 * 
 * 
*/

#include <WiFi.h>
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


// PINS SETUP
// DIGITAL PINS
const int TEMP_AND_HUM_PIN = 5;

// ANALOG PINS
const int LUMINOSITY_PIN = 34;
const int SOUND_PIN = 35;

byte temp_and_hum_sensor_data[5];


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
  //execute_command(command);
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


//void execute_command(String command) {
//  
//}


byte read_temp_and_hum_data() {
  byte i = 0;
  byte result = 0;
  for (i = 0; i < 8; i++) {
      while (digitalRead(TEMP_AND_HUM_PIN) == LOW);
      delayMicroseconds(30);
      if (digitalRead(TEMP_AND_HUM_PIN) == HIGH)
        result |= (1 << (8 - i));
    while (digitalRead(TEMP_AND_HUM_PIN) == HIGH);
    }
  return result;
}

void temp_and_hum_sensor_test() {
  digitalWrite(TEMP_AND_HUM_PIN, LOW); 
  delay(30); 
  digitalWrite(TEMP_AND_HUM_PIN, HIGH);
  delayMicroseconds(40); 
  pinMode(TEMP_AND_HUM_PIN, INPUT);
  while(digitalRead(TEMP_AND_HUM_PIN) == HIGH);
  delayMicroseconds(80); 
  if(digitalRead(TEMP_AND_HUM_PIN) == LOW) {
    delayMicroseconds(80); 
  }
  for(int i = 0; i < 5; i++) {
    temp_and_hum_sensor_data[i] = read_temp_and_hum_data();
  }
  pinMode(TEMP_AND_HUM_PIN, OUTPUT);
  digitalWrite(TEMP_AND_HUM_PIN, HIGH); 
}



float get_humidity(byte data[5]) {
//  temp_and_hum_sensor_test();
  float hum_int = String(data[0], DEC).toFloat();
  float hum_dec = String(data[1], DEC).toFloat();
  float hum = hum_int + (hum_dec / 100);
  return hum;
}

float get_temperature(byte data[5]) {
//  temp_and_hum_sensor_test();
  float temp_int = String(data[2], DEC).toFloat();
  float temp_dec = String(data[3], DEC).toFloat();
  float temp = temp_int + (temp_dec / 100);
  return temp;
}

float get_luminosity() {
  int sensorValue = analogRead(LUMINOSITY_PIN);
  float luminosity_percentage = (1.0 - (sensorValue / 4095.0)) * 100;
  return luminosity_percentage;
}

float get_sound() {
  //float db = 20.0 * log10(analogRead(SOUND_PIN) / 4095.0);
  float db = analogRead(SOUND_PIN);
  return db;
}

void setup() {
  Serial.begin(9600);
  delay(3000);
  Serial.println("Initializing...");
  pinMode(TEMP_AND_HUM_PIN, OUTPUT);

//  Serial.print("Connecting to ");
//  Serial.println(ssid);
//  WiFi.mode(WIFI_STA);
//  WiFi.begin(ssid, pass); 
//  WiFi.setHostname("NodeMCU_01");
//  
//  connect_to_wifi();
//
//  net.setCACert(cacert);
//  net.setCertificate(client_cert);
//  net.setPrivateKey(privkey);
//
//  client.setServer(MQTT_HOST, MQTT_PORT);
//  client.setCallback(messageReceived);
//  
//  connect_to_mqtt();
  
}


void loop() {

  delay(3000);
  Serial.println("Loop...");
  
  temp_and_hum_sensor_test();
  
  Serial.print("Humidity = ");
  Serial.print(get_humidity(temp_and_hum_sensor_data));
  Serial.print("%");
  Serial.println();
  
  Serial.print("Temperature = ");
  Serial.print(get_temperature(temp_and_hum_sensor_data));
  Serial.print("C");
  Serial.println();

  
  Serial.print("Luminosity = ");
  Serial.print(get_luminosity());
  Serial.print("%");
  Serial.println();

  Serial.print("Sound = ");
  Serial.print(analogRead(SOUND_PIN));
//  Serial.print(get_sound());
  Serial.println();


  byte checksum = temp_and_hum_sensor_data[0] + temp_and_hum_sensor_data[1] + temp_and_hum_sensor_data[2] + temp_and_hum_sensor_data[3];
  if (temp_and_hum_sensor_data[4] != checksum) 
    Serial.println("-- Checksum Error!");
  else
    Serial.println("-- OK");

  //  if (!client.connected()) {
  //    checkWiFiThenMQTT();
  //  } else {
  //    client.loop();  
  //  }

  delay(2000);
  
}
