
# 🔐 AI Defence — Intrusion Detection System

**Real-time human detection via webcam using YOLOv8 + OpenCV**

## 📖 Overview

**AI Defence** is a real-time security system that uses computer vision and deep learning to detect human intruders through a standard webcam. It combines state-of-the-art object detection with smart alert mechanisms and intuitive controls — making surveillance intelligent, autonomous, and easy to use.

> Suitable for smart home security, office monitoring, academic research, and AI/CV learning projects.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🧠 **Real-Time Detection** | YOLOv8-powered human detection with high accuracy and low latency |
| 🎥 **Live Webcam Feed** | Continuous video stream processing via OpenCV |
| 🔊 **Alarm System** | Instant audio alert triggered on intruder detection |
| 📝 **Auto Logging** | Saves intruder images + timestamped log entries automatically |
| 🎙️ **Voice Control** | Say `"STOP"` to disarm — hands-free deactivation |
| ✋ **Gesture Stop** | Show an open palm for ~1 second to halt the system |
| ⚡ **Multithreaded** | Concurrent threads for camera, audio, and voice I/O |

---

## 🛠️ Tech Stack

- **Language:** Python 3.8+
- **Detection Model:** YOLOv8 (Ultralytics)
- **Computer Vision:** OpenCV
- **Voice Recognition:** SpeechRecognition (Google API backend)
- **Array Processing:** NumPy
- **Audio Playback:** Playsound `== 1.2.2`

---

## ⚙️ Installation

**1. Clone the repository**
git clone https://github.com/Mehta-Santanu/Santanu_25SCS1003004621_IILM-GN-
```

**2. Install dependencies**
pip install ultralytics opencv-python speechrecognition playsound==1.2.2 numpy
```

**3. Run the system**
python main.py
```

---

## 🎮 Controls

| Action | Method |
|---|---|
| Stop the system | 🎙️ Say **"STOP"** |
| Stop the system | ✋ Show **open palm** for ~1 second |
| Exit the program | ⌨️ Press **`Q`** |

---

## 📂 Project Structure

```
AI Defence and Detect Intrusion/
main.py
alarm.wav
intruder_images
intruder_log.txt
README.md
```

---

## 📌 Applications

- 🏠 Smart home security
- 🏢 Office & workplace surveillance
- 🤖 AI-based autonomous monitoring
- 🎓 Academic & computer vision research projects

---

## 🔮 Future Enhancements

- [ ] Face recognition — distinguish known vs unknown individuals
- [ ] Mobile push notifications on detection
- [ ] Automatic video recording on intruder detection
- [ ] Advanced gesture control system
- [ ] Web dashboard for remote monitoring

---

## 👨‍💻 Author

**Angshul**  
B.Tech CSE | AI & Cybersecurity Enthusiast

---

## ⭐ Support

If you found this project useful, please consider giving it a **star** — it helps others discover it and motivates further development!

[![Star this repo](https://github.com/Mehta-Santanu)
