import os
from dataclasses import dataclass
from typing import Any

from config import Config


class WorkFile:
    """Class for managing work files"""

    def __init__(
        self,
        path: str,
        filename: str | None = None,
        project_name: str | None = None,
        task_name: str | None = None,
        comment: str | None = None,
        version: int | None = None,
        extension: str | None = None,
    ) -> None:
        if filename is not None:
            self._parse_filename(filename)
        elif (
            project_name is not None
            and task_name is not None
            and comment is not None
            and version is not None
            and extension is not None
        ):
            self.project_name: str = project_name
            self.task_name: str = task_name
            self.comment: str = comment
            self.version: int = version
        else:
            raise ValueError("Invalid arguments")

        self.path: str = path
        self.full_name: str = f"{self.project_name}_{self.task_name}_{self.comment}_{self.version}.{extension}"
        self.full_path: str = os.path.join(self.path, self.full_name)

    def get_table_row(self) -> list[str]:
        """Return a list of strings for the table"""
        return [
            self.project_name,
            self.task_name,
            self.comment,
            str(self.version),
            self.extension,
        ]

    def _parse_filename(self, filename: str) -> None:
        filename_split: list[str] = filename.split("_")
        self.project_name = (
            filename_split[0] + "_" + filename_split[1] + "_" + filename_split[2]
        )
        self.task_name = filename_split[3]
        self.comment = filename_split[4]
        self.version = int(filename_split[5][:3])
        self.extension: str = os.path.splitext(filename)[1]

    def get_full_name(self) -> str:
        """Return the full name of the work file"""
        return self.full_name

    def get_full_path(self) -> str:
        """Return the full path of the work file"""
        return self.full_path


@dataclass
class Folder:
    """Class for managing folders"""

    name: str
    is_task: bool
    children: list[Any]


class Task:
    """Class for managing tasks"""

    def __init__(self, project_path: str, task_name: str, parents: list[str]) -> None:
        self.project_path: str = project_path
        self.task_name: str = task_name
        self.parents: list[str] = parents
        self.task_path: str = self.project_path
        for parent in self.parents:
            self.task_path = os.path.join(self.task_path, parent)
        self.task_path = os.path.join(self.task_path, self.task_name)

    def get_task_path(self) -> str:
        """Return the path to the task"""
        return self.task_path

    def get_work_path(self) -> str:
        """Return the path to the work folder"""
        return os.path.join(self.task_path, Config.task_subfolders[0])

    def get_output_path(self) -> str:
        """Return the path to the output folder"""
        return os.path.join(self.task_path, Config.task_subfolders[1])


class Project:
    """Class for managing projects"""

    def __init__(self, project_name: str) -> None:
        self.project_name: str = project_name
        self.project_path: str = os.path.join(Config.work_drive, self.project_name)

    def get_project_path(self) -> str:
        """Return the path to the project"""
        return self.project_path

    def get_dailies_path(self) -> str:
        """Return the path to the dailies folder"""
        return os.path.join(
            Config.work_drive, self.project_name, Config.dailies_folder_name
        )
