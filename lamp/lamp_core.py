import logging
import os
import platform
from typing import Any

from config import Config
from lamp_types import Folder, Project, Task, WorkFile
from showinfm import show_in_file_manager  # type: ignore


class Lamp:
    """The main class of the application"""

    def __init__(self) -> None:
        self.current_project: Project = self.find_projects()[0]
        self.current_task = None
        self.current_tasks_list: list[Task] = []
        if platform.system() == "Windows":
            Config.work_drive = Config.work_drive_win
        elif platform.system() == "Darwin":
            Config.work_drive = Config.work_drive_mac
        else:
            Config.work_drive = Config.work_drive_mac

    def find_projects(self) -> list[Project]:
        """Find projects"""

        listing: list[str] = os.listdir(path=Config.work_drive)
        projects: list[Project] = []

        for item in listing:
            if item.split("_")[0].isnumeric() is False:
                continue
            if item.split("_")[1].isnumeric() is False:
                continue
            if os.path.isdir(os.path.join(Config.work_drive, item)):
                if os.path.exists(os.path.join(Config.work_drive, item, "00_pipeline")):
                    project = Project(item)
                    projects.append(project)
        return projects

    def create_project(self, project_name: str) -> bool | Exception:
        """Create a new project"""

        if os.path.exists(os.path.join(Config.work_drive, project_name)):
            return Exception("Project already exists")

        try:
            os.mkdir(os.path.join(Config.work_drive, project_name))
            os.mkdir(
                os.path.join(Config.work_drive, project_name, Config.work_folder_name)
            )
            os.mkdir(
                os.path.join(
                    Config.work_drive, project_name, Config.dailies_folder_name
                )
            )
            os.mkdir(
                os.path.join(
                    Config.work_drive, project_name, Config.pipeline_folder_name
                )
            )
        except Exception as e:
            return e

        return True

    def add_folder(
        self, project_path: str, folder_name: str, parents: list[str]
    ) -> bool | Exception:
        """Add a folder in the project"""

        work_path: str = os.path.join(project_path, Config.work_folder_name)
        folder_path: str = work_path

        print(f"work_path: {work_path}")
        print(f"task_path: {folder_path}")
        print(f"task_name: {folder_name}")
        print(f"parents: {parents}")

        for parent in parents:
            folder_path = os.path.join(folder_path, parent)
        folder_path = os.path.join(folder_path, folder_name)

        if os.path.exists(folder_path):
            return Exception("Folder already exists")
        os.mkdir(folder_path)

        return True

    def add_task(
        self, project_path: str, task_name: str, parents: list[str] | None = None
    ) -> bool | Exception:
        """Add a task in the project"""

        work_path: str = os.path.join(project_path, Config.work_folder_name)
        task_path: str = work_path

        print(f"work_path: {work_path}")
        print(f"task_path: {task_path}")
        print(f"task_name: {task_name}")
        print(f"parents: {parents}")

        if parents is not None:
            for parent in parents:
                task_path = os.path.join(task_path, parent)
        task_path = os.path.join(task_path, task_name)

        if os.path.exists(task_path):
            return Exception("Task already exists")
        os.mkdir(task_path)
        for subfolder in Config.task_subfolders:
            os.mkdir(os.path.join(task_path, subfolder))

        return True

    def find_tasks(self, project: Project) -> list[Folder]:
        """Find tasks in the project"""
        work_path: str = os.path.join(
            Config.work_drive, project.project_name, Config.work_folder_name
        )
        return self._iterate_children(work_path)

    def _iterate_children(self, path: str) -> list[Any]:
        """Iterate through children"""
        children: list[Any] = []
        contents: list[str] = os.listdir(path)
        for item in contents:
            if os.path.isdir(os.path.join(path, item)):
                if set(Config.task_subfolders).issubset(
                    os.listdir(os.path.join(path, item))
                ):
                    children.append(Folder(item, True, []))
                else:
                    children.append(
                        Folder(
                            item,
                            False,
                            self._iterate_children(os.path.join(path, item)),
                        )
                    )
        return children

    def find_work_files(self, path: str) -> list[WorkFile]:
        """Find work files in the path"""
        work_files: list[WorkFile] = []
        contents: list[str] = os.listdir(path)
        for item in contents:
            if os.path.isfile(os.path.join(path, item)):
                if item.split(".")[-1] in Config.work_file_extensions:
                    work_files.append(WorkFile(path, filename=item))
        return work_files

    def set_current_project(self, project: Project) -> None:
        """Set current project"""
        self.current_project = project

    def open_dailies(self) -> None:
        """Open dailies"""
        show_in_file_manager(
            os.path.join(
                Config.work_drive,
                self.current_project.project_name,
                Config.dailies_folder_name,
            )
        )
