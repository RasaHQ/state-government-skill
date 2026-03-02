import socket
import threading
import time

from mcp_server.server import mcp


def _start_mcp():
    mcp.run(transport="http", host="0.0.0.0", port=8090, path="/")


_thread = threading.Thread(target=_start_mcp, daemon=True)
_thread.start()

# Block until the server is actually accepting connections
for _ in range(50):
    try:
        with socket.create_connection(("127.0.0.1", 8090), timeout=1):
            break
    except OSError:
        time.sleep(0.2)
