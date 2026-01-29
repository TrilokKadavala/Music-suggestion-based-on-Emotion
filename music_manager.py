import webbrowser
import time

class MusicManager:
    def __init__(self):
        # Map emotions to YouTube playlists/videos
        self.mood_links = {
            "sleepy": "https://www.youtube.com/watch?v=FjHGZj2IjBk",    # Lullaby/Relaxing (or energetic if trying to wake up?) - Let's go with relaxing for now or user preference. Actually, if sleepy, maybe wake up? I'll stick to relaxing as per typical mood matching.
            "happy": "https://www.youtube.com/watch?v=ZbZSe6N_BXs",     # Happy
            "sad": "https://www.youtube.com/watch?v=RgKAFK5djSk",       # Sad
            "angry": "https://www.youtube.com/watch?v=lWA2pjMjpBs",     # Calming
            "neutral": "https://www.youtube.com/watch?v=5qap5aO4i9A",   # Lo-fi / Chill
            "fear": "https://www.youtube.com/watch?v=4PKwMzC5kew",      # Calming
            "surprise": "https://www.youtube.com/watch?v=HArcdE_36sg"   # Energetic
        }
        self.last_open_time = 0
        self.cooldown = 10  # Seconds between opening links

    def play_music(self, mood):
        current_time = time.time()
        
        # Check cooldown to avoid spamming tabs
        if current_time - self.last_open_time < self.cooldown:
            return

        mood = mood.lower()
        if mood in self.mood_links:
            url = self.mood_links[mood]
            print(f"Opening music for mood: {mood} -> {url}")
            webbrowser.open(url)
            self.last_open_time = current_time
        else:
            print(f"No specific playlist for mood: {mood}")
