import os
import sys

from config import Config


class Lamp:
    """The main class of the application"""

    def add_folder(self, folder_name: str) -> bool:
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

    def find_tasks(self, project_path: str) -> list[str]:
        """Find tasks in the project"""

        work_path = os.path.join(project_path, Config.task_folder_name)
        folders = os.listdir(work_path)
        tasks: list[str] = []

        for folder in folders:
            if os.path.isdir(os.path.join(work_path, folder)):
                contents = os.listdir(os.path.join(work_path, folder))
                if set(Config.task_subfolders).issubset(contents):
                    tasks.append(folder)
        return tasks


class PathManager:
    """Class for managing paths"""

    def get_work_folder(self, project_path: str) -> str:
        """Return the path to the work folder"""
        return os.path.join(project_path, Config.task_folder_name)
