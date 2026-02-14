from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse


class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        status, body = self.get_response()
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def get_response(self):
        path = self.url().path
        query = self.query_data()

        if path.startswith("/proyecto/"):
            parts = path.strip("/").split("/")
            proyecto = parts[1] if len(parts) >= 2 else ""
            autor = query.get("autor")

            if autor is not None:
                return 200, f"<h1>Proyecto: {proyecto} Autor: {autor}</h1>"
            
        if path == "/":
            with open("home.html", "r", encoding="utf-8") as f:
                return 200, f.read()
            
        return 404, "<h1>404 Not Found</h1>"


if __name__ == "__main__":
    print("Starting server")
    server = HTTPServer(("localhost", 8000), WebRequestHandler)
    server.serve_forever()
