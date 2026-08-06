from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException as FastAPIHTTPException
import markdown2
import os
from pathlib import Path
import aiofiles

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


def get_doc_list():
    files = [str(p.relative_to("content")) for p in Path("content").rglob("*.md")]
    return [f.replace(".md", "") for f in files]

@app.get("/")
def home(request: Request, docs: list = Depends(get_doc_list)):
    return templates.TemplateResponse(request, "index.html", {"docs": docs})

@app.get("/view/{filename:path}")
async def view_doc(request: Request, filename: str, docs: list = Depends(get_doc_list)):
    base = Path("content").resolve()
    target = (base / f"{filename}.md").resolve()
    if not target.is_relative_to(base):
        raise HTTPException(status_code=400, detail="Invalid path")
    if not target.exists():
        raise HTTPException(status_code=404, detail="Doc not found")
    async with aiofiles.open(target, "r", encoding="utf-8") as f:
        text = await f.read()
    html = markdown2.markdown(text, extras=["fenced-code-blocks"])
    return templates.TemplateResponse(request, "doc.html", {
        "filename": filename,
        "content": html,
        "docs": docs
    })

@app.get("/list")
def get_list():
    files = [str(p.relative_to("content")) for p in Path("content").rglob("*.md")]

    return {"files":files}

@app.exception_handler(404)
async def not_found(request: Request, exc : FastAPIHTTPException):
    return templates.TemplateResponse(
        request,"404.html", {"docs": get_doc_list() },status_code=404
    )
