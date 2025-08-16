# Django Docker PostgreSQL Devcontainer Seed

A **starter template** for Django projects with Docker, PostgreSQL, Dev Containers, asynchronous tasks with Celery, scheduled tasks with Celery Beat, custom Django management commands, and testing with Pytest. Perfect for rapid development and as a base for production-ready applications.  

---

## Table of Contents
1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Tech Stack](#tech-stack)  
4. [Getting Started](#getting-started)  
    - [Prerequisites](#prerequisites)  
    - [Clone & Setup](#clone--setup)  
    - [Run with Devcontainer](#run-with-devcontainer)  
5. [Project Configuration](#project-configuration)  
6. [Usage Guide](#usage-guide)  
    - [CRUD Operations](#crud-operations)  
    - [Asynchronous Tasks with Celery](#asynchronous-tasks-with-celery)  
    - [Scheduled Tasks with Celery Beat](#scheduled-tasks-with-celery-beat)  
    - [Custom Django Commands](#custom-django-commands)  
7. [Testing](#testing)

---

## Project Overview
This project is designed as a **starter template** for Django developers who want a ready-to-use development environment with:  

- Dockerized Django + PostgreSQL  
- Dev Container support for VS Code  
- CRUD operations on an `Item` model  
- Background task processing with Celery  
- Scheduled tasks with Celery Beat  
- Custom Django management commands  
- Test suite using Pytest  

It’s ideal for rapid prototyping, learning, or as a foundation for production projects.  

---

## Features
- Dockerized development environment  
- PostgreSQL database ready out-of-the-box  
- VS Code Dev Container configuration  
- Full CRUD for `Item` model  
- Celery async tasks  
- Celery Beat scheduled tasks  
- Custom Django management commands  
- Pytest test coverage  

---

## Tech Stack
- **Backend:** Django  
- **Database:** PostgreSQL  
- **Task Queue:** Celery  
- **Broker:** Redis  
- **Testing:** Pytest  
- **Containerization:** Docker & Docker Compose  
- **Dev Environment:** VS Code Dev Container  

---

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/get-started)  
- [VS Code](https://code.visualstudio.com/) with **Remote - Containers extension**  
- Optional: Python 3.11+ (for running outside containers)  

---

### Clone & Setup
```bash
git git@github.com:junior92jr/django-docker-postgres-devcontainer-seed.git
cd django-docker-postgres-devcontainer-seed

# Build and run docker containers
docker compose up --build -d

# Apply migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Open the dev server
docker compose exec web python manage.py runserver 0.0.0.0:8000
```

### Run with Devcontainer

Open the project in VS Code.

Click Reopen in Container when prompted.

The dev container comes preconfigured with Python, Docker, and dependencies.

Run Django commands directly inside the container:

```bash
python manage.py runserver
python manage.py test
```

## Project Configuration

### Environment Variables
This project comes with a `.sample_env` file. You can quickly create your local environment file by running:  
```bash
cp .sample_env .env
```
Then, you can adjust the values as needed (database credentials, secret key, Redis URL, etc.).

### Celery Configuration

In settings.py or celery.py:

```bash
CELERY_BROKER_URL = os.environ.get("REDIS_URL")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL")

# Using Django-Celery-Beat
INSTALLED_APPS += [
    'django_celery_beat',
]
```

## Usage Guide
### CRUD Operations
- **Create Item:** via Django Admin or API POST request  
- **Read Items:** via list view or API GET request  
- **Update Item:** via Admin or API PUT/PATCH  
- **Delete Item:** via Admin or API DELETE

### Asynchronous Tasks with Celery
- Start Celery worker:
```bash
docker compose exec web celery -A project_name worker --loglevel=info
```
- Call tasks asynchronously in Django code:
```bash
from items.tasks import example_task
example_task.delay(item_id=1)
```
### Scheduled Tasks with Celery Beat

With **Django-Celery-Beat**, periodic tasks are managed through the **Django admin interface**, so you don’t need to hardcode schedules in your settings.  

1. Go to **http://localhost:8000/admin/**  
2. Navigate to the **Periodic Tasks** section.  
3. Create a new periodic task:
   - **Name:** Daily Item Summary  
   - **Task:** `items.tasks.daily_summary`  
   - **Schedule:** choose a crontab or interval (e.g., every day at 8:00 AM)  
   - **Enabled:** checked  

Start Celery worker and Beat scheduler to process scheduled tasks:
```bash
docker compose exec web celery -A project_name worker --loglevel=info
docker compose exec web celery -A project_name beat --loglevel=info
```
Now your scheduled tasks will automatically run according to the intervals defined in the admin.

### Custom Django Commands

You can create and run custom management commands to perform batch operations, maintenance tasks, or background updates.

Run a custom command:
```bash
docker compose exec web python manage.py <command_name>
```
Example:
```bash
docker compose exec web python manage.py update_items_status
```
- Replace `update_items_status` with the name of your custom command.

- Custom commands are defined in your Django app under `management/commands/` and can include any Python logic you need.

## Testing

Run all tests:
```bash
pytest
```

Verbose output:
```bash
pytest -v
```

Run specific test file or class:

```bash
pytest path/to/test_file.py
pytest path/to/test_file.py::TestClassName
pytest path/to/test_file.py::TestClassName::test_method_name
```