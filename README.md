
# Task Manager API

A Django-based Task Management System with REST API support. This system allows users to create tasks, assign them to multiple users, and track individual progress for each assignee.

## Table of Contents
- [Task Manager API](#task-manager-api)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Project Structure](#project-structure)
  - [API Documentation](#api-documentation)
    - [Authentication APIs](#authentication-apis)
    - [Task APIs](#task-apis)
    - [User APIs](#user-apis)
    - [Error Responses](#error-responses)
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
git clone <repository-url>
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
