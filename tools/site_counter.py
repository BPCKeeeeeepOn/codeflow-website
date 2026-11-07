#!/usr/bin/env python3
"""site-counter —— 官网浏览量统计（纯 stdlib 零依赖，SQLite 落盘，WAL）。

端点（nginx :80 → /api/counter/ 反代到本服务）：
  GET /api/hit?path=/xxx   记一次浏览，返回 {total, today, visitors}
  GET /api/stats           Top20 路径 + 总量（运维自查用）
IP 只存 sha256 前 16 位哈希，不落原始地址。
"""
import hashlib
import json
import sqlite3
import threading
import urllib.parse
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

DB = Path(__file__).resolve().parent / "hits.db"
SALT = "site-counter-v1"
_lock = threading.Lock()
_conn = sqlite3.connect(DB, check_same_thread=False)
_conn.execute("PRAGMA journal_mode=WAL")
_conn.executescript("""
CREATE TABLE IF NOT EXISTS hits(
  id     INTEGER PRIMARY KEY AUTOINCREMENT,
  day    TEXT DEFAULT (date('now','localtime')),
  iphash TEXT,
  path   TEXT);
CREATE INDEX IF NOT EXISTS idx_hits_day  ON hits(day);
CREATE INDEX IF NOT EXISTS idx_hits_path ON hits(path);
""")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # 静默 access log（错误仍走 stderr）
        pass

    def _json(self, code: int, obj: dict) -> None:
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        if u.path == "/api/hit":
            path = (q.get("path", ["/"])[0])[:120]
            ip = self.headers.get("X-Real-IP") or self.client_address[0]
            iphash = hashlib.sha256((SALT + ip).encode()).hexdigest()[:16]
            today = date.today().isoformat()
            with _lock:
                _conn.execute("INSERT INTO hits(iphash,path) VALUES(?,?)", (iphash, path))
                total = _conn.execute("SELECT COUNT(*) FROM hits").fetchone()[0]
                td = _conn.execute("SELECT COUNT(*) FROM hits WHERE day=?", (today,)).fetchone()[0]
                uv = _conn.execute("SELECT COUNT(DISTINCT iphash) FROM hits").fetchone()[0]
                _conn.commit()
            self._json(200, {"total": total, "today": td, "visitors": uv})
        elif u.path == "/api/stats":
            with _lock:
                total = _conn.execute("SELECT COUNT(*) FROM hits").fetchone()[0]
                rows = _conn.execute(
                    "SELECT path, COUNT(*) n FROM hits GROUP BY path ORDER BY n DESC LIMIT 20").fetchall()
            self._json(200, {"total": total, "top": [{"path": p, "hits": n} for p, n in rows]})
        else:
            self._json(404, {"error": "not found"})


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 8905), Handler).serve_forever()
