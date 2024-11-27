# Simple Token Authentication API

This is a simple project which implements a token authentication system for API resources. It includes endpoints to generate, validate, and revoke tokens, as well as to manage resources.

## Setup Instructions

### Clone the repository:
```bash
git clone https://github.com/hasansajedi/simple_token_manager.git
cd token-auth-api
```
Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate
```

Install the required packages:
```bash
pip install -r requirements.txt
```

Apply migrations:
```bash
python manage.py migrate
```

Start the development server:
```bash
python manage.py runserver
```

## Features

- Secure token generation with encryption support.
- Token validation and revocation.
- Resource management with configurable validity duration.

---

## Endpoints

### 1. Generate Token
**URL:** `/api/v1/token-auth/token/generate/`  
**Method:** `POST`  
**Description:** Generates a token for the provided resource identifier and API key.  

**Curl Example:**
```bash
curl -X POST http://localhost:8000/api/v1/token-auth/token/generate/ \
-d "identifier={YOUR_IDENTIFIER}" \
-d "apikey={YOUR_APIKEY}" \
-H "Content-Type: application/x-www-form-urlencoded"
```

### 2. Validate Token

**URL:** /api/v1/token-auth/token/validate/
**Method:** POST
**Description:** Validates the provided token to check if it is active and not expired.

Curl Example:
```bash
curl -X POST http://localhost:8000/api/v1/token-auth/token/validate/ \
-H "Authorization: Bearer {YOUR_TOKEN}" \
-d "token={YOUR_TOKEN}" \
-H "Content-Type: application/x-www-form-urlencoded"
```

### 3. Revoke Token

**URL:** /api/v1/token-auth/token/revoke/
**Method:** POST
**Description:** Revokes an active token based on the resource's identifier and API key.

Curl Example:
```bash
curl -X POST http://localhost:8000/api/v1/token-auth/token/revoke/ \
-H "Authorization: Bearer {YOUR_TOKEN}" \
-d "identifier={YOUR_IDENTIFIER}" \
-d "apikey={YOUR_APIKEY}" \
-H "Content-Type: application/x-www-form-urlencoded"
```

### 4. Retrieve your resource

**URL:** /api/v1/token-auth/resource/
**Method:** POST
**Description:** Creates a new resource with an associated API key and identifier.

Curl Example:
```bash
curl -X POST http://localhost:8000/api/v1/token-auth/resource/ \ 
-H "Authorization: Bearer {YOUR_TOKEN}" \ 
-H "Content-Type: application/x-www-form-urlencoded"
```