import logging

from source.Config.config import Config


class BadConfig(BaseException):

    def __init__(self, t1=None, t2=None):
        super.__init__(t1, t2)


class ParseConfig(object):

    @staticmethod
    def parse() -> Config:

        data = {}
        with open('/etc/httpd.conf') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                pair = line.split()
                key: str = pair[0]
                value: str = pair[1]
                data.update({
                    key: value
                })

        listen = 80 if data.get('listen') is None else int(data['listen'])
        cpu_limit = 1 if data.get('cpu_limit') is None else int(data['cpu_limit'])
        thread_limit = 8 if data.get('thread_limit') is None else int(data['thread_limit'])
        document_root = "/var/www/html" if data.get('document_root') is None else data['document_root']

        return Config(port=listen, cpu_count=cpu_limit, threads=thread_limit, root_dir=document_root)
