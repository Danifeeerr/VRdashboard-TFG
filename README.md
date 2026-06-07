# TFG Desktop Application

> **Language / Idioma:** English | [Español](README.es.md)

Administration panel developed as part of a university Final Degree Project (TFG). It allows administrators to manage users, trainings and assignments, and to review the attempt history recorded by the VR application.

## TFG Projects

This repository is one of three components that make up the TFG:

| Project | Description | Repository |
|---|---|---|
| **API** | REST backend, database management | [View repository](https://github.com/Danifeeerr/TFG-database-API) |
| **Desktop Application** (this repo) | Administration client | — |
| **Virtual Reality Application** | Main training application | [View repository](https://github.com/Danifeeerr/occupational-safety-TFG) |

---

## Tech Stack

- **Python** + **PyQt6**
- **requests** for HTTP communication with the API
- **python-dotenv** for environment configuration
- **PyInstaller** for building a standalone executable

## Prerequisites

- Python 3.10+
- The API running and accessible (local or remote)

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd TFG-DesktopApp

# Create virtual environment and install dependencies
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux / macOS

pip install -r requirements.txt
```

## Configuration

Create a `.env` file at the root of the project:

```env
API_BASE=http://localhost:8000
```

Set `API_BASE` to the URL where the API is running.

## Running

```bash
python main.py
```

## Building an executable (Windows)

```bash
pyinstaller --onefile --windowed --add-data ".env;." main.py
```

The resulting `.exe` will be placed in the `dist/` folder.

---

## Application Screens

### Authentication

| Screen | Description |
|---|---|
| **Login** | Admin login using username and password, returns a JWT token |

### Users

| Screen | Description |
|---|---|
| **User list** | Lists all users, with access to their attempts and assignments |
| **New user** | Form to create a new user (admin or standard) |
| **Edit user** | Form to update username, password and admin status |

### Trainings & Assignments

| Screen | Description |
|---|---|
| **Assignments** | View and manage training assignments for a user |

### Attempts

| Screen | Description |
|---|---|
| **Attempt history** | Lists all attempts for a user with date filtering, shows training name, time spent, errors and whether it was passed |

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
