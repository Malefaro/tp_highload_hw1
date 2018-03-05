from source.Config.config import Config


class SrcParseConfig(object):

    @staticmethod
    def parse() -> Config:

        port = 80
        cpu_count = 4
        threads = 256
        root_dir = '/var/www/html'

        return Config(port=port, cpu_count=cpu_count, threads=threads, root_dir=root_dir)
