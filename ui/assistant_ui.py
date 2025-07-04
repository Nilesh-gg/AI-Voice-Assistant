# assistant_ui.py (with text input + voice + response UI)

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QMovie

from core.recognizer import listen_to_voice
from core.tts import speak_text
from core.brain import process_command
from PyQt5.QtGui import QIcon


class VoiceProcessor(QThread):
    response_ready = pyqtSignal(str)

    def run(self):
        user_input = listen_to_voice()
        if user_input:
            response = process_command(user_input)
            speak_text(response)
        else:
            response = "Sorry, I couldn't hear you."
            speak_text(response)
        self.response_ready.emit(response)

class AssistantUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/Nitro.jpg"))  # Ensure this path is correct
        self.setWindowTitle("Voice Assistant")
        self.setGeometry(100, 100, 600, 550)

        # === Inline QSS Styling ===
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QLabel {
                border: none;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ffff;
                border: 1px solid #333;
                border-radius: 10px;
                padding: 8px;
            }
            QLineEdit {
                background-color: #1e1e1e;
                color: #00ffff;
                border: 1px solid #333;
                border-radius: 10px;
                padding: 8px;
            }
            QPushButton {
                background-color: #007acc;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px 20px;
                border: none;
            }
            QPushButton:hover {
                background-color: #0096ff;
            }
        """)

        self.expanded = False

        # === Agent Face (GIF) ===
        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.gif_label.setFixedSize(1366, 768)
        self.gif_label.setScaledContents(True)

        gif_path = os.path.abspath(r"C:\Users\Nilesh\.vscode\VoiceAssistant\ui\agent.gif")
        if not os.path.exists(gif_path):
            self.gif_label.setText("[Missing agent.gif]")
        else:
            self.movie = QMovie(gif_path)
            self.gif_label.setMovie(self.movie)
            self.movie.start()

        # === Expand/Collapse Button ===
        self.toggle_button = QPushButton("⏷")
        self.toggle_button.setFixedSize(30, 30)
        self.toggle_button.clicked.connect(self.toggle_chat_area)

        # === Top layout (GIF + Toggle Button) ===
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.gif_label)
        top_layout.addWidget(self.toggle_button)

        # === Speak Button ===
        self.speak_button = QPushButton("🎤 Speak")
        self.speak_button.clicked.connect(self.start_voice_thread)

        # === Chat Log ===
        self.chat_log = QTextEdit()
        self.chat_log.setReadOnly(True)
        self.chat_log.setFixedHeight(150)

        # === Text Input Box + Send Button ===
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Type your command here...")
        self.input_line.returnPressed.connect(self.handle_text_input)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_text_input)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(self.send_button)

        # === Collapsible Container ===
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.addWidget(self.chat_log)
        self.chat_layout.addLayout(input_layout)
        self.chat_layout.addWidget(self.speak_button)
        self.chat_container.setLayout(self.chat_layout)
        self.chat_container.setVisible(False)

        # === Main Layout ===
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(top_layout)
        self.main_layout.addWidget(self.chat_container)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

    def toggle_chat_area(self):
        self.expanded = not self.expanded
        self.chat_container.setVisible(self.expanded)
        self.toggle_button.setText("⏶" if self.expanded else "⏷")

    def start_voice_thread(self):
        self.speak_button.setEnabled(False)
        self.chat_log.append("🧑 You: [Listening...]")

        self.voice_thread = VoiceProcessor()
        self.voice_thread.response_ready.connect(self.display_response)
        self.voice_thread.start()

    def handle_text_input(self):
        user_text = self.input_line.text().strip()
        if not user_text:
            return
        self.chat_log.append(f"🧑 You: {user_text}")
        response = process_command(user_text)
        speak_text(response)
        self.chat_log.append(f"🤖 Assistant: {response}")
        self.input_line.clear()

    def display_response(self, response):
        self.chat_log.append(f"🤖 Assistant: {response}")
        self.speak_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AssistantUI()
    window.show()
    sys.exit(app.exec_())
