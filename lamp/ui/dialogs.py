from typing import Tuple

from PyQt6.QtWidgets import QInputDialog, QMessageBox, QWidget


def display_error(message: str) -> None:
    """Display an error message"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setText(message)
    msg.setWindowTitle("Error")
    msg.exec()


def display_info(message: str) -> None:
    """Display an info message"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setText(message)
    msg.setWindowTitle("Info")
    msg.exec()


def new_project_dialog_open(parent: QWidget) -> str:
    """Open the new project dialog"""

    title = "New Project"
    label = "Project Name:"
    project_name: str = QInputDialog.getText(parent, title, label)[0]
    return project_name


def add_task_dialog_open(parent: QWidget) -> str:
    """Open the new task dialog"""

    title = "New Task"
    label = "Task Name:"
    task_name: str = QInputDialog.getText(parent, title, label)[0]

    return task_name


def add_folder_dialog_open(parent: QWidget) -> str:
    """Open the new folder dialog"""

    title = "New Folder"
    label = "Folder Name:"
    folder_name: str = QInputDialog.getText(parent, title, label)[0]

    return folder_name
