class FrontendException(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code

    def present(self, **kwargs):
        return {
            'message': self.message,
            'code': self.code,
        }
