# Fish Chain Optimization API Documentation

## User Management

### 1. User Registration

**Endpoint:** `POST /api/users/register/`

Register a new user with a specific role (ship owner, captain, or admin).

#### Request Body

```json
{
  "username": "string",
  "email": "string",
  "role": "ship_owner|captain|admin",
  "phone_number": "string (optional)",
  "password": "string",
  "password_confirm": "string",
  // Role-specific fields
  // For ship_owner:
  "owner_type": "individual|company (optional, default: individual)",
  "company_name": "string (required for company owners)",
  "tax_id": "string (optional)",
  // For captain:
  "license_number": "string (required for captains)",
  "years_of_experience": "integer (optional)",
  // For admin:
  "employee_id": "string (required for admins)",
  "department": "string (optional)",
  "position": "string (optional)"
}
```

#### Response

```json
{
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "phone_number": "string",
    "date_joined": "datetime",
    "role_names": ["string"],
    "ship_owner_profile": {
      "id": "integer",
      "owner_type": "individual|company",
      "company_name": "string|null",
      "tax_id": "string|null",
      "address": "string|null",
      "contact_person": "string|null",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  },
  "tokens": {
    "refresh": "string",
    "access": "string"
  },
  "message": "User registered successfully"
}
```

### 2. User Login

**Endpoint:** `POST /api/users/login/`

Login with username and password.

#### Request Body

```json
{
  "username": "string",
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
    "phone_number": "string",
    "date_joined": "datetime",
    "role_names": ["string"],
    "ship_owner_profile": {
      "id": "integer",
      "owner_type": "individual|company",
      "company_name": "string|null",
      "tax_id": "string|null",
      "address": "string|null",
      "contact_person": "string|null",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  },
  "tokens": {
    "refresh": "string",
    "access": "string"
  },
  "message": "Login successful"
}
```

### 3. User Logout

**Endpoint:** `POST /api/users/logout/`

Logout the current user (requires authentication).

#### Request Body

```json
{
  "refresh": "string"
}
```

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
  "phone_number": "string",
  "date_joined": "datetime",
  "role_names": ["string"],
  "ship_owner_profile": {
    "id": "integer",
    "owner_type": "individual|company",
    "company_name": "string|null",
    "tax_id": "string|null",
    "address": "string|null",
    "contact_person": "string|null",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
}
```

### 5. Update User Profile

**Endpoint:** `PUT /api/users/profile/update/`

Update the current user's basic profile (requires authentication).

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
  "phone_number": "string",
  "date_joined": "datetime",
  "role_names": ["string"],
  "ship_owner_profile": {
    "id": "integer",
    "owner_type": "individual|company",
    "company_name": "string|null",
    "tax_id": "string|null",
    "address": "string|null",
    "contact_person": "string|null",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
}
```

### 6. Update Role-Specific Profile

**Endpoint:** `PUT /api/users/profile/ship-owner/update/`

Update the current user's ship owner profile (requires authentication and ship_owner role).

#### Request Body

```json
{
  "owner_type": "individual|company",
  "company_name": "string",
  "tax_id": "string",
  "address": "string",
  "contact_person": "string"
}
```

#### Response

```json
{
  "id": "integer",
  "owner_type": "individual|company",
  "company_name": "string|null",
  "tax_id": "string|null",
  "address": "string|null",
  "contact_person": "string|null",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Authentication

All endpoints except registration and login require JWT token authentication. Include the Authorization header in your requests:

```
Authorization: Bearer <your_access_token_here>
```
