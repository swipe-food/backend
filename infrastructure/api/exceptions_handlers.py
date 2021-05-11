from flask import request, jsonify


class ApiException(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code

    def handle(self):
        request.logger.error(self.message, code=self.code, exception=self.__class__.__name__)
        return jsonify(message=self.message), self.code


class ValidationException(Exception):
    def __init__(self, messages):
        self.messages = messages

    def handle(self):
        request.logger.error(self.messages, exception=self.__class__.__name__)
        return jsonify(messages=self.messages), 422
