#!/usr/bin/env python3
"""Open the 稟冊 v0.21 UI and save screenshots.

The HTML, CSS, and app.js are the files from
Ya-MiC/ymzz-loop commit 4d59b866 (branch cursor/v021-integrated-app-e023).
A local stand-in answers the session calls so that file can draw. It is not
the Rust core, and the numbers on 彙報 are the empty state the page itself
writes. Fonts are read from the clone at runtime and are not copied into
this skill repository.
"""

from __future__ import annotations

import asyncio
import json
import shutil
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import websockets

UI = Path("/tmp/ymzz-loop/app/ui")
OUT = Path(__file__).resolve().parents[1] / "assets" / "product" / "screens"
COMMIT = "4d59b866db00a4cb8e8e05253772dcdc49ae988e"
MODE = {"done": False}


def api_body(path: str) -> dict:
    if path == "/api/session":
        return {"csrf": "screenshot"}
    if path == "/api/onboarding":
        if MODE["done"]:
            return {"onboarding_done": True, "nickname": "用戶", "step": 6}
        return {"onboarding_done": False, "step": 1}
    if path == "/api/root":
        return {}
    if path == "/api/dashboard":
        return {
            "files_indexed": 0,
            "source_label": "還沒掃描",
            "snapshot": None,
            "threads": 0,
            "orders": 0,
            "clock_label": "本機",
            "telemetry": False,
            "v020": {"markdown_files": [], "remind_time": "07:00", "max_days": 600},
        }
    if path == "/api/panel1/groups":
        return {"groups": {}}
    if path == "/api/ocr/last":
        return {}
    if path == "/api/threads":
        return {"threads": []}
    return {"ok": True}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        return

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("content-type", content_type)
        self.send_header("content-length", str(len(body)))
        self.send_header("cache-control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _api(self) -> None:
        path = urlparse(self.path).path
        body = json.dumps(api_body(path), ensure_ascii=False).encode("utf-8")
        self._send(200, body, "application/json; charset=utf-8")

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path.startswith("/api/"):
            self._api()
            return
        if path in ("", "/"):
            path = "/index.html"
        file = (UI / path.lstrip("/")).resolve()
        if not str(file).startswith(str(UI.resolve())) or not file.is_file():
            self._send(404, b"missing", "text/plain")
            return
        kind = "text/plain"
        if file.suffix == ".html":
            kind = "text/html; charset=utf-8"
        elif file.suffix == ".css":
            kind = "text/css; charset=utf-8"
        elif file.suffix == ".js":
            kind = "text/javascript; charset=utf-8"
        elif file.suffix == ".woff2":
            kind = "font/woff2"
        self._send(200, file.read_bytes(), kind)

    def do_POST(self) -> None:
        length = int(self.headers.get("content-length", "0"))
        if length:
            self.rfile.read(length)
        self._api()


async def command(ws, method: str, params: dict | None = None) -> dict:
    command.seq += 1
    await ws.send(json.dumps({"id": command.seq, "method": method, "params": params or {}}))
    while True:
        message = json.loads(await ws.recv())
        if message.get("id") == command.seq:
            if "error" in message:
                raise RuntimeError(message["error"])
            return message.get("result", {})


command.seq = 0


async def evaluate(ws, expression: str):
    result = await command(
        ws,
        "Runtime.evaluate",
        {"expression": expression, "awaitPromise": True, "returnByValue": True},
    )
    if result.get("exceptionDetails"):
        raise RuntimeError(result["exceptionDetails"])
    return result.get("result", {}).get("value")


async def shoot(ws, path: Path) -> None:
    await evaluate(ws, "document.fonts.ready")
    await asyncio.sleep(0.4)
    image = await command(ws, "Page.captureScreenshot", {"format": "png"})
    path.write_bytes(__import__("base64").b64decode(image["data"]))


async def open_page(ws, url: str) -> None:
    await command(ws, "Page.navigate", {"url": url})
    await evaluate(
        ws,
        """
        new Promise((resolve) => {
          const start = Date.now();
          const tick = () => {
            const onboard = document.getElementById('onboard');
            const ready = onboard && document.body && document.body.innerText.length > 0;
            if (ready || Date.now() - start > 8000) resolve(true);
            else setTimeout(tick, 50);
          };
          tick();
        })
        """,
    )


async def capture(port: int) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    chrome = shutil.which("google-chrome") or shutil.which("chromium")
    if not chrome:
        raise SystemExit("Chrome is not installed")
    profile = Path("/tmp/wenrun-chrome-profile")
    if profile.exists():
        shutil.rmtree(profile)
    process = subprocess.Popen(
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            "--window-size=1440,900",
            f"--remote-debugging-port={port + 1}",
            f"--user-data-dir={profile}",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        deadline = time.time() + 20
        page = None
        while time.time() < deadline:
            try:
                import urllib.request

                with urllib.request.urlopen(f"http://127.0.0.1:{port + 1}/json/list") as response:
                    pages = json.load(response)
                    page = next(item for item in pages if item.get("type") == "page")
                    break
            except Exception:
                await asyncio.sleep(0.2)
        if not page:
            raise SystemExit("Chrome debugging port did not open")
        async with websockets.connect(page["webSocketDebuggerUrl"], max_size=16_000_000) as ws:
            await command(ws, "Page.enable")
            await command(ws, "Runtime.enable")
            await command(
                ws,
                "Emulation.setDeviceMetricsOverride",
                {"width": 1440, "height": 900, "deviceScaleFactor": 1, "mobile": False},
            )
            MODE["done"] = False
            await open_page(ws, f"http://127.0.0.1:{port}/")
            await shoot(ws, OUT / "desktop-onboarding.png")

            MODE["done"] = True
            await open_page(ws, f"http://127.0.0.1:{port}/")
            await shoot(ws, OUT / "desktop-files.png")
            await evaluate(ws, "document.querySelector('[data-panel=\"report\"]').click()")
            await asyncio.sleep(0.3)
            await shoot(ws, OUT / "desktop-report.png")
            await evaluate(ws, "document.querySelector('.side [data-panel=\"links\"]').click()")
            await asyncio.sleep(0.3)
            await shoot(ws, OUT / "desktop-links.png")

            await command(
                ws,
                "Emulation.setDeviceMetricsOverride",
                {"width": 390, "height": 844, "deviceScaleFactor": 1, "mobile": True},
            )
            MODE["done"] = False
            await open_page(ws, f"http://127.0.0.1:{port}/")
            await shoot(ws, OUT / "mobile-onboarding.png")
            MODE["done"] = True
            await open_page(ws, f"http://127.0.0.1:{port}/")
            await shoot(ws, OUT / "mobile-files.png")
            await evaluate(ws, "document.querySelector('.main').scrollIntoView()")
            await asyncio.sleep(0.2)
            await shoot(ws, OUT / "mobile-files-work.png")
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
    note = {
        "commit": COMMIT,
        "ui": "app/ui/index.html, app.css, tokens.css, app.js",
        "repo": "https://github.com/Ya-MiC/ymzz-loop",
        "branch": "cursor/v021-integrated-app-e023",
        "renderer": "Google Chrome headless, the real page files",
        "core": "local stand-in for session calls only; not the Rust binary",
    }
    (OUT / "capture.json").write_text(json.dumps(note, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("captured", COMMIT)


def main() -> None:
    if not (UI / "index.html").exists():
        raise SystemExit(f"missing {UI}; clone Ya-MiC/ymzz-loop at {COMMIT}")
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        asyncio.run(capture(port))
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
