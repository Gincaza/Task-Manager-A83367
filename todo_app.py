import flet as ft
from flet.security import encrypt, decrypt

SECRET_KEY = "radiopiao"

class Task(ft.Column):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete
        self.display_task = ft.Checkbox(
            value=False, label=self.task_name, on_change=self.status_changed
        )
        self.edit_name = ft.TextField(expand=1)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        self.controls = [self.display_view, self.edit_view]

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.task_status_change(self)  # Atualizar armazenamento
        self.update()

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change(self)

    def delete_clicked(self, e):
        self.task_delete(self)

class TodoApp(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.new_task = ft.TextField(
            hint_text="What needs to be done?", on_submit=self.add_clicked, expand=True
        )
        self.tasks = ft.Column()

        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="all"), ft.Tab(text="active"), ft.Tab(text="completed")],
        )

        self.items_left = ft.Text("0 items left")

        self.width = 600
        self.controls = [
            ft.Row(
                [ft.Text(value="Todos", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(
                        icon=ft.icons.ADD, on_click=self.add_clicked
                    ),
                ],
            ),
            ft.Column(
                spacing=25,
                controls=[
                    self.filter,
                    self.tasks,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.items_left,
                            ft.OutlinedButton(
                                text="Clear completed", on_click=self.clear_clicked
                            ),
                        ],
                    ),
                ],
            ),
        ]

        # Carregar tarefas ao iniciar
        self.check_storage()

    def check_storage(self):
        # Recupera o ID do usuário autenticado
        token = self.page.auth.user.id if self.page.auth and self.page.auth.user.id else None


        storage = self.page.client_storage.get("tasks") or {}
        user_tasks = storage.get(token, [])

        if user_tasks:
            self.load_storage(user_tasks)
        else:
            print("Nenhuma tarefa encontrada para este usuário.")

    def load_storage(self, storage):
        tasks = storage

        for task_data in tasks:
            task_name, task_status = decrypt(task_data['task_name'], SECRET_KEY), task_data['status']
            task = Task(task_name, self.task_status_change, self.task_delete)
            task.completed = task_status
            task.display_task.value = task_status
            self.tasks.controls.append(task)

        self.before_update()
        self.page.update()

    def save_storage(self):
        token = self.page.auth.user.id if self.page.auth and self.page.auth.user.id else None

        # Cria a lista de tarefas criptografadas do usuário atual
        tasks = []
        for task in self.tasks.controls:
            tasks.append({
                "task_name": encrypt(task.task_name, SECRET_KEY), 
                "status": task.completed,
            })

        # Recupera o dicionário existente e atualiza apenas o token atual
        storage = self.page.client_storage.get("tasks") or {}
        storage[token] = tasks
        self.page.client_storage.set("tasks", storage)

    def add_clicked(self, e):
        if self.new_task.value:
            task = Task(self.new_task.value, self.task_status_change, self.task_delete)
            self.tasks.controls.append(task)
            self.new_task.value = ""
            self.new_task.focus()
            self.before_update()
            self.update()
            self.save_storage()

    def task_status_change(self, task):
        self.before_update()
        self.update()
        self.save_storage()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.before_update()
        self.update()
        self.save_storage()

    def tabs_changed(self, e):
        self.before_update()
        self.update()

    def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.task_delete(task)
        self.save_storage()

    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and not task.completed)
                or (status == "completed" and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} active item(s) left"