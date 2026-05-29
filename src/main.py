"""Servidor local para CompyFI LR(0)."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import socket

from ui import CODIGO_INICIAL, render_page, render_view

HOST = "127.0.0.1"
PUERTO_INICIAL = 8000
BASE_DIR = Path(__file__).resolve().parent


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/multimedia/"):
            self.serve_file(BASE_DIR / parsed.path.lstrip("/"))
            return

        params = parse_qs(parsed.query)
        view = params.get("view", ["compilador"])[0]
        ejemplo_id = params.get("example", ["valido"])[0]
        content = render_view(view, ejemplo_id=ejemplo_id)
        self.send_html(render_page(view, content))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        codigo = parse_qs(body).get("codigo", [CODIGO_INICIAL])[0]
        content = render_view("compilador", codigo_manual=codigo)
        self.send_html(render_page("compilador", content))

    def serve_file(self, path):
        if not path.exists() or not path.is_file():
            self.send_error(404)
            return
        data = path.read_bytes()
        suffix = path.suffix.lower()
        content_type = "image/png" if suffix == ".png" else "image/gif" if suffix == ".gif" else "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_html(self, html_text):
        data = html_text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, formato, *args):
        return


def puerto_disponible(puerto_inicial):
    puerto = puerto_inicial
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex((HOST, puerto)) != 0:
                return puerto
        puerto += 1


def main():
    puerto = puerto_disponible(PUERTO_INICIAL)
    url = f"http://{HOST}:{puerto}/index.html"
    print("\n=== CompyFI - Compilador LR(0) ===")
    print(f"Abre este enlace en el navegador: {url}")
    print("Presiona Ctrl+C para detener el servidor.\n")
    server = ThreadingHTTPServer((HOST, puerto), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
