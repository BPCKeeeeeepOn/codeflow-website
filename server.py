#!/usr/bin/env python3
"""server.py —— 官网站点服务（FastAPI，与产品同栈）。

职责：
  · 静态托管 site/（纯静态产物）
  · /api/health 健康检查（部署探活用）
  · 干净的 404（未匹配路径回 site/404.html）

运行：
  uvicorn server:app --port 8899        # 或 python server.py
说明：官网本体是静态站点，本服务只做托管与探活，不承载业务逻辑。
"""
from __future__ import annotations
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

BASE = Path(__file__).resolve().parent
SITE = BASE / "site"

app = FastAPI(title="TestOps 官网", docs_url=None, redoc_url=None)


@app.get("/api/health")
async def health() -> JSONResponse:
    """部署探活：站点产物是否就位。"""
    index = SITE / "index.html"
    return JSONResponse({
        "status": "up" if index.exists() else "degraded",
        "site": str(SITE),
        "pages": len(list(SITE.glob("*.html"))),
    })


# 静态托管（必须最后挂载：mount("/") 会吞掉之后声明的路由）
app.mount("/", StaticFiles(directory=str(SITE), html=True), name="site")


@app.exception_handler(404)
async def not_found(request: Request, exc) -> FileResponse:
    """静态托管下未匹配路径 → 站点自己的 404 页，而不是框架默认 JSON。"""
    return FileResponse(SITE / "404.html", status_code=404)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8899)
