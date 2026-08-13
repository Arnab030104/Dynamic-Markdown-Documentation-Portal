# Database Documentation

TaskFlow uses a relational database to store projects, users, tasks, and activity records.

## Database Architecture

```text
Application
    │
    ├── Users
    │
    ├── Projects
    │      │
    │      └── Tasks
    │
    └── Activity Logs
```

## Users Table

| Column       | Type      | Description           |
| ------------ | --------- | --------------------- |
| `id`         | INTEGER   | Unique user ID        |
| `name`       | VARCHAR   | User's full name      |
| `email`      | VARCHAR   | Email address         |
| `created_at` | TIMESTAMP | Account creation date |

## Projects Table

| Column        | Type         | Nullable |
| ------------- | ------------ | -------- |
| `id`          | INTEGER      | No       |
| `name`        | VARCHAR(150) | No       |
| `description` | TEXT         | Yes      |
| `owner_id`    | INTEGER      | No       |
| `created_at`  | TIMESTAMP    | No       |

## Tasks Table

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(30) DEFAULT 'pending',
    priority VARCHAR(20) DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Relationships

A project can contain many tasks:

```text
Project 1 ──────────── * Tasks
```

A user can own multiple projects:

```text
User 1 ─────────────── * Projects
```

## Indexing

The following columns should be indexed:

* `users.email`
* `tasks.project_id`
* `tasks.status`
* `tasks.created_at`

> Indexes improve query performance but increase storage requirements.

## Backup Strategy

Database backups are performed daily.

Recommended retention:

| Backup  | Retention |
| ------- | --------: |
| Daily   |    7 days |
| Weekly  |   4 weeks |
| Monthly | 12 months |

## Migration

Run migrations using:

```bash
python manage.py migrate
```

To create a new migration:

```bash
python manage.py makemigrations
```

---

**Database changes should always be tested in a staging environment before production.**
