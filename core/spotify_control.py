import os
import time
import pyautogui
import keyboard


def search_and_play_on_spotify_app(query: str) -> str:
    # Step 1: Launch Spotify via URI protocol
    os.system('start spotify:')
    time.sleep(6)  # Wait for the app to fully load and be ready

    # Step 2: Search and play song
    pyautogui.hotkey('ctrl', 'l')                  # Focus search bar
    time.sleep(0.3)
    pyautogui.typewrite(query)                     # Type the query
    time.sleep(0.3)
    pyautogui.press('enter')                       # Search
    time.sleep(2.5)                                # Wait for results
    pyautogui.press('tab', presses=1, interval=0.1)
    time.sleep(0.2)
    pyautogui.press('enter', presses=2, interval=1)

    return f"Searched and played '{query}' in Spotify."


def handle_spotify_command(command: str) -> str:
    command = command.lower()

    # Handle "play [song] on spotify"
    if command.startswith("play ") and "on spotify" in command:
        query = command[5:].replace("on spotify", "").strip()
        if query:
            return search_and_play_on_spotify_app(query)

    # Basic media controls (requires Spotify focused)
    if "play" in command or "resume" in command:
        keyboard.send("play/pause media")
        return "Playing music."

    elif "pause" in command or "stop" in command:
        keyboard.send("play/pause media")
        return "Paused music."

    elif "next" in command:
        keyboard.send("next track media")
        return "Skipped to next track."

    elif "previous" in command or "back" in command:
        keyboard.send("previous track media")
        return "Went to previous track."

    return "Try saying 'play [song name] on Spotify', 'pause music', or 'next song'."
