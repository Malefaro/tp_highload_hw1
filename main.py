import asyncio
import logging
import sys
import os

CONFIG = {
    "BUFFER": 1024,
    "HOST": "127.0.0.1",
    "PORT": 80,
    "WORKERS": 4,
    "CPU": 4,
}

forks = []


def accept_client():
    return 3.14


async def main(process_id, path):
    loop = asyncio.get_event_loop()
    f = asyncio.start_server(accept_client, host="localhost", port=3000)
    loop.run_until_complete(f)
    loop.run_forever()



if __name__ == '__main__':
    # Configure logging to show the name of the thread

    logging.basicConfig(
        level=logging.INFO,
        format='%(threadName)10s %(name)18s: %(message)s',
        stream=sys.stderr,
    )

    ROOT_DIR = ""

    for x in range(0, CONFIG["WORKERS"] * CONFIG["CPU"]):
        process_id = os.fork()
        forks.append(process_id)
        if process_id == 0:
            print('PID:', os.getpid())
            main(os.getpid(), ROOT_DIR)

    for process_id in forks:
        os.waitpid(process_id, 0)