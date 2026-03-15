#!/usr/bin/env python3
"""Run the Streamlit app on a free port.

This helper is useful when the default Streamlit port (8501) is already in use.
"""

import socket
import subprocess
import sys

from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP_PATH = ROOT / "streamlit_app" / "app.py"


def find_free_port(start: int = 8501, end: int = 8600) -> int:
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No free port found")


def main() -> int:
    port = find_free_port()
    print(f"Starting Streamlit on http://localhost:{port} (auto-selected free port)")
    return subprocess.call(
        [sys.executable, "-m", "streamlit", "run", str(APP_PATH), "--server.port", str(port)]
    )


if __name__ == "__main__":
    raise SystemExit(main())
