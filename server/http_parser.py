from server.StatusLine import *
from server.Header import *
from server.Response import *
import urllib.request
from os.path import splitext, getsize

types = {
    ".js": "application/javascript",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".html": "text/html",
    ".png": "image/png",
    ".gif": "image/gif",
    ".css": "text/css",
    ".txt": "text/plain",
    ".swf": "application/x-shockwave-flash",
}


async def send_error(conn, status_code, loop):
    headers = Header()
    status_line = StatusLine(status_code)
    response = Response(status_line, headers, status_line.reason_phrese, conn, loop)
    await response.answer()


async def send_answer(conn, status_code, all_data, loop):
    headers = Header(content_length=all_data)
    status_line = StatusLine(status_code)
    response = Response(status_line, headers, status_line.reason_phrese, conn, loop)
    await response.answer()


async def read_file(file, loop, executor):
    with open(file, "rb") as f:
        data = await loop.run_in_executor(executor, f.read)
        return data


async def send_file(conn, addr, method, root_dir, loop, executor):
    file_addr = urllib.request.unquote(addr)
    file_addr = file_addr.split("?")[0]
    file_addr = (root_dir or '.') + file_addr
    filetype = splitext(file_addr)[1]
    if '..' in file_addr:
        send_error(conn, 404, loop)
    else:
        try:
            data = await read_file(file_addr, loop, executor)
            status = 200
            type = types[filetype]
            all_data = getsize(file_addr)
            send_answer(conn, status, all_data, type)
            if method != "HEAD":
                await loop.sock_sendall(conn, data)
            conn.close()
        except FileNotFoundError:
            if "index.html" in file_addr:
                send_error(conn, 403, loop)
            else:
                send_error(conn, 404, loop)
        except IsADirectoryError:
            if addr[-1] == '/':
                addr += "index.html"
            else:
                addr += "/index.html"
            send_file(conn, addr, method, root_dir, loop, executor)


async def parse(conn, addr, pid, ROOT_DIR, loop, executor):
    data = b""

    while not b"\r\n" in data:
        # read data wile does not get first line
        tmp = await loop.sock_recv(conn, 1024)
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
    print(request.split(" ", 2))
    if len(request.split(" ", 2)) < 3:
        send_error(conn=conn, status_code=404, loop=loop)
    else:
        method, address, protocol = request.split(" ", 2)
        if method in ("GET", "HEAD"):
            await send_file(conn, address, method, ROOT_DIR, loop, executor)
        else:
            await send_error(conn=conn, status_code=405, loop=loop)
