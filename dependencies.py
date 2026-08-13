import os
import secrets
from pathlib import Path
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials