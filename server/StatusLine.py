status = {
    200: "OK",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Internal Server Error"
}

HTTP_VERSION = "HTTP/1.1"


class StatusLine(object):
    def __init__(self, status_code: int = None):

        self._http_version = HTTP_VERSION
        self._status_code = 404 if status_code is None else status_code
        self._reason_phrase = status[self._status_code]

    @property
    def http_version(self) -> str:
        return self._http_version

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def reason_phrese(self) -> str:
        return self._reason_phrase

    def get_status_line(self) -> bytes:
        status_line = self.http_version + " " + str(self.status_code) + " " + self.reason_phrese + "\r\n"
        return status_line.encode("utf-8")
