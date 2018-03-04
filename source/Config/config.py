class Config(object):

    def __init__(self, port=80, cpu_count=2,
                 threads=256, root_dir='/var/www/html'):

        self._threads = threads
        self._port = port
        self._cpu_count = cpu_count
        self._root_dir = root_dir

    @property
    def threads(self) -> int:
        return self._threads

    @property
    def port(self) -> int:
        return self._port

    @property
    def cpu_count(self):
        return self._cpu_count

    @property
    def root_dir(self):
        return self._root_dir
