from typing import Any

from lamp_types import Folder, Project, WorkFile
from PyQt6.QtCore import QAbstractItemModel, QAbstractListModel, QAbstractTableModel, Qt
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QTreeWidgetItem


class ProjectListModel(QAbstractListModel):
    """Model for the project list"""

    def __init__(self, projects: list[Project]) -> None:
        super().__init__()
        self._projects: list[Project] = projects

    def data(self, index, role) -> str:
        if role == Qt.ItemDataRole.DisplayRole:
            return self._projects[index.row()].project_name

    def rowCount(self, index) -> int:
        return len(self._projects)

    def itemFromIndex(self, index) -> str:
        return self._projects[index.row()]


class TaskTreeItem(QStandardItem):
    """Item for the task tree"""

    def __init__(self, folder: Folder) -> None:
        super().__init__(folder.name)
        self.folder: Folder = folder
        self.name: str = folder.name
        self.is_task: bool = folder.is_task
        for child in folder.children:
            self.appendRow(TaskTreeItem(child))

    def data(self, role: int = 1) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return self.folder.name
        if role == Qt.ItemDataRole.UserRole:
            return self.folder


class TaskTreeModel(QAbstractItemModel):
    """Model for the task tree"""

    def __init__(self, task_items: list[Any]) -> None:
        super().__init__()
        self._task_items = task_items

    def data(self, index, role) -> str:
        if role == Qt.ItemDataRole.DisplayRole:
            return self._task_items[index.row()]

    def rowCount(self, index) -> int:
        return len(self._task_items)


class WorkfilesTableModel(QAbstractTableModel):
    """Model for the workfiles table"""

    def __init__(self, workfiles: list[WorkFile]) -> None:
        super().__init__()
        self._workfiles: list[list[str]] = []
        for workfile in workfiles:
            self._workfiles.append(workfile.get_table_row())

    def data(self, index, role) -> str:
        if role == Qt.ItemDataRole.DisplayRole:
            return self._workfiles[index.row()]

    def rowCount(self, index) -> int:
        return len(self._workfiles)

    def columnCount(self, index) -> int:
        return len(self._workfiles[0])


def make_task_tree(task_items: list[Any]) -> QStandardItemModel:
    """Make the task tree"""
    model = QStandardItemModel()
    root_node = model.invisibleRootItem()
    for item in task_items:
        root_node.appendRow(TaskTreeItem(item))
    return model
