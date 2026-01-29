import cv2
import mediapipe as mp
import numpy as np
from deepface import DeepFace

class DrowsinessDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Eye landmarks (MediaPipe ref)
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        
        self.EAR_THRESHOLD = 0.25  # Threshold for "Sleepy"

    def calculate_ear(self, landmarks, indices):
        # Vertical lines
        A = np.linalg.norm(np.array(landmarks[indices[1]]) - np.array(landmarks[indices[5]]))
        B = np.linalg.norm(np.array(landmarks[indices[2]]) - np.array(landmarks[indices[4]]))
        # Horizontal line
        C = np.linalg.norm(np.array(landmarks[indices[0]]) - np.array(landmarks[indices[3]]))
        ear = (A + B) / (2.0 * C)
        return ear

    def detect(self, frame_rgb):
        results = self.face_mesh.process(frame_rgb)
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            h, w, c = frame_rgb.shape
            
            # Convert to pixel coordinates
            coords = [(int(l.x * w), int(l.y * h)) for l in landmarks]
            
            left_ear = self.calculate_ear(coords, self.LEFT_EYE)
            right_ear = self.calculate_ear(coords, self.RIGHT_EYE)
            
            avg_ear = (left_ear + right_ear) / 2.0
            
            if avg_ear < self.EAR_THRESHOLD:
                return True, avg_ear  # Sleepy
            return False, avg_ear
        return False, 0.0

class EmotionDetector:
    def analyze(self, frame):
        try:
            # DeepFace analyze
            # enforce_detection=False to avoid crashing if no face found in small crop
            results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, silent=True)
            if results:
                return results[0]['dominant_emotion']
        except Exception as e:
            # print(f"Emotion error: {e}")
            pass
        return "neutral"
