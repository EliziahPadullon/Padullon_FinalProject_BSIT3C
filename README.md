# User Authentication API

A Django REST API for user registration, login, and access to protected routes using JWT.

---

## Endpoints

### Register a New User

**POST** `/api/register/`  
**Content-Type:** `application/json`

#### Request Body

```json
{
  "username": "testuser",
  "password": "password123",
  "email": "testuser@gmail.com",
  "name": "Test User"
}


  Success Response:
  Code: 200 OK
    {
      "token": "your.jwt.token.here"
    }

  Error Response:
  Code: 400 Bad Request

    {
      "error": {
        "username": ["Username already exists!"],
        "email": ["Email already exists!"]
      }
    }


### Login a User
   POST http://127.0.0.1:8000/api/login/
   Content-Type: application/json

   Request Body
    {
      "username": "testuser",
      "password": "password123"
    }


  Success Response:
  Code: 200 OK
    {
      "token": "your.jwt.token.here"
    }

  Error Response:
  Code: 400 Bad Request

    {
      "error": "Invalid credentials"
    }

### Access Protected Route
   GET http://127.0.0.1:8000/api/protected/
   
   Headers
   Authorization: Bearer <your_jwt_token_here>

  Success Response:
  Code: 200 OK
    {
      "message": "Hello, testuser! This is a protected route."
    }

  Error Response:
  Code: 400 Bad Request

    {
      "error": "Invalid credentials"
    }

   
   
   
