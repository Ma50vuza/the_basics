# Todo API Usage Guide

Base URL:  
`https://todo-backend-liyx.onrender.com/api/todo_entries`

---

## Authentication

All todo endpoints require authentication via JWT.  
Obtain a token by registering and logging in, then include it in the `Authorization` header as `Bearer <token>`.

**Note:** Each user can only see, create, update, or delete their own todo items. Items are associated with the user's email address.

### 1. Register

**POST** `/api/register`  
Creates a new user account. Requires password confirmation.

**Request Example:**
```http
POST /api/register
Content-Type: application/json

{
  "username": "your_username",
  "email": "your_email@example.com",
  "password": "your_password",
  "verify_password": "your_password"
}
```

- `username`: Desired username (string, required)
- `email`: User's email address (string, required)
- `password`: Desired password (string, required)
- `verify_password`: Must match `password` (string, required)

**Response Example:**
```json
{
  "message": "Registration successful"
}
```

---

### 2. Login

**POST** `/api/login`  
Authenticates a user and returns a JWT token.

**Request Example:**
```http
POST /api/login
Content-Type: application/json

{
  "email": "your_email@example.com",
  "password": "your_password"
}
```

- `email`: User's email address (string, required)
- `password`: User's password (string, required)

**Response Example:**
```json
{
  "access_token": "<JWT_TOKEN>"
}
```

---

## Todo Endpoints (Require JWT)

Add header to all requests:  
`Authorization: Bearer <JWT_TOKEN>`

### 3. Create a Todo Item

**POST** `/api/todo_entries`  
Creates a new todo item for the authenticated user.

**Request Example:**
```http
POST /api/todo_entries
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "name": "Chocolate Droppa's New Mixtape, buy it"
}
```

- `name`: Name of the todo item (string, required)

**Response Example:**
```json
{
  "id": "68429f9ed9d401b2ad95dee0",
  "name": "Chocolate Droppa's New Mixtape, buy it",
  "time": "2025-06-06T07:58:22.798964"
  // "user_email": "your_email@example.com" (internal, not returned by default)
}
```

---

### 4. Get All Todo Items

**GET** `/api/todo_entries`  
Retrieves all todo items for the authenticated user only.

**Request Example:**
```http
GET /api/todo_entries
Authorization: Bearer <JWT_TOKEN>
```

**Response Example:**
```json
[
  {
    "id": "68416b64898268767422ee25",
    "name": "Buy and Cook groceries for kids and wife "
  },
  {
    "id": "68428816cf37aa4b0ae7916f",
    "name": "Laptop"
  }
]
```

---

### 5. Update a Todo Item

**PUT** `/api/todo_entries/<item_id>`  
Updates the name and/or description of a todo item. Only the owner can update their item.

**Request Example:**
```http
PUT /api/todo_entries/68429f9ed9d401b2ad95dee0
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "name": "Chocolate Droppa's New Mixtape is Dropping tomorrow.",
  "description": "Optional description here."
}
```

- `name`: New name for the todo item (string, optional)
- `description`: Description for the todo item (string, optional)

**Response Example (on success):**
```json
{
  "id": "68429f9ed9d401b2ad95dee0",
  "name": "Chocolate Droppa's New Mixtape is Dropping tomorrow."
}
```

**Response Example (if not found or not authorized):**
```json
{
  "error": "Item not found or not authorized"
}
```

---

### 6. Delete a Todo Item

**DELETE** `/api/todo_entries/<item_id>`  
Deletes a todo item. Only the owner can delete their item.

**Request Example:**
```http
DELETE /api/todo_entries/68429f9ed9d401b2ad95dee0
Authorization: Bearer <JWT_TOKEN>
```

**Response Example (on success):**
```json
{
  "message": "Item delete is successful"
}
```

**Response Example (if not found or not authorized):**
```json
{
  "error": "Item wasnt found or not authorized"
}
```

---

## Notes

- Replace `<item_id>` with the actual `id` of the todo item.
- All requests and responses use JSON format.
- Always include your JWT token in the `Authorization` header for protected endpoints.
- The `description` field is optional and may not be present in all responses.
- Each todo item is associated with the user who created it and is only accessible by that user.