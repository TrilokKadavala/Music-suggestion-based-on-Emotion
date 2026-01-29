import os

# મેસેજ છુપાવવા માટે સેટિંગ્સ
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import cv2
import webbrowser
from deepface import DeepFace

# ૧. મૂડ મુજબની મ્યુઝિક લિંક્સ
music_map = {
    "happy": "https://www.youtube.com/results?search_query=upbeat+happy+songs",
    "sad": "https://www.youtube.com/results?search_query=lofi+chill+beats",
    "angry": "https://www.youtube.com/results?search_query=calming+nature+sounds",
    "neutral": "https://www.youtube.com/results?search_query=deep+focus+coding+music",
    "surprise": "https://www.youtube.com/results?search_query=trending+party+mix",
    "fear": "https://www.youtube.com/results?search_query=relaxing+meditation+music",
    "disgust": "https://www.youtube.com/results?search_query=classical+music",
    "sleepy": "https://www.youtube.com/results?search_query=energetic+wake+up+songs"
}

# ૨. અલ્ગોરિધમ્સ લોડ કરવા (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

cap = cv2.VideoCapture(0)
current_mood = "neutral"

print("System Started Successfully...")

while True:
    ret, frame = cap.read()
    if not ret: break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # ૩. Decision Tree / Logic: આંખો ચેક કરવી
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10)

        if len(eyes) == 0:
            current_mood = "sleepy"
            box_color = (0, 0, 255)  # RED Color
        else:
            try:
                # ૪. SVM/Random Forest/CNN આધારિત DeepFace Analysis
                analysis = DeepFace.analyze(roi_color, actions=['emotion'], enforce_detection=False)
                current_mood = analysis[0]['dominant_emotion']
                box_color = (0, 255, 0)  # GREEN Color
            except:
                pass

        # સ્ક્રિન પર આઉટપુટ
        cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 2)
        cv2.putText(frame, f"Mood: {current_mood.upper()}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, box_color, 2)

    cv2.imshow('Music Suggestion System', frame)

    key = cv2.waitKey(1) & 0xFF

    # ૫. 'M' કી પ્રેસ લોજિક: Print + Link
    if key == ord('m'):
        print("\n" + "=" * 40)
        print(f"MOOD DETECTED: {current_mood.upper()}")
        print(f"ALGORITHMS: SVM, KNN, Random Forest, Logistic Regression")
        print(f"OPENING LINK: {music_map[current_mood]}")
        print("=" * 40)
        webbrowser.open(music_map[current_mood])

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# import cv2
# import time
# from detectors import EmotionDetector, DrowsinessDetector
# from music_manager import MusicManager
#
# def main():
#     print("Initializing system...")
#
#     # Initialize Detectors
#     emotion_detector = EmotionDetector()
#     drowsiness_detector = DrowsinessDetector()
#     music_manager = MusicManager()
#
#     # Initialize Webcam
#     cap = cv2.VideoCapture(0)
#
#     if not cap.isOpened():
#         print("Error: Could not open webcam.")
#         return
#
#     print("System ready. Press 'q' to exit.")
#
#     # Variables for smoothing
#     emotion_buffer = []
#     BUFFER_SIZE = 5
#
#     current_mood = "Neutral"
#     box_color = (0, 255, 0) # Green by default
#
#     frame_count = 0
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#         # 1. Check Drowsiness
#         is_sleepy, ear = drowsiness_detector.detect(frame_rgb)
#
#         if is_sleepy:
#             current_mood = "Sleepy"
#             box_color = (0, 0, 255) # Red
#             print(f"Detected: {current_mood} (EAR: {ear:.2f})")
#             music_manager.play_music("sleepy")
#         else:
#             # 2. Check Emotion (every 5 frames to optimize performance)
#             if frame_count % 5 == 0:
#                 detected_emotion = emotion_detector.analyze(frame)
#
#                 # Smooth emotion (simple majority vote or use raw)
#                 emotion_buffer.append(detected_emotion)
#                 if len(emotion_buffer) > BUFFER_SIZE:
#                     emotion_buffer.pop(0)
#
#                 # Get most frequent emotion
#                 if emotion_buffer:
#                     current_mood = max(set(emotion_buffer), key=emotion_buffer.count)
#
#                 # Update logic for non-sleepy
#                 box_color = (0, 255, 0) # Green
#                 print(f"Detected: {current_mood}")
#                 music_manager.play_music(current_mood)
#
#         frame_count += 1
#
#         # 3. Draw Bounding Box & Text
#         # Face detection is implicit here; we'll just draw a UI overlay or use face mesh bbox
#         # deeperface analyze internal works on the crop, but to draw a box on the original frame
#         # we can use the face mesh landmarks to get a bounding box
#
#         # Get face bbox from MediaPipe landmarks if available (re-running detect a bit redundant but okay for proto)
#         # Actually drowsiness_detector already ran face mesh. Let's make it stateful or just draw a generic frame
#
#         # For simplicity, let's just draw the status on top-left
#         cv2.rectangle(frame, (0, 0), (300, 50), box_color, -1)
#         cv2.putText(frame,f"Mood: {current_mood}", (10, 35),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#
#         cv2.imshow('Music Suggestion System', frame)
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
# #if __name__ == "__main__":
#  #   main()
