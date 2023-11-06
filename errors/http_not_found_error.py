from http import HTTPStatus

class HttpNotFoundError(Exception):
    def __init__(self):
        super().__init__()
        self.message = "Http not found"
        self.status = HTTPStatus.NOT_FOUND
