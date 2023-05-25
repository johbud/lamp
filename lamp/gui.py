from functools import partial

from config import Config
from lamp_core import Lamp
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LampBrowserWindow(QMainWindow):
    """The main browser window"""

    def __init__(self, lamp_instance: Lamp) -> None:
        super().__init__(parent=None)
        self._lamp = lamp_instance
        self.setWindowTitle("Lamp")
        self._general_layout = QVBoxLayout()
        central_widget = QWidget(self)
        central_widget.setLayout(self._general_layout)
        self.setCentralWidget(central_widget)
        self._create_menu()
        self._create_task_group()

    def update

    def _create_menu(self) -> None:
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Open project")
        menu.addAction("&Settings")
        menu.addAction("&Exit", self.close)

    def _create_task_group(self) -> None:
        layout = QVBoxLayout()
        task_group = QGroupBox("Tasks")
        task_group.setLayout(layout)

        btn_add_task = QPushButton("Add task")
        btn_remove_task = QPushButton("Remove task")
        btn_edit_task = QPushButton("Edit task")

        wgt_tasks = self._make_task_list()

        btn_add_task.clicked.connect(self._btn_add_task)
        btn_remove_task.clicked.connect(self._btn_remove_task)
        btn_edit_task.clicked.connect(self._btn_edit_task)

        layout.addWidget(btn_add_task)
        layout.addWidget(btn_remove_task)
        layout.addWidget(btn_edit_task)
        layout.addWidget(wgt_tasks)

        self._general_layout.addWidget(task_group)

    def _make_task_list(self) -> QListWidget:
        tasks = self._lamp.find_tasks(Config.project_path)
        wgt_tasks = QListWidget()
        for task in tasks:
            wgt_tasks.addItem(task)
        return wgt_tasks

    def _btn_add_task(self) -> None:
        dialog = AddTaskDialog(self._lamp)
        dialog.exec()

    def _btn_remove_task(self) -> None:
        pass

    def _btn_edit_task(self) -> None:
        pass


class AddTaskDialog(QDialog):
    """Dialog for adding a task"""

    def __init__(self, lamp_instance: Lamp) -> None:
        super().__init__(parent=None)
        self._lamp = lamp_instance
        self.setWindowTitle("Add task")
        dialog_layout = QVBoxLayout()
        self.task_name_field = QLineEdit(self, placeholderText="Task name")
        buttons = QDialogButtonBox()
        buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._btn_ok)
        buttons.rejected.connect(self._btn_cancel)
        dialog_layout.addWidget(self.task_name_field)
        dialog_layout.addWidget(buttons)
        self.setLayout(dialog_layout)
        self.show()

    def _btn_ok(self) -> None:
        self._lamp.add_task(Config.project_path, self.task_name_field.text())
        self.close()

    def _btn_cancel(self) -> None:
        self.close()
