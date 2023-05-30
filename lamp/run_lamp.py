import os
import sys

from gui import LampBrowserWindow
from lamp_core import Lamp
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    lamp = Lamp()
    app: QApplication = QApplication([])
    app.setStyleSheet(open(os.path.join("ui", "style", "style.qss"), "r").read())
    window: LampBrowserWindow = LampBrowserWindow(lamp)
    window.show()
    sys.exit(app.exec())
