# SpyCatAgency

The **SpyCatAgency** project is an application for managing spy cats, their missions and targets. The system allows you to
track missions, assign cats to missions, manage target statuses and much more
## Стек технологий

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
```
### 5. Set up the database
The project uses SQLite by default, and the database will be automatically created in the project root (if it does not already exist).

Run the command to initialize the database:
```commandline
python -m app.database
```

### 6. Launching the project
To launch the FastAPI server, use the command:
```commandline
fastapi dev main.py
```
Interactive API docs will be available at  http://127.0.0.1:8000/docs

### Generating Fake Data
To generate fake cats and missions, you can use the create_fake_data.py command. 
This script will create 10-15 fake cats and 5 fake missions:
```commandline
python app/create_fake_data.py
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

[Link Postman Collection for SpyCatAgency](https://web.postman.co/workspace/5befd29a-108e-47ad-86a6-caf288b91678/collection/26410240-1985c36c-61aa-4af1-91c8-6853412e6a85)

With this collection, you can easily test all API endpoints.