# Job Board - Filtrador de Trabajos TI

Aplicación para buscar ofertas de trabajo en informática usando la API de Jooble.

## Estructura

```
job-board/
├── backend/              # API FastAPI
│   ├── main.py
│   ├── routers/
│   ├── models/
│   └── services/
├── frontend/             # Interfaz web
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── README.md
```

## Setup

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar API Jooble (opcional)

1. Regístrate gratis en https://es.jooble.org/api/
2. Copia el archivo `.env.example` a `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edita `.env` y añade tu API key:
   ```
   JOBBLE_API_KEY=tu_api_key_aqui
   ```

**Sin API key**: La app funciona con datos mock de prueba.

### 3. Ejecutar

Backend (terminal 1):
```bash
cd backend
uvicorn main:app --reload --port 5000
```

Frontend (terminal 2):
```bash
# Windows
start frontend/index.html

# macOS
open frontend/index.html

# Linux
xdg-open frontend/index.html
```

O simplemente abre `frontend/index.html` en tu navegador.

## Uso

1. Abre http://localhost:5000/docs para ver la documentación de la API
2. Abre `frontend/index.html` en el navegador
3. Usa los filtros para buscar trabajos
4. Haz clic en "Ver oferta" para ir a la oferta original

## Tecnologías

- **Backend**: FastAPI, Pydantic, httpx
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **API**: Jooble (gratuita con registro)
