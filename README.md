# ToDo App

Este é um aplicativo de gerenciamento de tarefas desenvolvido com [Flet](https://flet.dev/). O aplicativo permite que os usuários adicionem, editem, excluam e filtrem tarefas. Além disso, ele utiliza autenticação via GitHub OAuth para gerenciar tarefas específicas do usuário.

## Funcionalidades

- Adicionar novas tarefas
- Editar tarefas existentes
- Marcar tarefas como concluídas
- Excluir tarefas
- Filtrar tarefas por status (todas, ativas, concluídas)
- Autenticação via GitHub OAuth
- Armazenamento seguro das tarefas utilizando criptografia

## Instalação

1. Clone o repositório:
    ```sh
    git clone <URL_DO_REPOSITORIO>
    cd TODO
    ```

2. Crie um ambiente virtual e ative-o:
    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

## Configuração

1. Crie um aplicativo OAuth no GitHub e obtenha o `Client ID` e `Client Secret`.

2. Atualize as variáveis `GITHUB_CLIENT_ID` e `GITHUB_CLIENT_SECRET` no arquivo `main.py` com os valores obtidos.

## Execução

Para iniciar o aplicativo, execute o seguinte comando:
```sh
python main.py
```

O aplicativo estará disponível em `http://localhost:8550`.