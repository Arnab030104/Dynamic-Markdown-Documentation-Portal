import os
import secrets
from pathlib import Path
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

def get_doc_list():
    files = [str(p.relative_to("content")) for p in Path("content").rglob("*.md")]
    return [f.replace(".md", "") for f in files]

security = HTTPBasic()

def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, os.environ["ADMIN_USERNAME"])
    correct_password = secrets.compare_digest(credentials.password, os.environ["ADMIN_PASSWORD"])
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username