import flet as ft
from todo_app import Task

class StorageManager:
    def __init__(self, page: ft.Page):
        self.page = page
    
    def check_storage(self):
        storage = self.page.client_storage.get("tasks")

        if storage:
            self.load_storage(storage)
        else:
            return None

    def load_storage(self, storage):
        tasks = storage

        for task_data in tasks:
            task_name, task_completed = task_data
            task = Task(task_name, self.page.task_status_change, self.page.task_delete)
            task.completed = task_completed
            task.display_task.value = task_completed
            self.page.tasks.controls.append(task)

        self.page.update()

    def save_storage(self):
        tasks = []
        for task in self.page.tasks.controls:
            tasks.append((task.task_name, task.completed))
        self.page.client_storage.set("tasks", tasks)