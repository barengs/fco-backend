# Fish Capture Optimization API Documentation

## User Management

### 1. User Registration

**Endpoint:** `POST /api/users/register/`

Register a new user (ship owner, captain, or admin).

#### Request Body

```json
{
  "username": "string",
  "email": "string",
  "user_type": "ship_owner|captain|admin",
  "ship_registration_number": "string (required for ship_owner and captain)",
  "phone_number": "string (optional)",
  "password": "string",
  "password_confirm": "string"
}
```

#### Response

```json
{
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "user_type": "string",
    "ship_registration_number": "string",
    "phone_number": "string",
    "date_joined": "datetime"
  },
  "token": "string",
  "message": "User registered successfully"
}
```

### 2. User Login

**Endpoint:** `POST /api/users/login/`

Login with username or ship registration number.

#### Request Body

```json
{
  "username": "string (can be username or ship_registration_number)",
  "password": "string"
}
```

#### Response

```json
{
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "user_type": "string",
    "ship_registration_number": "string",
    "phone_number": "string",
    "date_joined": "datetime"
  },
  "token": "string",
  "message": "Login successful"
}
```

### 3. User Logout

**Endpoint:** `POST /api/users/logout/`

Logout the current user (requires authentication).

#### Response

```json
{
  "message": "Logout successful"
}
```

### 4. Get User Profile

**Endpoint:** `GET /api/users/profile/`

Get the current user's profile (requires authentication).

#### Response

```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "user_type": "string",
  "ship_registration_number": "string",
  "phone_number": "string",
  "date_joined": "datetime"
}
```

### 5. Update User Profile

**Endpoint:** `PUT /api/users/profile/update/`

Update the current user's profile (requires authentication).

#### Request Body

```json
{
  "first_name": "string (optional)",
  "last_name": "string (optional)",
  "email": "string (optional)",
  "phone_number": "string (optional)"
}
```

#### Response

```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "user_type": "string",
  "ship_registration_number": "string",
  "phone_number": "string",
  "date_joined": "datetime"
}
```

## Authentication

All endpoints except registration and login require token authentication. Include the Authorization header in your requests:

```
Authorization: Token <your_token_here>
```
