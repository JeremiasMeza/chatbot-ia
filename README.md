# Chatbot IA

Este proyecto proporciona un frontend de administración para conversar con un modelo de lenguaje y la posibilidad de subir documentos PDF que se indexan para brindar respuestas basadas en su contenido.

## Backend

Un backend sencillo en **FastAPI** expone los siguientes endpoints:

- `GET /models/`: lista de modelos disponibles.
- `POST /upload/`: recibe un PDF y lo indexa en memoria.
- `POST /chat/`: dada una pregunta y un `doc_id` opcional, devuelve el fragmento más relevante del PDF.

Para ejecutar el backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Frontend

El panel de administración hecho con React permite seleccionar un modelo, subir un documento y chatear utilizando ese contexto.

Para ejecutarlo en modo desarrollo:

```bash
cd frontend
npm install
npm run dev
```

Por defecto el frontend se comunica con el backend en `http://localhost:8000`. Puedes cambiarlo definiendo la variable de entorno `VITE_API_URL`.
