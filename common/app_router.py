

class AppRouter:
    def __init__(self):
        self.routes = {}
        self.base_path = ""


    def get(self, path: str):
        path = self.base_path + AppRouter._fix_path(path)
        def wrapper(func):
            self.routes[path] = { 'method': "GET", 'handler': func, 'status': 200 }

        return wrapper

    def post(self, path: str):
        path = self.base_path + AppRouter._fix_path(path)

        def wrapper(func):
            self.routes[path] = { 'method': "POST", 'handler': func, 'status': 201 }

        return wrapper

    @staticmethod
    def _fix_path(path):
        if not path.startswith("/"):
            path = f'/{path}'

        return path