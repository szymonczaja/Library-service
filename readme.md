# Library Management API

This project is a Library Management REST API built with Python, FastAPI, and SQLite.

It supports:
- managing books and members,
- checking out and returning books,
- extending loan due dates,
- searching books by title,
- listing active and overdue loans,
- generating basic library statistics.

The project uses a service layer and repository pattern to separate business logic from data access. It also includes unit tests written with `pytest`.

## Run the project

```bash
pip install fastapi uvicorn pydantic email-validator
uvicorn api:app --reload
```

Open the API docs in your browser:

```text
http://127.0.0.1:8000/docs
```

## Run tests

```bash
pytest library_tests.py
```