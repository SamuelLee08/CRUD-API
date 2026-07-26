# Task API

A containerized CRUD API for managing tasks, built with FastAPI and PostgreSQL.

## Running Locally

The entire stack (app + database) starts with one command:

```bash
docker compose up
```

That's it. No manual setup needed.

## Setup

1. Clone the repo:
```bash
git clone https://github.com/SamuelLee08/CRUD-API.git
cd CRUD-API
```

2. Copy the environment template:
```bash
cp .env.example .env
```

3. Start the stack:
```bash
docker compose up
```

The API will be running on `http://localhost:3000`.

## Endpoints

| Method | Endpoint | Purpose | Success Code |
|--------|----------|---------|--------------|
| GET | `/health` | Check the server is running | 200 |
| GET | `/tasks` | List all tasks | 200 |
| GET | `/tasks/{id}` | Get one task | 200 |
| POST | `/tasks` | Create a task | 201 |
| PUT | `/tasks/{id}` | Update a task | 200 |
| DELETE | `/tasks/{id}` | Delete a task | 204 |

## Example curl Commands

Get all tasks:
```bash
curl http://localhost:3000/tasks
```

Create a task:
```bash
curl -X POST http://localhost:3000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk"}'
```

Update a task:
```bash
curl -X PUT http://localhost:3000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated title","done":true}'
```

Delete a task:
```bash
curl -X DELETE http://localhost:3000/tasks/1
```

## Database

PostgreSQL runs in a Docker container. Data persists in the `taskdata` volume.

View the data:
```bash
docker exec -it task-api-db-1 psql -U postgres -d tasks -c "SELECT * FROM tasks;"
```

## Tech Stack

- **FastAPI** — Web framework
- **PostgreSQL** — Database  
- **Docker & Docker Compose** — Containerization
- **psycopg** — Postgres driver for Python
- **Uvicorn** — ASGI server