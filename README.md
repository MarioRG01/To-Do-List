# TO-DO API

Una API RESTful de lista de pendientes (To-Do List) construida con:

- **Python 3.11.9**  
- **SQLite** como base de datos  
- **SQLAlchemy** para el ORM  
- **FastAPI** como framework web  
- **Uvicorn** para servir la app  
- **APScheduler** para limpieza automática de tareas completadas

## Requisitos

- Python 3.11.9  
- VS Code 
- Git

## Instalación
# Clona el repositorio y entra en él
git clone https://github.com/tu-usuario/To-Do-List.git

cd To-Do-List

## Variables de entorno

Crea un archivo .env en la raíz del proyecto con las siguientes variables:
DATABASE_URL=sqlite:///./todo.db

SECRET_KEY=tu_super_secreto

# Crea y activa el entorno virtual
python3.11 -m venv .venv
.venv\Scripts\activate.bat     # Windows

# Instala las dependencias
tpip install -r requirements.txt

# Correr server
uvicorn app.main:app --reload

## Estructura del proyecto
To-Do-List/
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ config.py
│  ├─ db/
│  │  ├─ base.py
│  │  ├─ models.py
│  │  └─ crud.py
│  ├─ auth/
│  │  ├─ security.py
│  │  └─ dependencies.py
│  ├─ routers/
│  │  ├─ auth.py
│  │  └─ tasks.py
│  └─ background/
│     └─ cleaner.py
├─ alembic/
│  └─ versions/
├─ requirements.txt
├─ postman_collection.json
├─ README.md
└─ .gitignore

## Configuración de la base de datos y migraciones

Inicializa Alembic:
alembic init alembic

En alembic.ini, ajusta:
sqlalchemy.url = sqlite:///./todo.db

En alembic/env.py, apunta tu metadata:
from app.config import DATABASE_URL
from app.db.base import metadata
config.set_main_option("sqlalchemy.url", DATABASE_URL)
target_metadata = metadata

Genera y aplica la migración:
alembic revision --autogenerate -m "Create users and tasks tables"
alembic upgrade head

## Autenticación JWT

Implementa:
POST /register → Registro de usuario.
POST /login → Devuelve JWT.

## Uso de Postman

Importa postman_collection.json.

Crea un entorno TodoAPI con:
base_url → http://127.0.0.1:8000
token → (vacío inicialmente)

Register (POST {{base_url}}/register)

Login (POST {{base_url}}/login) y captura el token:
let json = pm.response.json();
if (json.access_token) pm.environment.set("token", json.access_token);

Tareas:
Crear (POST {{base_url}}/tasks) con Authorization: Bearer {{token}}.
Listar (GET {{base_url}}/tasks).
Completar (PATCH {{base_url}}/tasks/{id}).

## Limpieza automática (Background Task)

Se uso APScheduler para ejecutar clean_completed() cada 10 minutos:
scheduler = AsyncIOScheduler()
scheduler.add_job(clean_completed, 'interval', minutes=10)
scheduler.start()

También se puede invocar manualmente:
python - <<EOF
from app.background.cleaner import clean_completed
import asyncio
asyncio.run(clean_completed())
EOF

##  Problemas comunes y soluciones

ModuleNotFoundError: No module named 'aiosqlite' → Instalar aiosqlite.
ImportError: email-validator is not installed → Instalar email-validator.
no such table: users → Añadir metadata.create_all(bind=engine) en startup.
NOT NULL constraint failed: tasks.completed → Incluir completed=False en el insert de create_task()
