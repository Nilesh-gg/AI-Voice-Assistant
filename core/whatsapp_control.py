# core/whatsapp_control.py

import os
import time
import pyautogui

def send_whatsapp_message(contact_name: str, message: str) -> str:
    try:
        # Open WhatsApp using URI scheme
        os.system("start whatsapp:")
        time.sleep(5)  # wait for WhatsApp to open

        # Focus search bar and search for contact
        pyautogui.hotkey("ctrl", "f")
        time.sleep(1)
        pyautogui.typewrite(contact_name)
        time.sleep(1)
        pyautogui.press("enter")

        # Type and send message
        time.sleep(1)
        pyautogui.typewrite(message)
        pyautogui.press("enter")

        return f"Message sent to {contact_name}."
    except Exception as e:
        return f"Failed to send WhatsApp message: {str(e)}"
