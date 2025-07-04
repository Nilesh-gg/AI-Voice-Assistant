import sys
from PyQt5.QtWidgets import QApplication
from ui.assistant_ui import AssistantUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AssistantUI()
    window.show()
    sys.exit(app.exec_())
