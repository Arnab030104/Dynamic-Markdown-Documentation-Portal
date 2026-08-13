from pathlib import Path
from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import aiofiles

from dependencies import get_doc_list, verify_admin

router = APIRouter(prefix="/admin", dependencies=[Depends(verify_admin)])
templates = Jinja2Templates(directory="templates")

@router.get("")
def admin_home(request: Request, docs: list = Depends(get_doc_list)):
    return templates.TemplateResponse(request, "admin.html", {"docs": docs})

@router.get("/new")
def new_doc_form(request: Request, docs: list = Depends(get_doc_list)):
    return templates.TemplateResponse(request, "new_doc.html", {"docs": docs})

@router.post("/new")
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

@router.get("/edit/{filename:path}")
async def edit_doc_form(request: Request, filename: str, docs: list = Depends(get_doc_list)):
    base = Path("content").resolve()
    target = (base / f"{filename}.md").resolve()
    if not target.is_relative_to(base) or not target.exists():
        raise HTTPException(status_code=404, detail="Doc not found")
    async with aiofiles.open(target, "r", encoding="utf-8") as f:
        content = await f.read()
    return templates.TemplateResponse(request, "edit_doc.html", {
        "docs": docs, "filename": filename, "content": content
    })

@router.post("/edit/{filename:path}")
async def save_doc(filename: str, content: str = Form(...)):
    base = Path("content").resolve()
    target = (base / f"{filename}.md").resolve()
    if not target.is_relative_to(base) or not target.exists():
        raise HTTPException(status_code=404, detail="Doc not found")
    async with aiofiles.open(target, "w", encoding="utf-8") as f:
        await f.write(content)
    return RedirectResponse(url=f"/view/{filename}", status_code=303)

@router.post("/delete/{filename:path}")
async def delete_doc(filename: str):
    base = Path("content").resolve()
    target = (base / f"{filename}.md").resolve()
    if not target.is_relative_to(base) or not target.exists():
        raise HTTPException(status_code=404, detail="Doc not found")
    target.unlink()
    return RedirectResponse(url="/admin", status_code=303)