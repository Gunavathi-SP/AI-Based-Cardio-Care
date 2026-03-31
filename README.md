# AI-Based-Cardio-Care
CardioCare is a comprehensive Healthcare IoT solution designed to bridge the gap between raw medical sensor data and proactive patient safety. Developed as a final-year project, this system transitions from high-fidelity hardware sensing to cloud-based historical tracking and real-time AI voice intervention.
Key Features:
Precision Hardware Sensing: Integrated MAX30102 (PPG) and DS18B20 sensors to capture high-fidelity Heart Rate, SpO2, and Body Temperature data.

AI-Driven Voice Assistant: Features an automated alerting engine (via pyttsx3) that provides immediate spoken warnings for critical conditions (e.g., SpO2 < 94%).

Cloud Connectivity: Seamless data streaming to the ThingSpeak IoT Cloud via REST API for remote monitoring and data logging.

Emergency SOS Logic: A rule-based mechanism that triggers local buzzer feedback and remote alerts upon detecting abnormal cardiac patterns.

Tech Stack:
  -Languages : Python (Alerting Engine), C++ (Arduino Firmware)
  -Hardware  : ESP8266 (NodeMCU), MAX30102 PPG Sensor, DS18B20 Temp Sensor
  -Cloud/API : ThingSpeak IoT Platform, RESTful API Integration
  -Libraries : Pyttsx3, PySerial, Wire.h, DallasTemperature, ESP8266WiFi
