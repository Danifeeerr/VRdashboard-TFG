# Aplicación de Escritorio TFG

> **Language / Idioma:** [English](README.md) | Español

Panel de administración desarrollado como parte de un Trabajo de Fin de Grado (TFG). Permite a los administradores gestionar usuarios, entrenamientos y asignaciones, y revisar el historial de intentos registrado por la aplicación VR.

## Proyectos del TFG

Este repositorio es uno de los tres componentes que forman el TFG:

| Proyecto | Descripción | Repositorio |
|---|---|---|
| **API** | Backend REST, gestión de la base de datos | [Ver repositorio](https://github.com/Danifeeerr/TFG-database-API) |
| **Aplicación de escritorio** (este repo) | Cliente de administración | — |
| **Aplicación de Realidad Virtual** | Aplicación principal de entrenamiento | [Ver repositorio](https://github.com/Danifeeerr/occupational-safety-TFG) |

---

## Tecnologías

- **Python** + **PyQt6**
- **requests** para la comunicación HTTP con la API
- **python-dotenv** para la configuración por variables de entorno
- **PyInstaller** para generar un ejecutable independiente

## Requisitos previos

- Python 3.10+
- La API en ejecución y accesible (local o remota)

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd TFG-DesktopApp

# Crear entorno virtual e instalar dependencias
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux / macOS

pip install -r requirements.txt
```

## Configuración

Crea un archivo `.env` en la raíz del proyecto:

```env
API_BASE=http://localhost:8000
```

Establece `API_BASE` con la URL donde está corriendo la API.

## Ejecución

```bash
python main.py
```

## Generar ejecutable (Windows)

```bash
pyinstaller --onefile --windowed --add-data ".env;." main.py
```

El `.exe` resultante se encontrará en la carpeta `dist/`.

---

## Pantallas de la aplicación

### Autenticación

| Pantalla | Descripción |
|---|---|
| **Login** | Inicio de sesión de administrador con usuario y contraseña, devuelve un token JWT |

### Usuarios

| Pantalla | Descripción |
|---|---|
| **Lista de usuarios** | Lista todos los usuarios, con acceso a sus intentos y asignaciones |
| **Nuevo usuario** | Formulario para crear un nuevo usuario (administrador o estándar) |
| **Editar usuario** | Formulario para actualizar nombre, contraseña y rol de administrador |

### Entrenamientos y asignaciones

| Pantalla | Descripción |
|---|---|
| **Asignaciones** | Ver y gestionar las asignaciones de entrenamientos de un usuario |

### Intentos

| Pantalla | Descripción |
|---|---|
| **Historial de intentos** | Lista todos los intentos de un usuario con filtro por fecha, muestra el entrenamiento, tiempo empleado, errores y si fue superado |

---

## Modelos de datos

```
users           training        assignation         attempt
─────────────   ────────────    ───────────────     ───────────────
id              id              userid (FK)         userid (FK)
username        name            trainingid (FK)     trainingid (FK)
password_hash   hours           completed           time_spent
admin           error_limit     date                number_errors
                                                    timestamp
```
