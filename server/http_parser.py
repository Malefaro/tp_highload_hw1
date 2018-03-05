import logging

import aiofiles as aiofiles

from source.Config.config import Config
from asyncio import StreamReader, StreamWriter, sleep, AbstractEventLoop
from server.Response import *
import urllib.request
from os.path import getsize

types = {
    "js": "application/javascript",
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "html": "text/html",
    "png": "image/png",
    "gif": "image/gif",
    "css": "text/css",
    "txt": "text/plain",
    "swf": "application/x-shockwave-flash",
    "plain": "text/plain"
}

logging.basicConfig(level=logging.ERROR)


class Parser(object):

    def __init__(self, config: Config):
        self._config = config

    @property
    def config(self) -> Config:
        return self._config

    async def parse(self, reader: StreamReader, writer: StreamWriter):
        data = b""

        while not b"\r\n" in data:
            # read data wile does not get first line
            tmp = await reader.read(1024)
            # if empty data
            if not tmp:
                break
            else:
                data += tmp

        # if data is empty
        if not data:
            return

        request = data.decode("utf-8")
        request = request.split("\r\n", 1)[0]
        logging.debug(request.split(" ", 2))
        if len(request.split(" ", 2)) < 3:
            answer = send_error(status_code=404)
            writer.write(answer)
            await writer.drain()

        else:
            method, address, protocol = request.split(" ", 2)
            if method in ("GET", "HEAD"):
                answer = await send_file(address, method, self._config.root_dir)
                writer.write(answer)
                await writer.drain()

            else:
                answer = send_error(status_code=405)
                writer.write(answer)
                await writer.drain()
            writer.close()


def send_error(status_code):
    headers = Header()
    status_line = StatusLine(status_code)
    response = Response(status_line, headers)
    return response.answer()


def send_answer(status_code, data_size, type, data):
    headers = Header(content_length=data_size, content_type=type)
    status_line = StatusLine(status_code)
    response = Response(status_line, headers, data, content_length=data_size)
    return response.answer()


async def read_file(file) -> bytes:
    async with aiofiles.open(file, mode='rb') as f:
        return await f.read()


async def send_file(addr, method, root_dir):
    logging.debug(f"[send_file] ...")
    file_addr = urllib.request.unquote(addr)
    file_addr = file_addr.split("?")[0]
    logging.debug(f"[send_file] try (root_dir or '.') + file_addr")
    file_addr = (root_dir or '.') + file_addr
    logging.debug(f"[send_file] try splitext(file_addr)[1]")
    logging.debug(f"[senf_file] file_addr: {file_addr}")

    path = file_addr
    file_path = file_addr

    if file_path[-1:] == '/':
        file_path += 'index.html'

    try:
        filetype = file_path.split('.')[-1]
    except BaseException:
        filetype = 'plain'

    # filetype = splitext(file_addr)[1]
    if len(file_path.split('../')) > 1:
        return send_error(404)
    else:
        try:
            data = None
            status = 200
            type = types[filetype]
            all_data = getsize(file_path)

            if method != "HEAD":
                data = await read_file(file_path)
                answer = send_answer(status_code=status, data_size=all_data, type=type, data=data)
            else:
                answer = send_answer(status_code=status, data_size=all_data, type=type, data=b'')

            return answer

        except FileNotFoundError:
            if "index.html" in file_path:
                return send_error(403)
            else:
                return send_error(404)
        except IOError:
            return send_error(404)
        except NotADirectoryError:
            if path[-1:] == '/':
                file_path += "index.html"
            else:
                file_path += "/index.html"
            send_file(file_addr,  method, root_dir)






