from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        status, content_type, body = self.get_response()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
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
                return 200, "text/html; charset=utf-8", f"<h1>Proyecto: {proyecto} Autor: {autor}</h1>"
           
        pages = {
            "/": open("home.html", "r", encoding="utf-8").read(),
            "/proyecto/1": open("1.html", "r", encoding="utf-8").read(),
            "/proyecto/2": open("2.html", "r", encoding="utf-8").read(),
            "/proyecto/3": open("3.html", "r", encoding="utf-8").read(),
        }

        if path == "/css/style.css":
            css = open("css/style.css", "r", encoding="utf-8").read()
            return 200, "text/css; charset=utf-8", css
        
        if path in pages:
            return 200, "text/html; charset=utf-8", pages[path]
        
        return 404, "text/html; charset=utf-8", "<h1>404 Not Found</h1>"

if __name__ == "__main__":
    print("Starting server")
    server = HTTPServer(("localhost", 8000), WebRequestHandler)
    server.serve_forever()
