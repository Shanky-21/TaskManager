```markdown
# Task Manager API

A Django-based Task Management System with REST API support. This system allows users to create tasks, assign them to multiple users, and track individual progress for each assignee.

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
cd TaskManager
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

## API Endpoints

### Authentication
- `POST /api/token/`: Obtain JWT token
  ```bash
  curl -X POST http://localhost:8000/api/token/ \
       -H "Content-Type: application/json" \
       -d '{"username": "your_username", "password": "your_password"}'
  ```

### Tasks
- `GET /api/tasks/`: List all tasks
- `POST /api/tasks/`: Create a new task
  ```bash
  curl -X POST http://localhost:8000/api/tasks/ \
       -H "Authorization: Bearer your_token" \
       -H "Content-Type: application/json" \
       -d '{
             "title": "Task Title",
             "description": "Task Description",
             "assign_to": [
                 {"user_id": 1, "status": "pending"}
             ]
           }'
  ```
- `GET /api/tasks/{uuid}/`: Get task details
- `PUT /api/tasks/{uuid}/`: Update task
- `DELETE /api/tasks/{uuid}/`: Delete task
- `GET /api/tasks/my_tasks/`: Get current user's tasks

### Users
- `GET /api/users/me/`: Get current user profile
- `POST /api/users/`: Create new user

## Models

### UserProfile
- Extended user information
- Fields: phone, address, date_of_birth

### Task
- Basic task information
- Fields: title, description, created_by

### UserTask
- Maps users to tasks with individual status
- Fields: user, task, status (pending/in_progress/completed)

## Testing API

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

## Requirements
```
django
djangorestframework
djangorestframework-simplejwt
psycopg2-binary
python-dotenv
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
```
