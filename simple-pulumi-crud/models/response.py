import json


class APIResponse:
    def __init__(self, code, message, http_status_code, operation, body):
        self.code = code
        self.message = message
        self.http_status_code = http_status_code
        self.operation = operation
        self.body = body

    def return_JSON(self):
        return json.dumps(self.__dict__)
