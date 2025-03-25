# Task Manager API

A Django-based Task Management System with REST API support. This system allows users to create tasks, assign them to multiple users, and track individual progress for each assignee.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [API Examples](#api-examples)
  - [Authentication](#authentication)
    - [User Signup](#1-user-signup)
    - [Get JWT Token](#2-get-jwt-token)
  - [Task Operations](#task-operations)
    - [Create Task](#3-create-task)
    - [Get Tasks](#4-get-tasks)
      - [Get Tasks by User](#41-get-tasks-by-user)
      - [Get My Tasks](#42-get-my-tasks)
    - [Update Task Status](#5-update-task-status)
    - [Update Task Details](#6-update-task-details)
    - [Delete Task](#7-delete-task)
      - [Success Case](#success-case)
      - [Error Cases](#error-cases)
- [Database Models](#database-models)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features
- User authentication with JWT
- Task creation and management
- Individual status tracking per user-task
- RESTful API endpoints
- User profile management
- PostgreSQL database integration

## Prerequisites
- Python 3.10+
- PostgreSQL
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone git@github.com:Shanky-21/TaskManager.git
cd task_manager
```

2. Create and activate virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key

# Database settings
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

5. Set up the database:
```bash
# Create PostgreSQL database
createdb task_manager

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure
```
task_manager/
├── task_manager_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── .env
├── manage.py
└── requirements.txt
```

## API Documentation

### Authentication APIs

#### 1. Obtain JWT Token
```bash
POST /api/token/
```
Request:
```json
{
    "username": "testuser",
    "password": "your_password"
}
```
Response:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Task APIs

#### 1. Create Task
```bash
POST /api/tasks/
```
Request:
```json
{
    "title": "Implement User Authentication",
    "description": "Add JWT authentication to the API endpoints",
    "assign_to": [
        {
            "user_id": 1,
            "status": "pending"
        },
        {
            "user_id": 2,
            "status": "in_progress"
        }
    ]
}
```
Response:
```json
{
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Implement User Authentication",
    "description": "Add JWT authentication to the API endpoints",
    "created_at": "2024-03-24T12:00:00Z",
    "updated_at": "2024-03-24T12:00:00Z",
    "created_by": {
        "id": 1,
        "username": "creator_user",
        "email": "creator@example.com",
        "first_name": "Creator",
        "last_name": "User"
    },
    "assignments": [
        {
            "uuid": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
            "user": {
                "id": 1,
                "username": "user1",
                "email": "user1@example.com"
            },
            "status": "pending",
            "assigned_at": "2024-03-24T12:00:00Z"
        }
    ]
}
```

#### 2. Get All Tasks
```bash
GET /api/tasks/
```
Response: List of tasks with assignments

#### 3. Get Task Detail
```bash
GET /api/tasks/{uuid}/
```
Response: Detailed task information

#### 4. Update Task
```bash
PUT /api/tasks/{uuid}/
```
Request: Same as create task
Response: Updated task details

#### 5. Get My Tasks
```bash
GET /api/tasks/my_tasks/
```
Response: List of tasks assigned to current user

### User APIs

#### 1. Create User (Sign Up)
```bash
POST /api/users/
```
Request:
```json
{
    "username": "newuser",
    "password": "secure_password",
    "email": "newuser@example.com",
    "first_name": "New",
    "last_name": "User",
    "phone": "1234567890",
    "address": "123 Street, City",
    "date_of_birth": "1990-01-01"
}
```
Response: User details with profile

#### 2. Get Current User Profile
```bash
GET /api/users/me/
```
Response: Current user's details with profile

### Error Responses

#### 1. Authentication Error
```json
{
    "detail": "Invalid credentials"
}
```

#### 2. Permission Error
```json
{
    "detail": "You do not have permission to perform this action"
}
```

#### 3. Validation Error
```json
{
    "title": ["This field is required"],
    "assign_to": ["Invalid user_id provided"]
}
```

## API Examples

### 1. User Signup

Create a new user account with profile information.

**Curl Command:**
```bash
curl -X POST http://localhost:8000/api/users/ \
     -H "Content-Type: application/json" \
     -d '{
           "username": "testuser2",
           "password": "Test@123",
           "email": "testuser2@example.com",
           "first_name": "Test",
           "last_name": "User",
           "phone": "1234567890",
           "address": "123 Test Street",
           "date_of_birth": "1990-01-01"
         }'
```

**Response:**
```json
{
    "id": 6,
    "username": "testuser2",
    "email": "testuser2@example.com",
    "first_name": "Test",
    "last_name": "User",
    "profile": {
        "uuid": "47f14b27-ec3a-43b4-bff6-70dee3fcedc8",
        "phone": "1234567890",
        "address": "123 Test Street",
        "date_of_birth": "1990-01-01",
        "created_at": "2025-03-25T18:08:14.000446Z",
        "updated_at": "2025-03-25T18:08:14.000471Z"
    }
}
```


### 2. User Authentication (Get JWT Token)

Get JWT access and refresh tokens for authentication.

**Curl Command:**
```bash
curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{
           "username": "testuser2",
           "password": "Test@123"
         }'
```

**Success Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg0...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY..."
}
```

**Error Response (Invalid Credentials):**
```bash
curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{
           "username": "testuser2",
           "password": "wrongpassword"
         }'
```

**Error Response:**
```bash
  {"detail":"No active account found with the given credentials"}%    
```


### 3. Create Task

Create a new task and assign it to users.

**Curl Command:**
```bash
# First, set your token
export TOKEN="your_jwt_token_here"

# Create task
curl -X POST http://localhost:8000/api/tasks/ \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Implement Login Feature",
           "description": "Add JWT authentication to the frontend",
           "assign_to": [
               {
                   "user_id": 6,
                   "status": "pending"
               }
           ]
         }'
```

**Success Response:**
```json
{
    "uuid": "task-uuid-here",
    "title": "Implement Login Feature",
    "description": "Add JWT authentication to the frontend",
    "created_at": "2024-03-25T18:30:00.000Z",
    "updated_at": "2024-03-25T18:30:00.000Z",
    "created_by": {
        "id": 6,
        "username": "testuser2",
        "email": "testuser2@example.com",
        "first_name": "Test",
        "last_name": "User"
    },
    "assignments": [
        {
            "uuid": "assignment-uuid-here",
            "user": {
                "id": 6,
                "username": "testuser2",
                "email": "testuser2@example.com"
            },
            "status": "pending",
            "assigned_at": "2024-03-25T18:30:00.000Z"
        }
    ]
}
```

### 4. Fetch Tasks

#### 4.1 Get All Tasks

Retrieve all tasks in the system.

**Curl Command:**
```bash
curl -X GET http://localhost:8000/api/tasks/ \
     -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "uuid": "task-uuid-here",
            "title": "Implement Login Feature",
            "description": "Add JWT authentication to the frontend",
            "created_at": "2024-03-25T18:30:00.000Z",
            "updated_at": "2024-03-25T18:30:00.000Z",
            "created_by": {
                "id": 6,
                "username": "testuser2"
            },
            "assignments": [
                {
                    "uuid": "assignment-uuid-here",
                    "user": {
                        "id": 6,
                        "username": "testuser2"
                    },
                    "status": "pending",
                    "assigned_at": "2024-03-25T18:30:00.000Z"
                }
            ]
        }
    ]
}
```

#### 4.2 Get My Tasks

Retrieve tasks assigned to the current user.

**Curl Command:**
```bash
curl -X GET http://localhost:8000/api/tasks/my_tasks/ \
     -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
    "count": 1,
    "results": [
        {
            "uuid": "task-uuid-here",
            "title": "Implement Login Feature",
            "description": "Add JWT authentication to the frontend",
            "status": "pending",
            "created_at": "2024-03-25T18:30:00.000Z",
            "updated_at": "2024-03-25T18:30:00.000Z"
        }
    ]
}
```

#### 4.3 Get Specific Task

Retrieve details of a specific task.

**Curl Command:**
```bash
curl -X GET http://localhost:8000/api/tasks/task-uuid/ \
     -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
    "uuid": "task-uuid-here",
    "title": "Implement Login Feature",
    "description": "Add JWT authentication to the frontend",
    "created_at": "2024-03-25T18:30:00.000Z",
    "updated_at": "2024-03-25T18:30:00.000Z",
    "created_by": {
        "id": 6,
        "username": "testuser2",
        "email": "testuser2@example.com",
        "first_name": "Test",
        "last_name": "User"
    },
    "assignments": [
        {
            "uuid": "assignment-uuid-here",
            "user": {
                "id": 6,
                "username": "testuser2",
                "email": "testuser2@example.com"
            },
            "status": "pending",
            "assigned_at": "2024-03-25T18:30:00.000Z"
        }
    ]
}
```

### 6. Update Task

#### 6.1 Update Task Details
Update the basic details of a task (only available to task creator).

**Curl Command:**
```bash
curl -X PUT "http://localhost:8000/api/tasks/b710a557-7412-4b64-812a-f2be7e572b0b/" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Updated Login Feature",
           "description": "Updated description for JWT authentication",
           "assign_to": [
               {
                   "user_id": 6,
                   "status": "in_progress"
               },
               {
                   "user_id": 2,
                   "status": "pending"
               }
           ]
         }'
```

**Success Response (200 OK):**
```json
{
    "uuid": "b710a557-7412-4b64-812a-f2be7e572b0b",
    "title": "Updated Login Feature",
    "description": "Updated description for JWT authentication",
    "created_at": "2025-03-25T18:21:37.166520Z",
    "updated_at": "2025-03-25T18:45:00.166580Z",
    "created_by": {
        "id": 6,
        "username": "testuser2",
        "email": "testuser2@example.com",
        "first_name": "Test",
        "last_name": "User"
    },
    "assignments": [
        {
            "uuid": "56007a53-fe39-4b16-807b-730e0161650b",
            "user": {
                "id": 6,
                "username": "testuser2"
            },
            "status": "in_progress",
            "assigned_at": "2025-03-25T18:21:37.263714Z",
            "updated_at": "2025-03-25T18:45:00.263751Z"
        },
        {
            "uuid": "new-assignment-uuid",
            "user": {
                "id": 2,
                "username": "anotheruser"
            },
            "status": "pending",
            "assigned_at": "2025-03-25T18:45:00.263714Z",
            "updated_at": "2025-03-25T18:45:00.263751Z"
        }
    ]
}
```

#### 6.2 Partial Update (PATCH)
Update specific fields of a task without affecting others.

**Curl Command:**
```bash
curl -X PATCH "http://localhost:8000/api/tasks/b710a557-7412-4b64-812a-f2be7e572b0b/" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Updated Title Only"
         }'
```

**Success Response (200 OK):**
```json
{
    "uuid": "b710a557-7412-4b64-812a-f2be7e572b0b",
    "title": "Updated Title Only",
    "description": "Updated description for JWT authentication",
    "created_at": "2025-03-25T18:21:37.166520Z",
    "updated_at": "2025-03-25T18:46:00.166580Z",
    "created_by": {
        "id": 6,
        "username": "testuser2"
    },
    "assignments": [
        {
            "uuid": "56007a53-fe39-4b16-807b-730e0161650b",
            "user": {
                "id": 6,
                "username": "testuser2"
            },
            "status": "in_progress",
            "assigned_at": "2025-03-25T18:21:37.263714Z",
            "updated_at": "2025-03-25T18:45:00.263751Z"
        }
    ]
}
```

**Error Responses:**

1. Not Task Creator (403 Forbidden):
```json
{
    "detail": "You do not have permission to perform this action."
}
```

2. Invalid Data (400 Bad Request):
```json
{
    "title": ["This field is required."],
    "assign_to": ["Invalid user_id provided"]
}
```

3. Task Not Found (404 Not Found):
```json
{
    "detail": "Not found."
}
```

**Important Notes:**
1. Only the task creator can update task details
2. PUT request requires all fields (title, description, assign_to)
3. PATCH request allows partial updates
4. Existing assignments not included in update will be removed (for PUT)
5. Assignment updates will create new UserTask entries or update existing ones


1. Full update (PUT):
```bash
curl -X PUT "http://localhost:8000/api/tasks/b710a557-7412-4b64-812a-f2be7e572b0b/" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Updated Login Feature",
           "description": "Updated description for JWT authentication",
           "assign_to": [
               {
                   "user_id": 6,
                   "status": "in_progress"
               }
           ]
         }'
```

2. Partial update (PATCH):
```bash
curl -X PATCH "http://localhost:8000/api/tasks/b710a557-7412-4b64-812a-f2be7e572b0b/" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Updated Title Only"
         }'
```

### 7. Delete Task

#### Success Case
First, let's create a task that we'll delete:
```bash
# 1. Create a task
curl -X POST http://localhost:8000/api/tasks/ \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Task to Delete",
           "description": "This task will be deleted",
           "assign_to": [
               {
                   "user_id": 6,
                   "status": "pending"
               }
           ]
         }'
```

Response:
```json
{
    "uuid": "b710a557-7412-4b64-812a-f2be7e572b0b",
    "title": "Task to Delete",
    "description": "This task will be deleted",
    "created_at": "2025-03-25T19:00:00.166520Z",
    "updated_at": "2025-03-25T19:00:00.166580Z",
    "created_by": {
        "id": 6,
        "username": "testuser2"
    },
    "assignments": [
        {
            "uuid": "56007a53-fe39-4b16-807b-730e0161650b",
            "user": {
                "id": 6,
                "username": "testuser2"
            },
            "status": "pending",
            "assigned_at": "2025-03-25T19:00:00.263714Z"
        }
    ]
}
```

Now delete the task:
```bash
# 2. Delete the task
curl -X DELETE "http://localhost:8000/api/tasks/b710a557-7412-4b64-812a-f2be7e572b0b/" \
     -H "Authorization: Bearer $TOKEN"
```

Success Response:
- Status Code: 204 No Content
- No response body

Verify deletion:
```bash
# 3. Try to fetch the deleted task
curl -X GET "http://localhost:8000/api/tasks/b710a557-7412-4b64-812a-f2be7e572b0b/" \
     -H "Authorization: Bearer $TOKEN"
```

Response (404 Not Found):
```json
{
    "detail": "Not found."
}
```

#### Error Cases

1. Trying to delete someone else's task:
```bash
curl -X DELETE "http://localhost:8000/api/tasks/someone-elses-task-uuid/" \
     -H "Authorization: Bearer $TOKEN"
```

Response (403 Forbidden):
```json
{
    "detail": "You can only delete tasks that you created."
}
```

2. Invalid UUID:
```bash
curl -X DELETE "http://localhost:8000/api/tasks/invalid-uuid/" \
     -H "Authorization: Bearer $TOKEN"
```

Response (400 Bad Request):
```json
{
    "detail": "Invalid UUID format"
}
```

3. Task already deleted:
```bash
curl -X DELETE "http://localhost:8000/api/tasks/b710a557-7412-4b64-812a-f2be7e572b0b/" \
     -H "Authorization: Bearer $TOKEN"
```

Response (404 Not Found):
```json
{
    "detail": "Not found."
}
```

**Important Notes:**
- Only the task creator can delete a task
- Deletion is permanent
- All related assignments are also deleted
- Returns 204 on success with no response body
- Requires valid JWT token


## Database Models

### UserProfile
- Extended user information
- Fields: uuid, phone, address, date_of_birth

### Task
- Basic task information
- Fields: uuid, title, description, created_by

### UserTask
- Maps users to tasks with individual status
- Fields: uuid, user, task, status (pending/in_progress/completed)

## Testing

1. Get authentication token:
```bash
curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'
```

2. Save the token:
```bash
export TOKEN="your_token_here"
```

3. Make authenticated requests:
```bash
# List tasks
curl http://localhost:8000/api/tasks/ \
     -H "Authorization: Bearer $TOKEN"

# Create task
curl -X POST http://localhost:8000/api/tasks/ \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Test Task",
           "description": "Description",
           "assign_to": [
               {"user_id": 1, "status": "pending"}
           ]
         }'
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
