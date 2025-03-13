import flet as ft
from flet.auth.providers import GitHubOAuthProvider
from todo_app import TodoApp

GITHUB_CLIENT_ID = "Ov23li2P801NaRcFR1GL"
GITHUB_CLIENT_SECRET = "f38a7badcb64804d64a814bb6a5ecf2ce7c40ef4"

def build_view(route: str, page: ft.Page):
    if route == "/":
        # Cria a view de login usando GitHub OAuth
        provider = GitHubOAuthProvider(
            client_id=GITHUB_CLIENT_ID,
            client_secret=GITHUB_CLIENT_SECRET,
            redirect_url="http://localhost:8550/oauth_callback",
        )

        def login_click(e):
            page.login(provider)

        login_button = ft.ElevatedButton("Login with GitHub", on_click=login_click)
        
        return ft.View(
            route="/",
            controls=[login_button],
        )
    
    elif route == "/todo":
        todo_app = TodoApp(page)
        page.controls.append(todo_app)
        return ft.View(
            route="/todo",
            controls=[
                todo_app,
            ],
        )

def main(page: ft.Page):
    # Função que é chamada após o login (on_login é acionado pelo próprio Flet)
    def on_login(e: ft.LoginEvent):
        if e.error:
            # Caso haja erro no login
            print("Login error:", e.error)
            page.views.clear()
            page.views.append(build_view("/", page))
        else:
            print("Access token:", page.auth.token.access_token)
            print("User ID:", page.auth.user.id)
            # Se o login for bem-sucedido, mudamos a rota para a view principal
            page.route = "/todo"
            page.views.clear()
            page.views.append(build_view(page.route, page))
        page.update()

    page.on_login = on_login

    page.title = "ToDo App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    # Define a rota inicial e constrói a view inicial (login)
    page.route = "/"
    page.views.append(build_view(page.route, page))
    page.update()

if __name__ == "__main__":
    ft.app(target=main, port=8550, view=ft.WEB_BROWSER, assets_dir="assets")
