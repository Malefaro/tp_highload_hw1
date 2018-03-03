from server.StatusLine import StatusLine
from server.Header import *

class Response(object):

    def __init__(self, status_line: StatusLine, headers: Header, message: str):

        self._status_line = status_line
        self._headers = headers
        self._message = message

    @property
    def status_line(self) -> StatusLine:
        return self._status_line

    @property
    def headers(self) -> Header:
        return self._headers

    @property
    def message(self) -> str:
        return self._message


    def answer(self) -> bytes:
        status_line: StatusLine = self.status_line
        headers: Header = self.headers
        message: str = self.message
        headers.content_length = len(message)
        data = status_line.get_status_line() + headers.get_headers() + b"\r\n" + message.encode("utf-8")

        return data


