import os
import webbrowser
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from core.spotify_control import handle_spotify_command
import urllib.parse
import subprocess
from core.whatsapp_control import send_whatsapp_message
# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

def process_command(command: str) -> str:
    command = command.lower()

    if "search" in command:
        query = command.replace("search", "").strip()
        if not query:
            return "What do you want me to search?"
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching for {query} on Google."

    

    elif "open" in command:
        app = command.replace("open", "").strip()
        if not app:
            return "What application do you want me to open?"

        app_lower = app.lower()

        try:
            if app_lower in ["spotify"]:
                os.system("start spotify:")
                return "Opening Spotify."

            elif app_lower in ["whatsapp"]:
                os.system("start whatsapp:")
                return "Opening WhatsApp."

            elif app_lower in ["vs code", "vscode", "code"]:
                subprocess.Popen(["code"])
                return "Opening Visual Studio Code."

            elif app_lower == "chrome":
                subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"])
                return "Opening Google Chrome."

            elif app_lower == "brave":
                subprocess.Popen(["C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"])
                return "Opening Brave Browser."

            elif app_lower == "valorant":
                subprocess.Popen(["C:\\Riot Games\\Riot Client\\RiotClientServices.exe"])
                return "Opening Valorant."

            else:
                clean_app = urllib.parse.quote(app_lower.replace(" ", ""))
                url = f"https://www.{clean_app}.com"
                webbrowser.open(url)
                return f"Opening {app.capitalize()} in browser."

        except Exception as e:
            return f"Could not open {app}. Error: {str(e)}"

    elif "time" in command:
        now = datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."

    elif "hello" in command or "hi" in command:
        return "Hello! How can I assist you today?"

    elif "how are you" in command:
        return "I'm just code, but I'm happy to help you!"
    elif "whatsapp message" in command:
        try:
            parts = command.split("to")
            if len(parts) < 2 or "saying" not in parts[1]:
                return "Please say: 'Send WhatsApp message to <name> saying <message>'."

            contact_part, message_part = parts[1].split("saying", 1)
            contact_name = contact_part.strip()
            message = message_part.strip()

            return send_whatsapp_message(contact_name, message)
        except Exception as e:
            return f"Error handling WhatsApp message: {str(e)}"

    elif any(x in command for x in ["spotify", "music", "play", "pause", "next", "previous"]):
        return handle_spotify_command(command)

    # Default to Gemini 1.5 Flash
    try:
        response = model.generate_content(command)
        return response.text.strip()
    except Exception as e:
        return f"Gemini error: {str(e)}"
