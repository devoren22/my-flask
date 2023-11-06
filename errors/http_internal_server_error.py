from http import HTTPStatus

class HttpInternalServerError(Exception):
    def __init__(self):
        super().__init__()
        self.message = "Internal server error"
        self.status = 500