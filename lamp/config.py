class Config:
    """Configuration class"""

    work_drive_win: str = "D:\\Dropbox (Personal)\\Annat\\Kod\\lamp\\test_folder"
    work_drive_mac: str = (
        "/Users/johnbuddee/Dropbox (Personal)/Annat/Kod/lamp/test_folder"
    )
    work_drive: str = work_drive_win
    pipeline_folder_name: str = "00_pipeline"
    work_folder_name: str = "02_work"
    task_subfolders: list[str] = ["01_work", "02_output"]
    dailies_folder_name: str = "03_dailies"
    work_file_extensions: list[str] = [".blend", ".nk", ".aep"]
