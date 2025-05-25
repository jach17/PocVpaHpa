# 🧪 Generador de Microservicios en Python con FastAPI

Este proyecto permite generar servicios en Python estructurados con FastAPI, arquitectura limpia, conexión a base de datos, pruebas unitarias automatizadas y ejemplo de integración con API externa.

---

## 📦 Requisitos Previos

Antes de generar un servicio, asegurate de tener instalado lo siguiente:

- [Node.js (LTS)](https://nodejs.org/es/)
- Yeoman
  ```bash
  npm install -g yo
  ```

- Clonar el generador y enlazarlo:
  ```bash
  cd generator-python/
  npm install
  npm link
  ```

---

## 🚀 Generar un Nuevo Microservicio

1. En la ubicación donde deseas tu microservicio ejecuta el comando:

```bash
yo python
```

2. Se usará el archivo `generators/app/config.json` para establecer:

```json
{
    "name": "repo-entity",
    "external": "api-external"
}
```

Esto generará una carpeta con el nombre `[name]-service`, por ejemplo `users-service`.

---

## 🧪 Pruebas unitarias automatizadas

Una vez generado el proyecto, **las pruebas unitarias automatizadas se ejecutarán automáticamente** como validación inicial del arquetipo.

Si deseas volver a ejecutarlas manualmente, puedes usar el comando desde el `Makefile` incluido en el proyecto:

```bash
poetry run make test_coverage
```

Esto generará los reportes de cobertura (`html` y `xml`) usando las configuraciones definidas en `.coveragerc`.

---

## 📦 Docker y Makefile incluidos

El servicio generado incluirá un archivo `Makefile` con los siguientes comandos útiles:

```makefile
make up            # Levanta el entorno con docker-compose
make rebuild       # Reconstruye contenedores y inicia el entorno
make test_coverage # Ejecuta pruebas con reporte de cobertura
```

Además, puedes iniciar el servicio directamente con Docker:

```bash
docker compose up --build
```

Y verificar la salud del sistema en:

```http
GET http://localhost:9092/health
```

---

## 💡 ¿Qué incluye el arquetipo?

- FastAPI como framework principal
- Arquitectura limpia (Core, Infrastructure)
- Conexión con PostgreSQL
- Endpoints CRUD de ejemplo
- Cliente HTTP hacia API externa (ej: Rick & Morty)
- Pruebas unitarias con Pytest y cobertura
- Configuración para Docker y Makefile

---



# Microservicio ejemplo con FastAPI

## 🚀 Requisitos

- Python 3.8 o superior
- [Poetry](https://python-poetry.org/docs/#installation)
- Docker (opcional, pero recomendado)

---

## 🗂️ Estructura del proyecto

```
project/
├── app/
│   ├── core/
│   │   ├── application/
│   │   │   ├── factories/
│   │   │   └── ports/
│   │   └── domain/
│   │       ├── entities/
│   │       ├── enums/
│   │       └── services/
│   └── infrastructure/
│       ├── adapters/
│       ├── api/
│       │   ├── routers/
│       │   │   └── routers1.py
│       │   ├── schemas/
│       │   └── main.py
│       ├── config/
│       │   └── settings.py
│       ├── database/
│       │   ├── models/
│       │   ├── repositories/
│       │   └── session.py
│       ├── http/
│       │   └── client.py
│       └── shared_resources/
│           ├── constants/
│           ├── http_requests.py
│           └── utils.py
└── test/
    └── unit/
        └── services/
```

---

## 🛠️ Iniciar el Proyecto Localmente

### 1. Instalar dependencias
```bash
poetry lock
poetry install --no-root
```

> ℹ️ `--no-root` evita instalar el proyecto como paquete, útil si solo deseas las dependencias.

### 2. Configurar variables de entorno

```
DB_HOST=localhost
DB_PORT=5431
DB_NAME=dbname
DB_SCHEMA=public
DB_USER=user
DB_PASSWORD=password
EXTERNAL_BASE_URL=https://rickandmortyapi.com/
```

### 3. Ejecutar el servidor

```bash
poetry run uvicorn app.infrastructure.api.main:app --reload
```

---

## ✅ Endpoints disponibles

### 🔍 Verificación de conexión a base de datos

```http
GET - http://localhost:8000/health
```

Respuesta OK:
```json
{
  "status": "OK",
  "timestamp": "...",
  "components": {
    "database": {
      "status": "connected",
      "provider": "postgres"
    }
  }
}
```

### 👥 Operaciones CRUD sobre `users`

**Estructura esperada de tabla:**

```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    telefono TEXT
);
```

- Crear usuario:
```http
POST - /api/v1/users/repository/
```

```json
{ "nombre": "Jonnathan", "telefono": "123456789" }
```

- Obtener todos:
```http
GET - /api/v1/users/repository/
```

- Actualizar usuario (por ID):
```http
POST - /api/v1/users/repository/1
```

```json
{ "nombre": "Jonnathannn", "telefono": "123456789" }
```

### 🌐 Consultar API externa

```http
GET - /api/v1/external/?external_id=1
```

Ejemplo de respuesta:
```json
{
  "id": 1,
  "name": "Rick Sanchez",
  "status": "Alive",
  ...
}
```

---

## 🐳 Uso con Docker

### 1. Construcción de imagen

```bash
docker compose build
```

### 2. Iniciar contenedor

```bash
docker compose up
```

### 3. Verificar servicio

```http
GET - http://localhost:9092/health
```

> Asegurate de usar `DB_HOST=host.docker.internal` si la base de datos está en otro contenedor.

---

## 🧰 Uso con Makefile

Este proyecto incluye un Makefile para facilitar comandos comunes usando Docker y pruebas.

### 🔼 Iniciar el entorno (modo background)
```bash
make up
```

### 🔄 Reconstruir contenedores y iniciar
```bash
make rebuild
```

### 🧪 Ejecutar pruebas con cobertura
```bash
make test_coverage
```

Esto genera reportes de cobertura en formato HTML y XML, usando las configuraciones definidas en `.coveragerc`.


---