import flet as ft

class StorageManager:
    def __init__(self, page: ft.Page):
        self.page = page
    
    def check_storage(self, e):
        storage = self.page.client_storage.get("key")

        if storage:
            self.load_storage(storage)
        else:
            return None

    def load_storage(self, storage):
        # Implement the logic to load storage here
        pass