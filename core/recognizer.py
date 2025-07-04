import speech_recognition as sr

def listen_to_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
            print("✅ Recognizing...")
            return recognizer.recognize_google(audio)
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return "Sorry, speech recognition service failed."

