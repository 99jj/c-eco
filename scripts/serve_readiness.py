import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, _format: str, *_args: object) -> None:
        pass


server = ThreadingHTTPServer(("127.0.0.1", 8765), QuietHandler)
timer = threading.Timer(5, server.shutdown)
timer.start()
try:
    server.serve_forever(poll_interval=0.1)
finally:
    timer.cancel()
    server.server_close()
