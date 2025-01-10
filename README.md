# SpyCatAgency

The **SpyCatAgency** project is an application for managing spy cats, their missions and targets. The system allows you to
track missions, assign cats to missions, manage target statuses and much more
## Technology stack

- **FastAPI** - create RESTful API
- **SQLAlchemy** - for work with DB
- **SQLite** - tour DB, you may choose any one
- **Pydantic** - for validate data
- **Faker** - for creating fake test data

## install

### 1. Clone repository

```commandline
git clone https://github.com/Danil1994/SpyCatAgency.git
```

### 2. Create virtual env and activate it

### 3. Install dependencies
```commandline
pip install -r requirements.txt
pip install "fastapi[standard]"

```

### 4. Launching the project
To launch the FastAPI server, use the command:
```commandline
fastapi dev app/main.py
```
This command also create SQLite DB automatically.

Interactive API docs will be available at  http://127.0.0.1:8000/docs

### Generating Fake Data
To generate fake cats and missions, you can use the create_fake_data.py command. 
This script will create 10-15 fake cats and 5 fake missions:
```commandline
python -m app.create_fake_data
```

## Project structure
```bash
spy-cat-agency/
│
├── app/
│   ├── __init__.py
│   ├── main.py           # main FastAPI route
│   ├── models.py         # DB models (SQLAlchemy)
│   ├── schemas.py        # Pydantic schemas
│   ├── database.py       # Settings and connection to the database
│   ├── create_fake_data.py  # Script for creating fake data
│   ├── crud.py           # CRUD operations with DB
│   └── routers/          # Routers for processing API requests
│       └── cats.py
│       └── missions.py
└── requirements.txt      # List of dependencies

```
## Postman API Collection

You can download the Postman collection to test all API endpoints from the following link:

[Load Postman Collection for SpyCatAgency](https://drive.google.com/file/d/1Ted1asIQleSXcvmYxK0PG5rF-Kln87SP/view?usp=drive_link)

With this collection, you can easily test all API endpoints.