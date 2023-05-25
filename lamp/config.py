import os


class Config:
    """Configuration class"""

    work_drive = "G:"
    task_folder_name = "02_work"
    task_subfolders = ["01_work", "02_output"]
    test_project_path_win = "D:\\Dropbox (Personal)\\Annat\\Kod\\lamp\\test_project"
    project_path: str
    if os.name == "nt":
        project_path = test_project_path_win
    else:
        project_path = ""
