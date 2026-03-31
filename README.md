# AI-Based-Cardio-Care
An end-to-end Healthcare IoT solution that bridges embedded systems, cloud data logging, and AI-driven real-time alerting.
Developed as a final-year project, CardioCare is a real-time health monitoring ecosystem designed to enhance patient safety. It transitions from raw sensor data to cloud analytics and proactive voice intervention to identify abnormal cardiac patterns instantly.
Key Features :

Precision Hardware Sensing: Integrates the MAX30102 and DS18B20 sensors to capture high-fidelity Heart Rate, SpO2, and Body Temperature data

AI-Driven Voice Assistant: Features an automated voice alert system (via pyttsx3) that provides immediate spoken warnings for critical conditions like low oxygen (SpO2 < 94%) or abnormal heart rates.

Cloud Connectivity: Real-time data streaming to the ThingSpeak IoT Cloud via REST API for remote patient monitoring and historical tracking.

Emergency SOS Logic: A rule-based classification mechanism designed to detect life-threatening cardiac events and trigger instant local buzzer feedback.

Tech StackLanguages: Python (Alerting Engine), C++ (Arduino Firmware).Hardware: ESP8266 (NodeMCU), MAX30102 PPG Sensor, DS18B20 Temp Sensor.Libraries: PySerial, Pyttsx3, Wire.h, DallasTemperature, ESP8266WiFi.

