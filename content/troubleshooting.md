# Troubleshooting Guide

This guide contains solutions for common TaskFlow problems.

## Application Won't Start

### Symptom

The application exits immediately after starting.

### Check the Logs

```bash
python main.py
```

Look for errors containing:

```text
ModuleNotFoundError
ImportError
ConnectionError
```

### Solution

Reinstall dependencies:

```bash
pip install -r requirements.txt
```

---

## Database Connection Failed

### Error

```text
Connection refused: PostgreSQL server is unavailable
```

### Check PostgreSQL

```bash
systemctl status postgresql
```

Start PostgreSQL:

```bash
sudo systemctl start postgresql
```

---

## Port Already in Use

### Error

```text
Address already in use
```

Find the process using port `8000`:

```bash
lsof -i :8000
```

Then stop the process:

```bash
kill <PID>
```

On Windows:

```powershell
netstat -ano | findstr :8000
```

---

## Invalid API Key

If you receive:

```http
401 Unauthorized
```

check that your request contains:

```http
Authorization: Bearer YOUR_API_KEY
```

Also verify that the API key hasn't expired.

---

## Slow API Requests

Possible causes include:

* Missing database indexes
* Large database queries
* Network latency
* High server load
* Too many simultaneous requests

### Diagnostic Steps

1. Check application logs.
2. Check database query performance.
3. Check CPU usage.
4. Check memory usage.
5. Check network latency.

---

## Common HTTP Errors

| Error | Possible Cause           | Solution           |
| ----- | ------------------------ | ------------------ |
| `400` | Invalid request          | Check request body |
| `401` | Missing authentication   | Check API token    |
| `403` | Insufficient permissions | Check user role    |
| `404` | Resource missing         | Verify resource ID |
| `429` | Rate limit exceeded      | Wait and retry     |
| `500` | Server error             | Check server logs  |

---

## Still Having Problems?

Before contacting support, collect:

* Application version
* Operating system
* Python version
* Error message
* Relevant log output
* Steps to reproduce the problem

> **Never send API keys, passwords, or other secrets in support requests.**

## Support Information

**Response time:** Usually within one business day.

**Priority issues:** Production outages should be reported immediately.
