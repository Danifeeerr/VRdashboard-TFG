# TFG API

> **Language / Idioma:** English | [Español](README.es.md)

REST API developed as part of a university Final Degree Project (TFG). It provides access and management of the system's database, acting as the shared backend for the other two applications in the project.

## TFG Projects

This repository is one of three components that make up the TFG:

| Project | Description | Repository |
|---|---|---|
| **API** (this repo) | REST backend, database management | — |
| **Desktop Application** | Administration client | [View repository](https://github.com/Danifeeerr/VRdashboard-TFG) |
| **Virtual Reality Application** | Main training application | [View repository](https://github.com/Danifeeerr/occupational-safety-TFG) |

---

## Tech Stack

- **Python** + **FastAPI**
- **PostgreSQL** with **SQLAlchemy**
- **Pydantic v2** for schema validation
- **JWT** for authentication
- **Argon2** for password hashing

## Prerequisites

- Python 3.10+
- PostgreSQL running and accessible

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd TFGAPI

# Create virtual environment and install dependencies
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux / macOS

pip install -r requirements.txt
```

## Configuration

Create a `.env` file at the root of the project:

```env
dburl=postgresql://user:password@host:port/db_name
skey=your_jwt_secret_key
```

## Running

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.
Interactive documentation (Swagger UI) is auto-generated at `http://localhost:8000/docs`.

---

## Endpoints

### Authentication

| Method | Route | Description |
|---|---|---|
| `POST` | `/login` | Log in and receive a JWT token |

### Users

| Method | Route | Description |
|---|---|---|
| `GET` | `/users` | List all users |
| `GET` | `/user` | Get the current user from a token |
| `GET` | `/user/{id}` | Get a user by ID *(admin only)* |
| `POST` | `/users/new` | Create a new user |
| `POST` | `/users/update` | Update user data |
| `DELETE` | `/users/delete/{id}` | Delete a user *(admin only)* |

### Trainings

| Method | Route | Description |
|---|---|---|
| `GET` | `/training` | List all trainings |
| `GET` | `/training/{id}` | Get a training by ID |
| `POST` | `/training/new` | Create a new training |
| `POST` | `/training/update` | Update a training |
| `DELETE` | `/training/delete/{id}` | Delete a training |

### Assignations

| Method | Route | Description |
|---|---|---|
| `GET` | `/assignation` | List all assignations |
| `GET` | `/assignation/{userid}` | List assignations for a user *(admin only)* |
| `POST` | `/assignation/new` | Assign a training to a user *(admin only)* |
| `POST` | `/assignation/update` | Mark an assignation as completed |
| `DELETE` | `/assignation/delete` | Delete an assignation *(admin only)* |

### Attempts

| Method | Route | Description |
|---|---|---|
| `GET` | `/attempt` | Get attempts for a user on a specific training |
| `GET` | `/attempt/user` | Get all attempts for a user |
| `GET` | `/attempt/timestamp` | Get an attempt by user and timestamp |
| `POST` | `/attempt/new` | Register a new attempt |
| `DELETE` | `/attempt/delete` | Delete an attempt |

---

## Data Models

```
users           training        assignation         attempt
─────────────   ────────────    ───────────────     ───────────────
id              id              userid (FK)         userid (FK)
username        name            trainingid (FK)     trainingid (FK)
password_hash   hours           completed           time_spent
admin           error_limit     date                number_errors
                                                    timestamp
```
