# Django Project Setup and Running Guide

This guide will help you set up and run the Django project `taskManagement` with the necessary dependencies.

## Prerequisites

- Python installed on your system
- Pipenv installed (to manage virtual environments and dependencies)

## Steps to Set Up the Project

### 1. Clone the Repository

````bash
# Clone the repository (replace URL with the actual repo link)
git clone <repository-url>

# Navigate to the project directory
cd <repository-folder>

### 2. Set Up a Virtual Environment

Use Pipenv to create and activate a virtual environment:
```bash
# Create and activate the virtual environment
pipenv shell

### 3. Install Dependencies

Install Django and required packages:
```bash
pipenv install django djangorestframework djangorestframework-simplejwt
````

### 4. Create the Django Project

Create a new Django project named `taskManagement`:

````bash
django-admin startproject taskManagement .


### 5. Create Django Apps

Create two apps: `account` and `tasks`:
```bash
python manage.py startapp account
python manage.py startapp tasks

````

### 6. Add Apps to Installed Apps

Edit `taskManagement/settings.py` and add the newly created apps to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...,
    'rest_framework',
    'account',
    'tasks',
]
```

### 7. Apply Migrations

Run the following commands to apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Run the Server

Start the Django development server:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser to see the running project.

### Common Commands for Development

- **Creating superuser:**
  ```bash
  python manage.py createsuperuser
  ```

## API Usage

### 1. Authentication

- **Register**:

  ```http
  POST /account/api/auth/register
  Content-Type: application/json
  {
      "email": "user@example.com",
      "name" : "Example",
      "contact" : 7854125487,
      "password": "password123",
      "password2": "password123"
  }

  ```

- **Login**:
  **Note**: After login, all JWT tokens (`access` and `refresh`) are attached to the response as HttpOnly cookies for secure client-side storage.

  ```http
  POST /account/api/auth/login
  Content-Type: application/json
  {
      "email": "user@example.com",
      "password": "password123"
  }
  ```

### 2. Tasks Management

- **Retrieve All Tasks**:

  ```http
  GET /tasks/task
  Content-Type: application/json

  ```

- **Create Task**:

  ```http
  POST /tasks/task/
  Content-Type: application/json
  X-CSRFToken: <CSRF_TOKEN>

  {

    "title": "Task Example 1",
    "description": "This is a sample task description for demonstration purposes.",
    "status": "in_progress",
    "priority": "medium",
    "due_date": "2024-12-20"

  }
  ```

- **Get Single Task**:

  ```http
  GET /tasks/task/<uuid:id>
  Authorization: Bearer <JWT_ACCESS_TOKEN>
  ```

- **Update Task**:

  ```http
  PUT /tasks/task/
  Content-Type: application/json
  X-CSRFToken: <CSRF_TOKEN>

  {
      "id" : "< task_id >"
      "status": "completed"
  }
  ```

- **Delete Task**:
  ```http
  DELETE /tasks/task/delete/<uuid:id>
  X-CSRFToken: <CSRF_TOKEN>
  ```

### 3. Filter, Sort, and Search Tasks

- **Filter Tasks**:
  ```http
  GET /tasks/filter/<str:filter>/<str:query>/
  ```
  Example:
  ```http
  GET /tasks/filter/status/completed/
  ```

- **Sort Tasks**:
  ```http
  GET /tasks/sort/<str:filter>/
  ```
  Example:
  ```http
  GET /tasks/sort/created_at/
  ```

- **Search Tasks**:
  ```http
  GET /tasks/search/<str:query>/
  ```
  Example:
  ```http
  GET /tasks/search/meeting/
