# Task Management System

A Django-based task management system with user authentication and task assignment capabilities.

## Features

- User Authentication (Signup/Login)
- Task Dashboard
- Task Creation and Assignment
- User-based Task Filtering
- Multiple User Assignment Support

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
- Copy `.env.example` to `.env`
- Update the database credentials and other settings in `.env`

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- POST /api/auth/register/ - User registration
- POST /api/auth/login/ - User login
- POST /api/auth/logout/ - User logout

### Tasks
- GET /api/tasks/ - List all tasks
- POST /api/tasks/ - Create a new task
- GET /api/tasks/{id}/ - Get task details
- PUT /api/tasks/{id}/ - Update task
- DELETE /api/tasks/{id}/ - Delete task
- GET /api/tasks/user/{user_id}/ - Get tasks for specific user 