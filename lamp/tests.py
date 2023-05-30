import unittest

from lamp_core import Lamp


class TestLamp(unittest.TestCase):
    """Test the Lamp class"""

    def test_find_projects(self) -> None:
        """Test the find_projects method"""
        lamp = Lamp()
        projects: list[str] = lamp.find_projects()
        self.assertEqual(projects, ["23_1234_testprojekt_A", "23_1234_testprojekt_B"])

    def test_find_tasks(self) -> None:
        """Test the find_tasks method"""
        lamp = Lamp()
        tasks: list[str] = lamp.find_tasks("23_1234_testprojekt_A")
        self.assertEqual(
            tasks,
            [
                {
                    "name": "folder_A",
                    "children": [
                        {"name": "task_A", "children": []},
                        {"name": "task_B", "children": []},
                    ],
                },
                {"name": "task_C", "children": []},
            ],
        )


if __name__ == "__main__":
    unittest.main()
