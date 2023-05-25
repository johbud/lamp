import sys

from gui import LampBrowserWindow
from lamp_core import Lamp
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    lamp = Lamp()
    app = QApplication([])
    window = LampBrowserWindow(lamp)
    window.show()
    sys.exit(app.exec())
