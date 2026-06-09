from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import Pyro5.api as pyro

ROOT = Path(__file__).resolve().parent.parent
URI_FILE = ROOT / "pyro_uri.txt"
SERVER_SCRIPT = ROOT / "backend" / "pyro_server.py"
DEFAULT_SERVICE_URI = "PYRO:project.pyro.agecalculator@127.0.0.1:9091"
SERVER_LOG = ROOT / "pyro_server.log"


def _start_server_process() -> None:
    with SERVER_LOG.open("a", encoding="utf-8") as log_file:
        subprocess.Popen(
            [sys.executable, str(SERVER_SCRIPT)],
            cwd=str(ROOT),
            stdout=log_file,
            stderr=log_file,
        )


def _proxy_is_available() -> bool:
    try:
        uri = load_service_uri()
        with pyro.Proxy(uri) as proxy:
            return proxy.healthcheck() == "ok"
    except Exception:
        return False


def load_service_uri() -> str:
    if URI_FILE.exists():
        uri = URI_FILE.read_text(encoding="utf-8").strip()
        if uri:
            return uri
    return DEFAULT_SERVICE_URI


def ensure_service_available(timeout_seconds: float = 30.0) -> str:
    if _proxy_is_available():
        return load_service_uri()

    _start_server_process()

    deadline = time.time() + timeout_seconds
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            uri = load_service_uri()
            with pyro.Proxy(uri) as proxy:
                if proxy.healthcheck() == "ok":
                    return uri
        except Exception as exc:
            last_error = exc
        time.sleep(0.25)

    raise RuntimeError(
        "No fue posible iniciar o contactar el servidor Pyro remoto."
        + (f" Detalle: {last_error}" if last_error else "")
    )


def calculate_remote(birthdate_text: str) -> dict[str, Any]:
    uri = ensure_service_available()
    with pyro.Proxy(uri) as proxy:
        return proxy.calculate(birthdate_text)