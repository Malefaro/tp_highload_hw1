import locale, datetime


class Header(object):

    def __init__(self, server: str = "custorm_server", connection: str = "keep-alive",
                 date: str = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
                 content_length: int = 0, content_type: str = ""):

        # locale.setlocale(locale.LC_TIME, 'en_US')
        self._date = date
        self._server = server
        self._connection = connection
        self._content_length = content_length
        self._content_type = content_type

    @property
    def date(self) -> str:
        return self._date

    @property
    def server(self) -> str:
        return self._server

    @property
    def connection(self) -> str:
        return self._connection

    @property
    def content_length(self) -> int:
        return self._content_length

    @property
    def content_type(self) -> str:
        return self._content_type

    @content_length.setter
    def content_length(self, length):
        self._content_length = length

    @classmethod
    def get_headers(cls) -> bytes:
        date = "Date: " + cls.date + "\r\n"
        server = "Server: " + cls.server + "\r\n"
        connection = "Connection: " + cls.connection + "\r\n"
        content_type = "Content-Type: " + cls.content_type + "\r\n"
        content_length = "Content-Length: " + str(cls.content_length) + "\r\n"
        answer = date + server + connection + content_type + content_length
        return answer.encode("utf-8")
