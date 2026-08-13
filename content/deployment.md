# Deployment Guide

This guide explains how to deploy TaskFlow to a production server.

## Architecture

A typical production deployment looks like this:

```text
                Internet
                   │
                   ▼
              ┌─────────┐
              │ Nginx   │
              └────┬────┘
                   │
                   ▼
              ┌─────────┐
              │ FastAPI │
              └────┬────┘
                   │
          ┌────────┴────────┐
          ▼                 ▼
      PostgreSQL          Redis
```

## Server Requirements

Recommended production server:

| Resource |      Minimum |
| -------- | -----------: |
| CPU      |      2 cores |
| RAM      |         4 GB |
| Storage  |        20 GB |
| OS       | Ubuntu 24.04 |

## Environment Variables

Production configuration:

```env
APP_ENV=production
DEBUG=false
DATABASE_URL=postgresql://user:password@localhost/taskflow
REDIS_URL=redis://localhost:6379
SECRET_KEY=change-this-value
```

## Build Application

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run With Uvicorn

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

For multiple workers:

```bash
uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4
```

## Nginx Configuration

Example configuration:

```nginx
server {
    listen 80;

    server_name api.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Health Check

The application provides:

```http
GET /health
```

Expected response:

```json
{
  "status": "healthy"
}
```

## Deployment Checklist

* [ ] Configure production environment variables
* [ ] Configure database
* [ ] Run database migrations
* [ ] Configure HTTPS
* [ ] Configure Nginx
* [ ] Configure backups
* [ ] Start application workers
* [ ] Verify health endpoint
* [ ] Monitor application logs

## Rollback

If a deployment fails:

1. Stop the new application version.
2. Restore the previous version.
3. Roll back database migrations if necessary.
4. Restart the application.
5. Verify the health endpoint.

> Always test rollback procedures before a production deployment.
