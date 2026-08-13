# Authentication

TaskFlow uses **JSON Web Tokens (JWT)** to authenticate API requests.

## Authentication Flow

```text
Client
  │
  │ Login
  ▼
Authentication Server
  │
  │ JWT Token
  ▼
Client
  │
  │ Authorization: Bearer TOKEN
  ▼
API Server
```

## Login

Send the user's credentials to:

```http
POST /auth/login
Content-Type: application/json
```

### Request

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

### Response

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

## Making Authenticated Requests

Include the token in the `Authorization` header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

## Token Expiration

Tokens expire after **60 minutes**.

When the token expires, the API returns:

```json
{
  "error": "token_expired",
  "message": "Your authentication token has expired."
}
```

## Refreshing Tokens

Use the refresh endpoint:

```http
POST /auth/refresh
```

Example response:

```json
{
  "access_token": "new-token",
  "expires_in": 3600
}
```

## Security Recommendations

### Do

* Use HTTPS.
* Store tokens securely.
* Use short-lived access tokens.
* Rotate refresh tokens.
* Log authentication failures.

### Don't

* Store tokens in plain text files.
* Share tokens through email.
* Commit tokens to Git.
* Put private tokens in URLs.

> **Important:** Treat access tokens like passwords.

## Logout

To invalidate a session:

```http
POST /auth/logout
Authorization: Bearer YOUR_TOKEN
```

A successful request returns:

```json
{
  "success": true,
  "message": "Logged out successfully."
}
```
