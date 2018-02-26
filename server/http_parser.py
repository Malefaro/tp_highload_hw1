from server.StatusLine import *
from server.Header import *
from server.Response import *


async def send_error(conn, status_code, loop):
    headers = Header()
    status_line = StatusLine(status_code)
    response = Response(status_line, headers, status_line.reason_phrese, conn, loop)
    await response.answer()


async def parse(conn, addr, pid, ROOT_DIR, loop):
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
        # senderror(conn, 404)
        print("404")
    else:
        method, address, protocol = request.split(" ", 2)
        if method in ("GET", "HEAD"):
            print("method is get or head")
            # sendfile(conn, address, method, ROOT_DIR)
        else:
            print(405)
            await send_error(conn=conn, status_code=405, loop=loop)
