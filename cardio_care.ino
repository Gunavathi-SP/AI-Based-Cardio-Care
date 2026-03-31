#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"
#include "spo2_algorithm.h"
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// ------------------- WiFi + ThingSpeak --------------------
const char* WIFI_SSID = "Project";
const char* WIFI_PASS = "harshitha";
const char* THINGSPEAK_API_KEY = "AESSI3XACM5SSR61";
// -----------------------------------------------------------

// MAX30102
MAX30105 particleSensor;

// DS18B20 Temperature
#define ONE_WIRE_BUS 14 // D5
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature tempSensor(&oneWire);

// HRM-2511-E Finger Sensor
#define FINGER_PIN A0

// Buzzer Pin
#define BUZZER_PIN 12 // D6

// Thresholds
int fingerThreshold = 200;
uint32_t maxIRThreshold = 1000;

// IR Buffer
const byte bufferLength = 100;
uint32_t irBuffer[bufferLength];
uint32_t redBuffer[bufferLength];

// Output Variables
int32_t spo2;
int8_t validSPO2;
int32_t heartRate;
int8_t validHeartRate;

void setup() {
  Serial.begin(115200);
  pinMode(BUZZER_PIN, OUTPUT);

  Wire.begin(4, 5); // SDA = D2, SCL = D1

  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30102 not found");
    while (1);
  }

  particleSensor.setup(
    60,
    4,
    2,
    100,
    411,
    16384
  );

  // ---------------- WiFi Connection ----------------
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected!");
  // ---------------------------------------------------

  tempSensor.begin();
  Serial.println("System Ready - Place Finger on Sensor");
}

void loop() {

  int fingerValue = analogRead(FINGER_PIN);
  uint32_t irValue = particleSensor.getIR();

  if (fingerValue > fingerThreshold && irValue > maxIRThreshold) {

    beepPattern();

    // Collect Data
    for (byte i = 0; i < bufferLength; i++) {
      redBuffer[i] = particleSensor.getRed();
      irBuffer[i] = particleSensor.getIR();

      if (irBuffer[i] < maxIRThreshold) {
        Serial.println("Keep finger steady...");
        return;
      }
      delay(20);
    }

    maxim_heart_rate_and_oxygen_saturation(
      irBuffer, bufferLength,
      redBuffer,
      &spo2, &validSPO2,
      &heartRate, &validHeartRate
    );

    tempSensor.requestTemperatures();
    float tempC = tempSensor.getTempCByIndex(0);
    float tempF = tempC * 1.8 + 32;

    int showSpO2 = (validSPO2 && spo2 > 70 && spo2 < 100) ? spo2 : 0;
    int showHR = (validHeartRate && heartRate > 40 && heartRate < 180) ? heartRate : 0;

    Serial.print("BPM: ");
    Serial.print(showHR);
    Serial.print(" | SpO2: ");
    Serial.print(showSpO2);
    Serial.print(" | Temp: ");
    Serial.print(tempF);
    Serial.println(" °F");

    // ----------------------------------------------------
    //            SEND DATA TO THINGSPEAK
    // ----------------------------------------------------
    if (WiFi.status() == WL_CONNECTED) {

      HTTPClient http;

      String url = "http://api.thingspeak.com/update?api_key=" +
                   String(THINGSPEAK_API_KEY) +
                   "&field1=" + String(showHR) +
                   "&field2=" + String(showSpO2) +
                   "&field3=" + String(tempF);

     WiFiClient client;
http.begin(client, url);

      int httpResponseCode = http.GET();

      Serial.print("ThingSpeak Response: ");
      Serial.println(httpResponseCode);

      http.end();
    }
    else {
      Serial.println("WiFi Disconnected. Unable to send data.");
    }

  }
  else {
    Serial.println("Place Finger Properly!");
    digitalWrite(BUZZER_PIN, LOW);
    delay(300);
  }
}

void beepPattern() {
  digitalWrite(BUZZER_PIN, HIGH);
  delay(600);
  digitalWrite(BUZZER_PIN, LOW);
  delay(500);
}
