from __future__ import annotations

import sys
from pathlib import Path

import Pyro5.api as pyro

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.calculator_service import AgeCalculatorService
URI_FILE = ROOT / "pyro_uri.txt"
HOST = "127.0.0.1"
PORT = 9091
OBJECT_NAME = "project.pyro.agecalculator"


def main() -> None:
    service = AgeCalculatorService()
    with pyro.Daemon(host=HOST, port=PORT) as daemon:
        uri = daemon.register(service, objectId=OBJECT_NAME)
        URI_FILE.write_text(str(uri), encoding="utf-8")
        print("Servidor Pyro activo")
        print(f"URI del objeto: {uri}")
        print(f"Archivo de conexión: {URI_FILE}")
        print("Deja esta terminal abierta mientras uses el cliente o la web.")
        daemon.requestLoop()


if __name__ == "__main__":
    main()