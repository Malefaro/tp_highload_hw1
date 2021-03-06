from server.StatusLine import StatusLine
from server.Header import *


class Response(object):

    def __init__(self, status_line: StatusLine, headers: Header, message: bytes = None, content_length: int = None):

        self._status_line = status_line
        self._headers = headers
        self._content_length = 0 if content_length is None else content_length
        self._message = b"" if message is None else message

    @property
    def status_line(self) -> StatusLine:
        return self._status_line

    @property
    def headers(self) -> Header:
        return self._headers

    @property
    def message(self) -> bytes:
        return self._message

    @property
    def content_length(self):
        return self._content_length

    def answer(self) -> bytes:
        status_line: StatusLine = self.status_line
        headers: Header = self.headers
        message: bytes = self.message
        headers.content_length = self.content_length
        data = status_line.get_status_line() + headers.get_headers() + b"\r\n"
        data += message

        return data


