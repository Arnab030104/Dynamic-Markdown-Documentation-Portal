# Getting Started

Welcome to **TaskFlow**! This guide will help you get your first project running in a few minutes.

## Prerequisites

Before you begin, make sure you have:

* Python 3.10 or newer
* Git installed
* A TaskFlow account
* An API key

## Installation

Clone the repository:

```bash
git clone https://github.com/example/taskflow.git
cd taskflow
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file:

```env
TASKFLOW_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///taskflow.db
DEBUG=true
```

> **Security:** Never commit your `.env` file to Git.

## Start the Application

```bash
python main.py
```

You should see:

```text
Server running on http://localhost:8000
```

Open your browser and visit:

http://localhost:8000

## Next Steps

After installation, you can:

1. Create your first project.
2. Add team members.
3. Create tasks.
4. Configure notifications.
5. Explore the API.

---

**You're ready to go! 🎉**
