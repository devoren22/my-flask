from lib.router import AppRouter


class Blueprint(AppRouter):
    def __init__(self, base_path: str):
        super().__init__()
        self.base_path = AppRouter._fix_path(base_path)
