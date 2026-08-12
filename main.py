from fastapi import FastAPI, HTTPException, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
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



@app.get("/admin")
def admin_home(request: Request, docs: list = Depends(get_doc_list)):
    return templates.TemplateResponse(
        request,
        "admin.html",
        {"docs": docs}
    )
    
@app.get("/admin/new")
def new_doc_form(request: Request, docs: list = Depends(get_doc_list)):
    return templates.TemplateResponse(
        request,
        "new_doc.html",
        {"docs": docs}
    )
    
    
from fastapi import Form

@app.post("/admin/new")
async def create_doc(filename: str = Form(...), content: str = Form(...)):
    base = Path("content").resolve()
    target = (base / f"{filename}.md").resolve()
    if not target.is_relative_to(base):
        raise HTTPException(status_code=400, detail="Invalid filename")
    if target.exists():
        raise HTTPException(status_code=400, detail="File already exists")
    async with aiofiles.open(target, "w", encoding="utf-8") as f:
        await f.write(content)
    return RedirectResponse(url=f"/view/{filename}", status_code=303)


@app.get("/admin/edit/{filename:path}")
async def edit_doc_form(request: Request, filename: str, docs :list = Depends(get_doc_list)):
    base = Path("content").resolve()
    target = (base / F"{filename}.md").resolve()
    
    if not target.is_relative_to(base) or not target.exists():
        raise HTTPException(status_code=404, detail="Doc not found")
    async with aiofiles.open(target, "r", encoding="utf-8") as f:
        content = await f.read()
    return templates.TemplateResponse(
        request,
        "edit_doc.html",
        {
            "docs": docs,
            "filename": filename,
            "content": content
        }
    )
    
@app.post("/admin/edit/{filename:path}")
async def save_doc(filename: str, content: str = Form(...)):
    base = Path("content").resolve()
    target = (base / f"{filename}.md").resolve()
    if not target.is_relative_to(base) or not target.exists():
        raise HTTPException(status_code=404, detail="Doc not found")
    async with aiofiles.open(target, "w", encoding="utf-8") as f:
        await f.write(content)
    return RedirectResponse(url=f"/view/{filename}", status_code=303)


@app.post("/admin/delete/{filename:path}")
async def delete_doc(filename: str):
    base = Path("content").resolve()
    target = (base / f"{filename}.md").resolve()
    if not target.is_relative_to(base) or not target.exists():
        raise HTTPException(status_code=404, detail="Doc not found")
    target.unlink()
    return RedirectResponse(url="/admin", status_code=303)