#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler


class CustomHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-XSS-Protection", "0")
        SimpleHTTPRequestHandler.end_headers(self)


if __name__ == "__main__":
    print("Starting test server on http://localhost:8000")
    HTTPServer(("", 8000), CustomHandler).serve_forever()
