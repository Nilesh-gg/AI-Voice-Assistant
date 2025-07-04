# hotkey_or_wake.py (with tray icon, universal path, and startup addition)

import keyboard
import threading
import subprocess
import speech_recognition as sr
import os
import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
import ctypes

# --- Universal path resolution ---
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

APP_PATH = os.path.join(BASE_DIR, "dist/app.exe")  # or use "dist/app.exe" when packaged

# --- Add to Windows startup ---
def add_to_startup():
    exe_path = os.path.abspath(sys.argv[0])
    startup_dir = os.path.join(os.getenv("APPDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup")
    bat_path = os.path.join(startup_dir, "LaunchNitro.bat")

    if not os.path.exists(bat_path):
        with open(bat_path, "w") as f:
            f.write(f'start "" "{exe_path}"')
        print("✅ Nitro added to Windows startup.")
    else:
        print("ℹ️ Nitro is already set to launch at startup.")

# --- Tray Icon Setup ---
def show_tray_icon():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    icon_path = os.path.join(BASE_DIR, "assets", "Nitro.jpg")  # Make sure this exists
    tray_icon = QSystemTrayIcon(QIcon(icon_path), parent=app)

    tray_menu = QMenu()
    open_action = QAction("Launch Assistant")
    open_action.triggered.connect(launch_assistant)
    exit_action = QAction("Exit")
    exit_action.triggered.connect(app.quit)
    tray_menu.addAction(open_action)
    tray_menu.addSeparator()
    tray_menu.addAction(exit_action)

    tray_icon.setContextMenu(tray_menu)
    tray_icon.setToolTip("Nitro Assistant Listener")
    tray_icon.show()
    ctypes.windll.user32.MessageBoxW(0, "Nitro is running in background.", "Nitro Assistant", 0x40 | 0x1)

    sys.exit(app.exec_())

# --- HOTKEY TRIGGER ---
def hotkey_listener():
    print("🔵 Press Ctrl+Alt+N to launch the assistant.")
    keyboard.add_hotkey("ctrl+alt+n", launch_assistant)
    keyboard.wait()

# --- WAKE WORD TRIGGER ---
def wake_word_listener():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Say 'Hey Nitro' to launch the assistant.")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        try:
            with mic as source:
                print("🎧 Listening for wake word...")
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)
            query = recognizer.recognize_google(audio).lower()
            print("Heard:", query)
            if "hey nitro" in query:
                print("🚀 Wake word detected!")
                launch_assistant()
        except sr.WaitTimeoutError:
            print("⏱️ No voice detected within timeout.")
            continue
        except sr.UnknownValueError:
            print("🤐 Couldn’t understand.")
            continue
        except sr.RequestError:
            print("⚠️ Speech service unavailable.")
        except Exception as e:
            print("❌ Error:", e)

# --- Launch the assistant app ---
def launch_assistant():
    try:
        if APP_PATH.endswith(".py"):
            subprocess.Popen(["python", APP_PATH])
        else:
            subprocess.Popen([APP_PATH])
        print("🚀 Assistant launched!")
    except Exception as e:
        print(f"❌ Failed to launch assistant: {e}")

# --- START LISTENERS ---
if __name__ == "__main__":
    add_to_startup()
    threading.Thread(target=hotkey_listener, daemon=True).start()
    threading.Thread(target=wake_word_listener, daemon=True).start()
    show_tray_icon()
