from pathlib import Path
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
import aiofiles
import markdown2

from dependencies import get_doc_list

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
def home(request: Request, docs: list = Depends(get_doc_list)):
    return templates.TemplateResponse(request, "index.html", {"docs": docs})

@router.get("/view/{filename:path}")
async def view_doc(request: Request, filename: str, docs: list = Depends(get_doc_list)):
    base = Path("content").resolve()
    target = (base / f"{filename}.md").resolve()
    if not target.is_relative_to(base) or not target.exists():
        raise HTTPException(status_code=404, detail="Doc not found")
    async with aiofiles.open(target, "r", encoding="utf-8") as f:
        text = await f.read()
    html = markdown2.markdown(text, extras=["fenced-code-blocks"])
    return templates.TemplateResponse(request, "doc.html", {
        "filename": filename, "content": html, "docs": docs
    })