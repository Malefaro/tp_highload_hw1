import asyncio
import functools
from socket import *
from server.http_parser import *
from concurrent.futures import ThreadPoolExecutor
from source.Config.parse_config import ParseConfig
import logging
import sys
import os

from source.Config.src_parse_config import SrcParseConfig

CONFIG = {
    "BUFFER": 1024,
    "HOST": "127.0.0.1",
    "PORT": 3000,
    "WORKERS": 2,
    "CPU": 2,
}

forks = []


async def main(conf, loop):
    parser = Parser(conf)

    await asyncio.start_server(client_connected_cb=parser.parse,
                               host="localhost",
                               port=conf.port,
                               loop=loop,
                               reuse_port=True)


if __name__ == '__main__':

    # conf = ParseConfig.parse()
    conf = SrcParseConfig.parse()

    ROOT_DIR = ""
    ADDR = (CONFIG["HOST"], int(conf.port))

    for x in range(0, CONFIG["WORKERS"] * CONFIG["CPU"]):
        process_id = os.fork()
        forks.append(process_id)
        if process_id == 0:
            ioloop = asyncio.get_event_loop()
            print('PID:', os.getpid())

            for i in range(0, 10):
                ioloop.create_task(main(conf=conf, loop=ioloop))

            ioloop.run_forever()

    for process_id in forks:
        os.waitpid(process_id, 0)
