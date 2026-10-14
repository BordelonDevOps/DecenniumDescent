"""Single-use, loopback-only visible text preview for an explicitly selected review packet."""
import argparse,hashlib
from pathlib import Path
from http.server import BaseHTTPRequestHandler,HTTPServer
p=argparse.ArgumentParser()
p.add_argument('packet')
args=p.parse_args()
root=Path(__file__).resolve().parent
packet=(root/args.packet).resolve()
assert packet.parent==root and packet.name.startswith('CODEX_') and packet.suffix=='.md'
payload=packet.read_bytes()
assert len(payload)<1_000_000
served=False
class ReviewHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global served
        if self.path!='/review':
            self.send_error(404);return
        self.send_response(200)
        self.send_header('Content-Type','text/plain; charset=utf-8')
        self.send_header('Content-Length',str(len(payload)))
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.end_headers()
        self.wfile.write(payload)
        self.wfile.flush()
        served=True
    def log_message(self,*args):pass
with HTTPServer(('127.0.0.1',0),ReviewHandler) as server:
    server.timeout=120
    print(f'http://127.0.0.1:{server.server_port}/review',flush=True)
    print(f'UTF8 characters={len(payload.decode("utf-8"))}; SHA256={hashlib.sha256(payload).hexdigest()}',flush=True)
    server.handle_request()
print(f'Served={served}; preview server stopped.',flush=True)
