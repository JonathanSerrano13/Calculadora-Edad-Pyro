from __future__ import annotations

import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import Pyro5.api as pyro

from backend.calculator_service import AgeCalculatorService
from backend.pyro_client import calculate_remote, ensure_service_available

import os

ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT / "frontend"
# Allow PORT and HOST to be configured by the environment (useful on Render)
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))
PYRO_HOST = "127.0.0.1"
PYRO_PORT = 9091
OBJECT_NAME = "project.pyro.agecalculator"
URI_FILE = ROOT / "pyro_uri.txt"


def start_embedded_pyro_server() -> str:
    ready = threading.Event()
    failure: list[BaseException] = []
    uri_box: list[str] = []

    def run_server() -> None:
        try:
            service = AgeCalculatorService()
            with pyro.Daemon(host=PYRO_HOST, port=PYRO_PORT) as daemon:
                uri = daemon.register(service, objectId=OBJECT_NAME)
                URI_FILE.write_text(str(uri), encoding="utf-8")
                uri_box.append(str(uri))
                ready.set()
                daemon.requestLoop()
        except BaseException as exc:  # pragma: no cover - surfaced on startup
            failure.append(exc)
            ready.set()

    threading.Thread(target=run_server, daemon=True).start()

    if not ready.wait(timeout=10):
        raise RuntimeError("No fue posible iniciar el servidor Pyro embebido.")

    if failure:
        raise RuntimeError(f"No fue posible iniciar el servidor Pyro embebido: {failure[0]}")

    if not uri_box:
        raise RuntimeError("El servidor Pyro embebido no devolvió una URI válida.")

    return uri_box[0]


class PyroBridgeHandler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.end_headers()

    def do_POST(self) -> None:
        if self.path != "/api/calculate":
            self.send_error(404, "Ruta no encontrada")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length).decode("utf-8")
        try:
            payload = json.loads(raw_body or "{}")
            birthdate_text = str(payload.get("birthdate", "")).strip()
            if not birthdate_text:
                raise ValueError("Ingresa una fecha de nacimiento.")
            result = calculate_remote(birthdate_text)
        except Exception as exc:
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            response = {"error": str(exc)}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))


def main() -> None:
    uri = start_embedded_pyro_server()
    print(f"Servidor Pyro listo en {uri}")

    handler = partial(PyroBridgeHandler, directory=str(FRONTEND_DIR))
    server = ThreadingHTTPServer((HOST, PORT), handler)
    print(f"Servidor web activo en http://{HOST}:{PORT}")
    print("Este servidor sirve la interfaz y la conecta al objeto remoto Pyro.")
    server.serve_forever()


if __name__ == "__main__":
    main()