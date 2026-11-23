"""Local server for the stream-trim page: the page, the ranged preview, and
a small JSON API to read state and start/stop the final render.

  python3 server.py <raw.mp4>     prints: READY http://127.0.0.1:<port>/
Run prepare.py on the recording first."""
import json
import math
import os
import re
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import audio_chain
import prepare
import render

HERE = os.path.dirname(os.path.abspath(__file__))
CHUNK = 1 << 20


class TrimServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, raw, chain, port):
        self.raw = raw
        self.chain = chain
        self.cache = prepare.cache_dir(raw)
        with open(os.path.join(self.cache, "analysis.json")) as f:
            self.analysis = json.load(f)
        with open(os.path.join(self.cache, "peaks.json")) as f:
            self.peaks = json.load(f)
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.status = {"state": "idle", "phase": None, "percent": 0, "output": None, "error": None}
        super().__init__(("127.0.0.1", port), Handler)

    def render_status(self):
        with self.lock:
            return dict(self.status)

    def start_render(self, in_s, out_s):
        """Returns (http code, body)."""
        with self.lock:
            if self.status["state"] == "running":
                return 409, {"error": "a render is already running"}
            if os.path.exists(render.final_path(self.raw)):
                return 409, {"error": f"{os.path.basename(render.final_path(self.raw))} already exists"}
            self.stop_event.clear()
            self.status = {"state": "running", "phase": "measuring", "percent": 0,
                           "output": None, "error": None}
        threading.Thread(target=self._render, args=(in_s, out_s), daemon=True).start()
        return 202, {"ok": True}

    def _render(self, in_s, out_s):
        def progress(percent, phase):
            with self.lock:
                self.status.update(percent=round(percent, 1), phase=phase)

        try:
            out = render.render_final(self.raw, in_s, out_s, self.chain,
                                      progress=progress, stop=self.stop_event)
            update = {"state": "done", "percent": 100, "output": out}
        except Exception as e:  # report anything to the page
            update = {"state": "error", "error": str(e)}
        with self.lock:
            self.status.update(update)


class Handler(BaseHTTPRequestHandler):
    server: TrimServer

    def log_message(self, *args):
        pass

    def send_json(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        s = self.server
        if self.path == "/":
            self.send_file(os.path.join(HERE, "page.html"), "text/html; charset=utf-8")
        elif self.path == "/proxy.mp4":
            self.send_ranged(os.path.join(s.cache, "proxy.mp4"))
        elif self.path == "/api/state":
            out = render.final_path(s.raw)
            self.send_json(200, {**s.analysis, "peaks": s.peaks["peaks"], "per_s": s.peaks["per_s"],
                                 "name": os.path.basename(s.raw), "render": s.render_status(),
                                 "output": out, "exists": os.path.exists(out)})
        elif self.path == "/api/render":
            self.send_json(200, s.render_status())
        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):
        s = self.server
        length = int(self.headers.get("Content-Length") or 0)
        raw_body = self.rfile.read(length) if length else b""
        if self.path == "/api/render":
            try:
                body = json.loads(raw_body)
                in_s, out_s = body["in"], body["out"]
                if not all(isinstance(x, (int, float)) and not isinstance(x, bool)
                           and math.isfinite(x) for x in (in_s, out_s)):
                    raise ValueError("in and out must be numbers")
                if not 0 <= in_s < out_s <= s.analysis["duration"]:
                    raise ValueError(f"need 0 <= in < out <= {s.analysis['duration']:.2f}")
            except (ValueError, KeyError, TypeError) as e:
                self.send_json(400, {"error": str(e) or "bad request"})
                return
            self.send_json(*s.start_render(float(in_s), float(out_s)))
        elif self.path == "/api/stop":
            if s.render_status()["state"] != "running":
                self.send_json(409, {"error": "no render is running"})
            else:
                s.stop_event.set()
                self.send_json(200, {"ok": True})
        else:
            self.send_json(404, {"error": "not found"})

    def send_file(self, path, ctype):
        if not os.path.exists(path):
            self.send_json(404, {"error": f"{os.path.basename(path)} missing"})
            return
        with open(path, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_ranged(self, path):
        size = os.path.getsize(path)
        start, end, code = 0, size - 1, 200
        m = re.fullmatch(r"bytes=(\d+)-(\d*)", self.headers.get("Range", ""))
        if m:
            start = int(m.group(1))
            end = min(int(m.group(2)), size - 1) if m.group(2) else size - 1
            if start > end:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{size}")
                self.end_headers()
                return
            code = 206
        self.send_response(code)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1))
        if code == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        try:
            with open(path, "rb") as f:
                f.seek(start)
                left = end - start + 1
                while left > 0:
                    chunk = f.read(min(CHUNK, left))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    left -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass  # the browser cancels range requests while seeking


def make_server(raw, chain, port=0):
    return TrimServer(raw, chain, port)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: server.py <raw.mp4>")
    chain = audio_chain.load_chain(os.path.join(HERE, "chain.json"))
    try:
        srv = make_server(sys.argv[1], chain)
    except FileNotFoundError:
        sys.exit("ERROR: no prepared cache for this recording, run prepare.py first")
    print(f"READY http://127.0.0.1:{srv.server_address[1]}/", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
