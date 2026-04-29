# CONTRIBUTING

Gracias por tu interés en contribuir al proyecto **Idea Evolution Engine**. Este documento te guiará a través de los pasos necesarios para configurar el entorno de desarrollo y ejecutar la versión actual del proyecto.

---

## 🏗️ Arquitectura del proyecto

```text
idea-evolution-engine/
│
├── backend/              # API (FastAPI)
│   └── app/
│       ├── api/          # Rutas versionadas (/api/v1)
│       ├── shared/       # Configuración central (settings)
│       └── main.py       # Punto de entrada
│
├── frontend/             # Aplicación web (React + Vite)
│   └── src/
│       ├── features/     # Módulos por funcionalidad
│       ├── hooks/        # Lógica del flujo (useIdeaFlow)
│       ├── services/     # Comunicación con backend
│       ├── config/       # Configuración de entorno
│       └── shared/       # Utilidades comunes
│
└── README.md
```

---

## ⚙️ Requisitos

Antes de ejecutar el proyecto necesitas:

### Backend

* Python 3.10+
* pip
* sqlite

### Frontend

* Node.js 18+
* npm

### Modelo de IA (Ollama)

* [Ollama](https://ollama.com/download) instalado y corriendo
* Descarga **uno** de los dos perfiles según tu hardware:

| Perfil | Modelo | VRAM mínima | Calidad | Comando |
|---|---|---|---|---|
| `capable` (recomendado) | llama3.1:latest | ~17 GB | Máxima | `ollama pull llama3.1` |
| `fast` | qwen2.5 | ~5 GB | Buena | `ollama pull qwen2.5` |

El perfil se selecciona con `MODEL_PROFILE=capable` o `MODEL_PROFILE=fast` en el `.env`.

---

## 🚀 Instalación y ejecución (PASO A PASO)

### Clonar repositorio

```bash
git clone https://github.com/TU_USUARIO/idea-evolution-engine.git
cd idea-evolution-engine
```

---

## 🔧 BACKEND (NUEVA TERMINAL)

### 1. Ir al backend

```bash
cd backend
```

---

### 2. Crear el archivo `.env`

Copia el archivo de ejemplo incluido en el repo:

```bash
cp .env.example .env
```

O crea el `.env` manualmente:

```env
APP_NAME="Idea Evolution Engine API"
APP_VERSION=0.1.0
APP_ENV=development
BACKEND_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
DATABASE_NAME=idea_evolution.db
OLLAMA_BASE_URL=http://localhost:11434

# "capable" = llama3.1:latest (mejor calidad, requiere ~17 GB VRAM)
# "fast"    = qwen2.5         (ligero, funciona con CPU o ~5 GB VRAM)
MODEL_PROFILE=capable
```

---

### 3. Crear entorno virtual

```bash
python -m venv .venv
```

---

### 4. Activar entorno virtual

#### Windows

```bash
.venv\Scripts\activate
```

#### Mac/Linux

```bash
source .venv/bin/activate
```

---

### 5. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 6. Ejecutar backend

```bash
uvicorn app.main:app --reload
```

---

## 💻 FRONTEND (NUEVA TERMINAL)

### 1. Ir al frontend

```bash
cd frontend
```

---

### 2. Crear el archivo `.env`

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

---

### 3. Instalar dependencias

```bash
npm install
```

---

### 4. Ejecutar frontend

```bash
npm run dev
```

---

### 5. Abrir en navegador

```text
http://localhost:5173/
```
