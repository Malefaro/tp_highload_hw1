from source.Config.config import Config


class SrcParseConfig(object):

    @staticmethod
    def parse() -> Config:

        port = 8081
        cpu_count = 4
        threads = 256
        root_dir = '/home/anton/dev/tp/highload/pavel/tp_highload_hw1/http-test-suite/httptest'

        return Config(port=port, cpu_count=cpu_count, threads=threads, root_dir=root_dir)
