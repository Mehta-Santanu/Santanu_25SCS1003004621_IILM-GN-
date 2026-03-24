# ---------------------------------------------------------
# AI Intrusion Detection System
# YOLOv8 + Voice STOP + Safe Hand Gesture STOP + Alarm
# ---------------------------------------------------------

import cv2
from ultralytics import YOLO
import datetime
import os
import speech_recognition as sr
import threading
import time
from playsound import playsound
import numpy as np

# ---------------------------------------------------------
# GLOBAL VARIABLES
# ---------------------------------------------------------
stop_event = threading.Event()
last_alert_time = 0
ALERT_COOLDOWN = 3
PROCESS_EVERY = 3
frame_count = 0

# Hand gesture confirmation timer
hand_start_time = [None]

# ---------------------------------------------------------
# LOAD YOLO MODEL & CAMERA
# ---------------------------------------------------------
print("Loading YOLOv8 model...")
model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not cap.isOpened():
    print("❌ Camera not found!")
    exit()

# ---------------------------------------------------------
# CREATE FOLDER
# ---------------------------------------------------------
os.makedirs("intruder_images", exist_ok=True)

# ---------------------------------------------------------
# VOICE COMMAND THREAD (STOP)
# ---------------------------------------------------------
def listen_for_stop():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.5)

    print("🎙 Voice listener active (Say STOP)")

    while not stop_event.is_set():
        try:
            with mic as source:
                audio = r.listen(source, timeout=1, phrase_time_limit=1)

            command = r.recognize_google(audio).lower()
            if "stop" in command:
                print("🛑 VOICE STOP DETECTED")
                stop_event.set()

        except:
            continue

threading.Thread(target=listen_for_stop, daemon=True).start()

# ---------------------------------------------------------
# SAFE HAND GESTURE STOP (OPENCV ONLY)
# ---------------------------------------------------------
def hand_stop_detected(frame, timer_holder):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Strict skin range
    lower_skin = np.array([0, 30, 80], dtype=np.uint8)
    upper_skin = np.array([20, 180, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=1)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    h, w, _ = frame.shape

    for cnt in contours:
        area = cv2.contourArea(cnt)

        # 1️⃣ Area filter (ignore face/body)
        if area < 18000 or area > 80000:
            continue

        x, y, cw, ch = cv2.boundingRect(cnt)

        # 2️⃣ Aspect ratio filter (hand-like)
        aspect_ratio = cw / float(ch)
        if aspect_ratio < 0.5 or aspect_ratio > 1.8:
            continue

        # 3️⃣ Position filter (TOP-RIGHT only)
        if x < w * 0.6 or y > h * 0.5:
            continue

        # 4️⃣ Time confirmation (1 second hold)
        if timer_holder[0] is None:
            timer_holder[0] = time.time()
        elif time.time() - timer_holder[0] >= 1.0:
            cv2.rectangle(frame, (x, y), (x + cw, y + ch), (255, 0, 0), 2)
            return True

    timer_holder[0] = None
    return False

# ---------------------------------------------------------
# DRAW YOLO BOXES
# ---------------------------------------------------------
def draw_boxes(frame, results):
    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2),
                              (0, 0, 255), 2)
                cv2.putText(frame, "INTRUDER",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 0, 255), 2)
    return frame

# ---------------------------------------------------------
# PLAY ALARM
# ---------------------------------------------------------
def play_alarm():
    try:
        playsound("alarm.wav")
    except:
        pass

# ---------------------------------------------------------
# HANDLE INTRUSION
# ---------------------------------------------------------
def handle_intrusion(frame):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    cv2.imwrite(f"intruder_images/intruder_{timestamp}.jpg", frame)

    with open("intruder_log.txt", "a") as f:
        f.write(f"Intruder detected at {timestamp}\n")

    play_alarm()

# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------
print("\n✅ System Ready")
print("👉 Say STOP | Show ✋ in TOP-RIGHT for 1s | Press Q to exit\n")

results = []

while not stop_event.is_set():

    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # ---------------- HAND STOP CHECK ----------------
    if hand_stop_detected(frame, hand_start_time):
        cv2.putText(frame, "HAND STOP CONFIRMED",
                    (40, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 0, 0), 3)
        print("✋ HAND STOP CONFIRMED")
        stop_event.set()

    # ---------------- YOLO DETECTION ----------------
    if frame_count % PROCESS_EVERY == 0:
        results = model(frame, conf=0.6, verbose=False)

    frame = draw_boxes(frame, results)

    intruder_detected = any(
        int(box.cls[0]) == 0
        for r in results for box in r.boxes
    )

    current_time = time.time()
    if intruder_detected and (current_time - last_alert_time) > ALERT_COOLDOWN:
        last_alert_time = current_time
        print("🚨 INTRUDER DETECTED")

        threading.Thread(
            target=handle_intrusion,
            args=(frame.copy(),),
            daemon=True
        ).start()

    cv2.imshow("AI Intrusion Detection System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        stop_event.set()

# ---------------------------------------------------------
# CLEAN EXIT
# ---------------------------------------------------------
cap.release()
cv2.destroyAllWindows()
stop_event.set()

print("\n✅ Program stopped successfully.")
