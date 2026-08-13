# TaskFlow API Documentation

Welcome to the **TaskFlow API** documentation. This API allows you to create, manage, and track tasks for your projects.

## Overview

The TaskFlow API is a RESTful API that uses JSON for request and response data.

### Base URL

```text
https://api.taskflow.example.com/v1
```

### Authentication

All API requests require an API key.

Include your API key in the request header:

```http
Authorization: Bearer YOUR_API_KEY
```

> **Note:** Never expose your API key in client-side JavaScript or commit it to a public repository.

---

# Tasks

Tasks are the primary resources in the TaskFlow API.

## Get All Tasks

Returns a list of tasks.

### Request

```http
GET /tasks
```

### Query Parameters

| Parameter  | Type    | Required | Description              |
| ---------- | ------- | -------- | ------------------------ |
| `page`     | integer | No       | Page number              |
| `limit`    | integer | No       | Number of tasks per page |
| `status`   | string  | No       | Filter by task status    |
| `priority` | string  | No       | Filter by priority       |

### Example Request

```bash
curl -X GET "https://api.taskflow.example.com/v1/tasks?status=pending" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Example Response

```json
{
  "success": true,
  "data": [
    {
      "id": 101,
      "title": "Create documentation portal",
      "status": "pending",
      "priority": "high",
      "created_at": "2026-08-12T10:30:00Z"
    },
    {
      "id": 102,
      "title": "Design dashboard",
      "status": "completed",
      "priority": "medium",
      "created_at": "2026-08-11T08:15:00Z"
    }
  ]
}
```

---

## Get a Single Task

Returns information about a specific task.

### Request

```http
GET /tasks/{task_id}
```

### Example

```bash
curl -X GET "https://api.taskflow.example.com/v1/tasks/101" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Response

```json
{
  "success": true,
  "data": {
    "id": 101,
    "title": "Create documentation portal",
    "description": "Build a web application that converts Markdown files into HTML.",
    "status": "pending",
    "priority": "high"
  }
}
```

---

## Create a Task

Creates a new task.

### Request

```http
POST /tasks
Content-Type: application/json
```

### Request Body

```json
{
  "title": "Build authentication system",
  "description": "Add JWT authentication to the API",
  "priority": "high"
}
```

### Example Response

```json
{
  "success": true,
  "message": "Task created successfully",
  "data": {
    "id": 103,
    "title": "Build authentication system",
    "status": "pending",
    "priority": "high"
  }
}
```

---

## Update a Task

Updates an existing task.

```http
PUT /tasks/{task_id}
```

### Example Request

```json
{
  "title": "Build authentication system",
  "status": "in_progress",
  "priority": "high"
}
```

---

## Delete a Task

Permanently deletes a task.

```http
DELETE /tasks/{task_id}
```

### Example

```bash
curl -X DELETE "https://api.taskflow.example.com/v1/tasks/103" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

> **Warning:** Deleted tasks cannot be recovered.

---

# Task Status

A task can have one of the following statuses:

* `pending`
* `in_progress`
* `completed`
* `cancelled`

The typical task lifecycle is:

```text
pending → in_progress → completed
```

A task can also be cancelled:

```text
pending → cancelled
in_progress → cancelled
```

---

# Priority Levels

Task priority can be:

| Priority     | Description                            |
| ------------ | -------------------------------------- |
| **Low**      | Minor task that can be completed later |
| **Medium**   | Normal priority task                   |
| **High**     | Important task requiring attention     |
| **Critical** | Urgent task requiring immediate action |

---

# Error Handling

The API uses standard HTTP status codes.

| Status Code | Meaning                 |
| ----------- | ----------------------- |
| `200`       | Request successful      |
| `201`       | Resource created        |
| `400`       | Invalid request         |
| `401`       | Authentication required |
| `403`       | Access denied           |
| `404`       | Resource not found      |
| `429`       | Too many requests       |
| `500`       | Internal server error   |

### Example Error

```json
{
  "success": false,
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "The requested task does not exist."
  }
}
```

---

# Rate Limits

The API allows up to:

**100 requests per minute per API key.**

If you exceed the limit, the API returns:

```http
429 Too Many Requests
```

You should wait before sending additional requests.

---

# Best Practices

Follow these recommendations when working with the API:

1. Always use HTTPS.
2. Keep your API key private.
3. Handle API errors gracefully.
4. Use pagination when retrieving large collections.
5. Cache responses when appropriate.
6. Respect the API rate limit.
7. Validate user input before sending requests.

---

# Code Examples

## Python

```python
import requests

url = "https://api.taskflow.example.com/v1/tasks"

headers = {
    "Authorization": "Bearer YOUR_API_KEY"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    tasks = response.json()
    print(tasks)
else:
    print("Request failed:", response.status_code)
```

## JavaScript

```javascript
const response = await fetch(
  "https://api.taskflow.example.com/v1/tasks",
  {
    headers: {
      Authorization: "Bearer YOUR_API_KEY"
    }
  }
);

const data = await response.json();

console.log(data);
```

---

# Changelog

## Version 1.2.0

**August 12, 2026**

* Added task priority filtering.
* Added pagination support.
* Improved error responses.
* Added JavaScript examples.

## Version 1.1.0

**July 20, 2026**

* Added task update endpoint.
* Added task deletion endpoint.
* Improved authentication.

## Version 1.0.0

**June 1, 2026**

* Initial API release.
* Added task creation.
* Added task retrieval.
* Added task listing.

---

# Support

If you encounter an issue with the API, check the error response first.

For development questions, contact the TaskFlow engineering team.

**Happy building! 🚀**
