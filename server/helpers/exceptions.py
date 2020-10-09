class HTTPException(Exception):
    title = 'Internal Server Error'
    code = 500

    def __init__(self, message='', title=None, code=None):
        Exception.__init__(self)
        self.message = message
        if code is not None:
            self.code = code
        if title is not None:
            self.title = title

    def to_dict(self):
        payload = {
            'code': self.code,
            'title': self.title
        }
        if self.message:
            payload['message'] = self.message

        return {'error': payload}


class HTTPBadRequest(HTTPException):
    code = 400
    title = 'Bad Request'


class HTTPNotFound(HTTPException):
    code = 404
    title = 'Not Found'
