# Dynamic Markdown Documentation Portal
# by - Arnab Kumar roy karjee
## Run it
1. `python -m venv env` then activate it
2. `pip install -r requirements.txt`
3. `uvicorn main:app --reload`
4. Visit http://127.0.0.1:8000

## Structure
- `main.py` — routes
- `content/` — your .md files live here, subfolders supported
- `templates/` — Jinja2 HTML (base.html is the shared layout)
- `static/` — CSS, including generated pygments.css