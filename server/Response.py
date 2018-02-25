from server.StatusLine import *
from server.Header import *

class Response(object):

    def __init__(self, status_line: StatusLine, headers: Header, message: str, connection):

        self._status_line = status_line
        self._headers = headers
        self._message = message
        self._connection = connection

    @property
    def status_line(self) -> StatusLine:
        return self.status_line

    @property
    def headers(self) -> Header:
        return self.headers

    @property
    def message(self) -> str:
        return self.message

    @property
    def connection(self):
        return self._connection

    @classmethod
    def answer(cls):
        status_line: StatusLine = cls.status_line
        headers: Header = cls.headers
        message: str = cls.message
        headers.content_length = len(message)
        connection = cls.connection

        connection.send(status_line.get_status_line())
        connection.send(headers.get_headers())
        connection.send(b"\r\n")
        connection.send(message.encode("utf-8"))

