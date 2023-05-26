from lamp_core import Lamp
from models import ProjectListModel, make_task_tree
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow


class LampBrowserWindow(QMainWindow):
    """The main browser window"""

    def __init__(self, lamp_instance: Lamp) -> None:
        super().__init__(parent=None)
        self._lamp = lamp_instance
        uic.loadUi("project_browser.ui", self)

        self.list_projects.setModel(ProjectListModel(self._lamp.find_projects()))

        self.tree_tasks.setModel(
            make_task_tree(self._lamp.find_tasks(self._lamp.current_project))
        )

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
        self._lamp.current_project = self.list_projects.model().itemFromIndex(
            self.list_projects.selectedIndexes()[0]
        )
        self.tree_tasks.setModel(
            make_task_tree(self._lamp.find_tasks(self._lamp.current_project))
        )

    def _btn_new_project(self) -> None:
        """Create a new project"""
        pass

    def _btn_dailies(self) -> None:
        """Open the dailies window"""
        pass

    def _btn_add_folder(self) -> None:
        """Add a folder"""
        pass

    def _btn_add_task(self) -> None:
        """Add a task"""
        pass

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
