import threading

from mcp_server.server import mcp


def _start_mcp():
    mcp.run(transport="http", host="0.0.0.0", port=8090, path="/")


_thread = threading.Thread(target=_start_mcp, daemon=True)
_thread.start()
