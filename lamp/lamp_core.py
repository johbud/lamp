import os
from typing import Any

from config import Config


class Lamp:
    """The main class of the application"""

    def __init__(self) -> None:
        self.current_project: str = self.find_projects()[0]
        self.current_task = None

    def find_projects(self) -> list[str]:
        """Find projects"""

        listing = os.listdir(Config.work_drive)
        projects: list[str] = []

        for item in listing:
            if item.split("_")[0].isnumeric() is False:
                continue
            if item.split("_")[1].isnumeric() is False:
                continue
            if os.path.isdir(os.path.join(Config.work_drive, item)):
                if os.path.exists(os.path.join(Config.work_drive, item, "00_pipeline")):
                    projects.append(item)
        return projects

    def add_folder(self) -> bool:
        """Add a folder in the project"""
        return True

    def add_task(self, project_path: str, task_name: str) -> bool:
        """Add a task in the project"""
        work_path = os.path.join(project_path, Config.task_folder_name)
        task_path = os.path.join(work_path, task_name)
        if os.path.exists(task_path):
            return False
        os.mkdir(task_path)
        for subfolder in Config.task_subfolders:
            os.mkdir(os.path.join(task_path, subfolder))
        return True

    def find_tasks(self, project: str) -> list[str]:
        """Find tasks in the project"""
        work_path = os.path.join(Config.work_drive, project, Config.task_folder_name)
        return self._iterate_children(work_path)

    def _iterate_children(self, path: str) -> list[Any]:
        """Iterate through children"""
        children: list[Any] = []
        contents = os.listdir(path)
        for item in contents:
            if os.path.isdir(os.path.join(path, item)):
                if set(Config.task_subfolders).issubset(
                    os.listdir(os.path.join(path, item))
                ):
                    children.append({"name": item, "children": []})
                else:
                    children.append(
                        {
                            "name": item,
                            "children": self._iterate_children(
                                os.path.join(path, item)
                            ),
                        }
                    )
        return children


class PathManager:
    """Class for managing paths"""

    def get_work_folder(self, project_path: str) -> str:
        """Return the path to the work folder"""
        return os.path.join(project_path, Config.task_folder_name)
