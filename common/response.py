import json
from typing import Dict


class Response:
    def __init__(self, status):
        self.status_code = status
        self.data = {}
    def status(self, new_status):
        self.status_code = new_status
        return self

    def send(self, data):
        if isinstance(data, Dict):
            self.data = json.dumps(data)
        else:
            self.data = str(data)

        return self
