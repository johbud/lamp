import os

from lamp_core import Lamp
from models import ProjectListModel, make_task_tree
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow
from ui.dialogs import (
    add_folder_dialog_open,
    add_task_dialog_open,
    display_error,
    display_info,
    new_project_dialog_open,
)


class LampBrowserWindow(QMainWindow):
    """The main browser window"""

    def __init__(self, lamp_instance: Lamp) -> None:
        super().__init__(parent=None)
        self._lamp: Lamp = lamp_instance
        uic.loadUi(os.path.join("ui", "project_browser.ui"), self)
        self.list_projects_model = ProjectListModel(self._lamp.find_projects())
        self.list_projects.setModel(self.list_projects_model)

        self.tree_tasks.setModel(
            make_task_tree(self._lamp.find_tasks(self._lamp.current_project))
        )

        # self.tbl_workfiles.setModel()

        self._connect_signals()

    def _connect_signals(self) -> None:
        """Connect signals to slots"""
        self.btn_open_project.clicked.connect(self._btn_open_project)
        self.btn_new_project.clicked.connect(self._btn_new_project)
        self.btn_dailies.clicked.connect(self._btn_dailies)

        self.btn_add_folder.clicked.connect(self._btn_add_folder)
        self.btn_add_task.clicked.connect(self._btn_add_task)
        self.btn_del_task.clicked.connect(self._btn_del_task)
        self.btn_output.clicked.connect(self._btn_output)

        self.btn_add_workfile.clicked.connect(self._btn_add_workfile)
        self.btn_add_existing_workfile.clicked.connect(self._btn_add_existing_workfile)

    def _btn_open_project(self) -> None:
        """Open the selected project"""
        if len(self.list_projects.selectedIndexes()) == 0:
            return
        self._lamp.set_current_project(
            self.list_projects.model().itemFromIndex(
                self.list_projects.selectedIndexes()[0]
            )
        )

        self.tree_tasks.setModel(
            make_task_tree(self._lamp.find_tasks(self._lamp.current_project))
        )

    def _btn_new_project(self) -> None:
        """Create a new project"""
        project_name: str = new_project_dialog_open(self)
        if project_name:
            result: bool | Exception = self._lamp.create_project(project_name)
            if isinstance(result, Exception):
                display_error(str(result))
            else:
                display_info(f"Project {project_name} created successfully")
                self.list_projects_model = ProjectListModel(self._lamp.find_projects())
                self.list_projects.setModel(self.list_projects_model)

    def _btn_dailies(self) -> None:
        """Open the dailies folder"""
        self._lamp.open_dailies()

    def _btn_add_folder(self) -> None:
        """Add a folder"""

        if len(self.tree_tasks.selectedIndexes()) != 0:
            if (
                self.tree_tasks.selectedIndexes()[0]
                .data(role=Qt.ItemDataRole.UserRole)
                .is_task
            ):
                display_error("Cannot add folder to a task")
                return

        folder_name: str = add_folder_dialog_open(self)
        if len(self.tree_tasks.selectedIndexes()) == 0:
            parents: list[str] = []
        else:
            parents: list[str] = [self.tree_tasks.selectedIndexes()[0].data().name]
            parent = self.tree_tasks.selectedIndexes()[0].parent()
            while parent.data():
                print(parent.data())
                parents.append(parent.data().name)
                parent = parent.parent()

        project_path: str = self._lamp.current_project.project_path

        if folder_name:
            result: bool | Exception = self._lamp.add_folder(
                project_path, folder_name, parents
            )
            if isinstance(result, Exception):
                display_error(str(result))
            else:
                display_info(f"Folder {folder_name} created successfully")
                self.tree_tasks.setModel(
                    make_task_tree(self._lamp.find_tasks(self._lamp.current_project))
                )
        else:
            display_error("Folder name cannot be empty")

    def _btn_add_task(self) -> None:
        """Add a task"""
        task_name: str = add_task_dialog_open(self)

        # is parent selected?
        if len(self.tree_tasks.selectedIndexes()) == 0:
            parents: list[str] = []

        else:
            if (
                self.tree_tasks.selectedIndexes()[0]
                .data(role=Qt.ItemDataRole.UserRole)
                .is_task
            ):
                # if a task is selected, add the new task to the same parent

                if self.tree_tasks.selectedIndexes()[0].parent().data():
                    parents: list[str] = [
                        self.tree_tasks.selectedIndexes()[0].parent().data()
                    ]
                    parent = self.tree_tasks.selectedIndexes()[0].parent().parent()
                    while parent.data():
                        parents.append(parent.data())
                        parent = parent.parent()
                else:
                    parents: list[str] = []

            else:
                # if a task is not selected, add the new task to the selected folder

                parents: list[str] = [self.tree_tasks.selectedIndexes()[0].data()]
                parent = self.tree_tasks.selectedIndexes()[0].parent()
                while parent.data():
                    parents.append(parent.data())
                    parent = parent.parent()

        project_path: str = self._lamp.current_project.project_path

        if task_name:
            result: bool | Exception = self._lamp.add_task(
                project_path, task_name, parents
            )
            if isinstance(result, Exception):
                display_error(str(result))
            else:
                display_info(f"Task {task_name} created successfully")
                self.tree_tasks.setModel(
                    make_task_tree(self._lamp.find_tasks(self._lamp.current_project))
                )
        else:
            display_error("Task name cannot be empty")

    def _btn_del_task(self) -> None:
        """Delete a task or folder"""
        pass

    def _btn_output(self) -> None:
        """Open the output window"""
        pass

    def _btn_add_workfile(self) -> None:
        """Add a workfile"""
        pass

    def _btn_add_existing_workfile(self) -> None:
        """Add an existing workfile"""
        pass
