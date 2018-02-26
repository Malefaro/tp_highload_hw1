import asyncio
from socket import *
from server.http_parser import *
from concurrent.futures import ThreadPoolExecutor
import logging
import sys
import os

CONFIG = {
    "BUFFER": 1024,
    "HOST": "127.0.0.1",
    "PORT": 3000,
    "WORKERS": 2,
    "CPU": 2,
}

forks = []


async def main(server_sock, pid, loop):
    e = ThreadPoolExecutor()
    while True:
        print('waiting for connection... listening on port')
        conn, addr = await loop.sock_accept(server_sock)
        try:
            loop.create_task(parse(conn, addr, pid, "/", loop, e))
        except Exception:
            conn.close()


if __name__ == '__main__':
    # Configure logging to show the name of the thread

    logging.basicConfig(
        level=logging.INFO,
        format='%(threadName)10s %(name)18s: %(message)s',
        stream=sys.stderr,
    )

    ROOT_DIR = ""
    ADDR = (CONFIG["HOST"], CONFIG["PORT"])

    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(ADDR)
    # number of connections in the queue
    sock.listen(10)

    for x in range(0, CONFIG["WORKERS"] * CONFIG["CPU"]):
        process_id = os.fork()
        forks.append(process_id)
        if process_id == 0:
            ioloop = asyncio.get_event_loop()
            print('PID:', os.getpid())
            ioloop.create_task(main(sock, process_id, ioloop))
            ioloop.run_forever()
            ioloop.close()

    for process_id in forks:
        os.waitpid(process_id, 0)
