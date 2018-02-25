async def parse(conn, addr, pid, ROOT_DIR):
    data = b""

    while not b"\r\n" in data:
        # read data wile does not get first line
        tmp = conn.recv(1024)
        # if empty data
        if not tmp:
            break
        else:
            data += tmp

    # if data is empty
    if not data:
        return

    udata = data.decode("utf-8")
    udata = udata.split("\r\n", 1)[0]
    print(udata.split(" ", 2))
    if len(udata.split(" ", 2)) < 3:
        # senderror(conn, 404)
        print("404")
    else:
        method, address, protocol = udata.split(" ", 2)
        if method in ("GET", "HEAD"):
            print("method is get or head")
            # sendfile(conn, address, method, ROOT_DIR)
        else:
            print(405)
            # senderror(conn, 405)
