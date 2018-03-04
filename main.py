import asyncio
from server.http_parser import *
from source.Config.parse_config import ParseConfig
import os

from source.Config.src_parse_config import SrcParseConfig

forks = []


async def main(conf, loop):
    parser = Parser(conf)

    await asyncio.start_server(client_connected_cb=parser.parse,
                               host="0.0.0.0",
                               port=conf.port,
                               loop=loop,
                               reuse_port=True)


if __name__ == '__main__':

    conf = ParseConfig.parse()
    # conf = SrcParseConfig.parse()

    for x in range(0, int(conf.cpu_count)*2):
        process_id = os.fork()
        forks.append(process_id)
        if process_id == 0:
            ioloop = asyncio.get_event_loop()
            print('PID:', os.getpid())

            for i in range(0, int(conf.threads)):
                ioloop.create_task(main(conf=conf, loop=ioloop))

            ioloop.run_forever()

    for process_id in forks:
        os.waitpid(process_id, 0)
