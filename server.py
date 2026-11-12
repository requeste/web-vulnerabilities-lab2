from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs
from db import db_init, add_user, check_user

db_init()

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        fields = parse_qs(body)

        user = fields.get("username", [""])[0]
        password = fields.get("password", [""])[0]

        if not user or not password:
            self.send_error(400, explain="Имя или пароль не заполнены")
            return

        if self.path == "/register":
            add_user(user, password)
            self.send_response(303)
            self.send_header("Location", "https://github.com/requeste")
            self.end_headers()
            return

        if self.path == "/login":
            if check_user(user, password):
                self.send_response(303)
                self.send_header("Location", "https://github.com/requeste")
                self.end_headers()
                return
            else:
                self.send_error(401, explain="Неправильный логин или пароль")
                return

    def do_GET(self):
        if self.path == "/backup":
            bp = Path(__file__).with_name("database.db").read_bytes()

            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header(
                "Content-Disposition",
                'attachment; filename="backup.db"'
            )
            self.send_header("Content-Length", str(len(bp)))
            self.end_headers()

            self.wfile.write(bp)
            return
        
        if self.path == "/style.css":
            filename = "style.css"
            content_type = "text/css; charset=utf-8"

        elif self.path == "/picture.png":
            filename = "picture.png"
            content_type = "image/png"

        elif self.path == "/register":
            filename = "register.html"
            content_type = "text/html; charset=utf-8"

        else:
            filename = "site.html"
            content_type = "text/html; charset=utf-8"

        page = Path(__file__).with_name(filename).read_bytes()

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(page)

host = "localhost"
port = 8000

server = HTTPServer((host, port), Handler)
print(f"Сервер запущен http://{host}:{port}")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("Сервер остановлен")

server.server_close()