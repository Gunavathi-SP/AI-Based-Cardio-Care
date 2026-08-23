# ❤️ AI-Based CardioCare

An IoT-based healthcare monitoring system designed to continuously monitor vital health parameters and provide real-time alerts when abnormal readings are detected.

**CardioCare** bridges the gap between physical health sensors, cloud-based monitoring, and real-time alert mechanisms by combining **IoT hardware, Python, cloud connectivity, and automated voice alerts**.

---

## 🎯 Project Overview

Monitoring vital health parameters continuously can help identify potentially dangerous conditions at an early stage.

CardioCare is a final-year project that collects real-time health data using sensors connected to an **ESP8266 NodeMCU**, sends the data to the **ThingSpeak IoT Cloud** for remote monitoring and historical tracking, and provides immediate local and voice-based alerts when critical conditions are detected.

The system monitors:

❤️ Heart Rate  
🫁 SpO₂ (Blood Oxygen Level)  
🌡️ Body Temperature  

---

## ✨ Key Features

### ❤️ Precision Health Monitoring

Uses dedicated sensors to capture real-time vital parameters:

- **MAX30102 PPG Sensor**
  - Heart Rate
  - SpO₂

- **DS18B20 Temperature Sensor**
  - Body Temperature

### 🔊 AI-Assisted Voice Alerts

Uses Python's **pyttsx3** library to generate automated voice warnings when predefined critical conditions are detected.

For example:

```text
SpO₂ < 94%
       ↓
Critical condition detected
       ↓
Alert generated
       ↓
Voice warning played
