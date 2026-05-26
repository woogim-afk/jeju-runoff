from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

app = FastAPI()

# ── 환경변수로 허용 블로그 도메인 설정 ──────────────────────────────
# Railway 환경변수에 ALLOWED_BLOG 를 설정하세요 (예: myblog.tistory.com)
ALLOWED_BLOG = os.environ.get("ALLOWED_BLOG", "").strip().lower()

def is_allowed(request: Request) -> bool:
    """Referer 또는 Origin 헤더가 허용 블로그 도메인인지 확인"""
    if not ALLOWED_BLOG:
        return True  # 환경변수 미설정 시 전체 허용 (개발 중)
    
    referer = request.headers.get("referer", "").lower()
    origin  = request.headers.get("origin",  "").lower()
    
    return ALLOWED_BLOG in referer or ALLOWED_BLOG in origin

@app.middleware("http")
async def blog_only_guard(request: Request, call_next):
    """블로그 외 접근 차단 미들웨어"""
    # 정적 파일 요청은 통과
    path = request.url.path
    if path.startswith("/static") or path == "/health":
        return await call_next(request)
    
    if not is_allowed(request):
        html = """<!DOCTYPE html>
<html lang="ko">
<head><meta charset="UTF-8"><title>접근 제한</title>
<style>
  body{font-family:sans-serif;display:flex;align-items:center;justify-content:center;
       min-height:100vh;margin:0;background:#f5f5f5;}
  .box{background:#fff;border-radius:12px;padding:40px;text-align:center;
       border:1px solid #e0e0e0;max-width:400px;}
  h2{color:#085041;margin-bottom:12px;}
  p{color:#666;font-size:14px;line-height:1.6;}
</style></head>
<body><div class="box">
  <h2>🔒 접근 제한</h2>
  <p>이 앱은 지정된 블로그에서만 이용할 수 있습니다.<br>
  블로그를 통해 접속해 주세요.</p>
</div></body></html>"""
        return HTMLResponse(content=html, status_code=403)
    
    return await call_next(request)

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    html_path = Path("static/index.html")
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))

@app.get("/health")
async def health():
    return JSONResponse({"status": "ok"})

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
