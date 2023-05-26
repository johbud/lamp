from typing import Any

from PyQt6.QtCore import QAbstractItemModel, QAbstractListModel, Qt
from PyQt6.QtGui import QStandardItem, QStandardItemModel


class ProjectListModel(QAbstractListModel):
    """Model for the project list"""

    def __init__(self, projects: list[str]) -> None:
        super().__init__()
        self._projects = projects

    def data(self, index, role) -> str:
        if role == Qt.ItemDataRole.DisplayRole:
            return self._projects[index.row()]

    def rowCount(self, index) -> int:
        return len(self._projects)

    def itemFromIndex(self, index) -> str:
        return self._projects[index.row()]


class TaskTreeItem(QStandardItem):
    """Item for the task tree"""

    def __init__(self, name: str, children: list[Any]) -> None:
        super().__init__(name)
        for child in children:
            self.appendRow(TaskTreeItem(child["name"], child["children"]))


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


def make_task_tree(task_items: list[Any]) -> QStandardItemModel:
    """Make the task tree"""
    model = QStandardItemModel()
    root_node = model.invisibleRootItem()
    for item in task_items:
        root_node.appendRow(TaskTreeItem(item["name"], item["children"]))
    return model
