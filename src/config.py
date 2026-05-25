import json
import os
import pygame

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "settings.json")

def load_settings():
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading settings: {e}")
    return {"volume": 0.5, "muted": False}

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f)
    except Exception as e:
        print(f"Error saving settings: {e}")

def start_music():
    if not pygame.mixer.get_init():
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Error initializing mixer: {e}")
            return

    if not pygame.mixer.music.get_busy():
        base_sounds = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds")
        possible_names = ["background.mp3", "backgroud_music.mp3"]
        music_path = None
        for name in possible_names:
            path = os.path.join(base_sounds, name)
            if os.path.exists(path):
                music_path = path
                break
        
        if music_path:
            try:
                pygame.mixer.music.load(music_path)
                settings = load_settings()
                vol = 0.0 if settings.get("muted", False) else settings.get("volume", 0.5)
                pygame.mixer.music.set_volume(vol)
                pygame.mixer.music.play(-1)  # Loop indefinitely
            except Exception as e:
                print(f"Error starting music: {e}")
        else:
            print(f"No background music file found in {base_sounds}")

def update_music_volume():
    if pygame.mixer.get_init():
        settings = load_settings()
        vol = 0.0 if settings.get("muted", False) else settings.get("volume", 0.5)
        try:
            pygame.mixer.music.set_volume(vol)
        except Exception as e:
            print(f"Error setting music volume: {e}")
