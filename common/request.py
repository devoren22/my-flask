import json


class Request:
    def __init__(self):
        self.query = {}
        self.params = {}
        self.body = {}

    def __str__(self):
        return json.dumps({ 'query': self.query, 'params': self.params, 'body': self.body })
