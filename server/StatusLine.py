status = {
    200: "OK",
    403: "Forbidden",
    404: "Not Found",
    500: "Internal Server Error"
}

HTTP_VERSION = "HTTP/1.1"


class StatusLine(object):
    def __init__(self, status_code: int = 404):

        self._http_version = HTTP_VERSION
        self._status_code = status_code
        self._reason_phrase = status[status_code]

    @property
    def http_version(self) -> str:
        return self._http_version

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def reason_phrese(self) -> str:
        return self._reason_phrase

    @classmethod
    def get_status_line(cls) -> str:
        status_line = cls.http_version + " " + str(cls.status_code) + " " + cls.reason_phrese + "\r\n"
        return status_line.encode("utf-8")
