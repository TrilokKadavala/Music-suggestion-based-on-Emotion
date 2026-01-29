import streamlit as st
import cv2
from deepface import DeepFace
import webbrowser

st.set_page_config(page_title="Music Suggestion Based On Emotion")

st.title("🎵 Music Suggestion Based On Emotion")
st.write("Click Start Camera and detect your emotion")

music_map = {
    "happy": "https://www.youtube.com/results?search_query=upbeat+happy+songs",
    "sad": "https://www.youtube.com/results?search_query=lofi+sad+songs",
    "angry": "https://www.youtube.com/results?search_query=calm+relaxing+music",
    "neutral": "https://www.youtube.com/results?search_query=chill+music"
}

start = st.button("Start Camera")

if start:

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if ret:

        st.image(frame, channels="BGR")

        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        emotion = result[0]['dominant_emotion']

        st.success(f"Detected Emotion: {emotion}")

        if emotion in music_map:
            link = music_map[emotion]

            st.markdown(f"### 🎧 Recommended Music")
            st.markdown(f"[Click Here To Open Music]({link})")

    cap.release()
