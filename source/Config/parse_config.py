import logging

from source.Config.config import Config


class BadConfig(BaseException):

    def __init__(self, t1=None, t2=None):
        super.__init__(t1, t2)


class ParseConfig(object):

    @staticmethod
    def parse() -> Config:
        conf = {}

        try:
            # file = open('/etc/http.conf')
            file = open('/home/oem/projects/tp/sem3/highload/tp_highload_hw1/httpd.conf')
            for line in file:
                line.strip()
                pair = line.split()
                if len(pair) != 2:
                    raise BadConfig("number of params must equal two")

                conf.update({
                    pair[0]: pair[1]
                })

        except BadConfig as err:
            logging.error(err)

        return Config(port=conf.get('listen'), cpu_count=conf.get('cpu_limit'),
                      threads=conf.get('thread_limit'), root_dir=conf.get('document_root'))
