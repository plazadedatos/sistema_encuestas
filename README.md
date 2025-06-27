# Sistema de Encuestas

Este proyecto contiene una aplicacion de encuestas dividida en dos partes: un
frontend desarrollado con Next.js y un backend en Python. Sirve como base para
crear y gestionar encuestas de forma sencilla.

## Requisitos previos

- Node.js 18 o superior
- Python 3.9 o superior

## Instalacion y ejecucion

### Frontend

```bash
cd sistema_encuestas_frontend_inicial
npm install
npm run dev
```

Accede a `http://localhost:3000` en tu navegador para ver la interfaz.

### Backend

```bash
cd sistema_encuestas_backend
python -m venv venv
source venv/bin/activate
# instala dependencias si existen
pip install -r requirements.txt 2>/dev/null || true
# ejecuta la aplicacion
python main.py
```

El backend se inicia por defecto en `http://localhost:8000`.

## Estructura del repositorio

- `sistema_encuestas_frontend_inicial/` – Aplicacion cliente con Next.js.
- `sistema_encuestas_backend/` – Codigo del servidor en Python.
