# 🚀 Idea Evolution Engine

Plataforma web impulsada por inteligencia artificial diseñada para ayudar a los usuarios a transformar ideas iniciales en conceptos más claros, estructurados y útiles mediante un proceso iterativo guiado.

---

## 🧠 Descripción del proyecto

Idea Evolution Engine permite a los usuarios:

* Introducir una idea inicial
* Generar múltiples variantes de esa idea
* Seleccionar una dirección
* Refinar y transformar el concepto
* Comparar versiones
* Analizar la idea desde distintas perspectivas
* Obtener una síntesis final estructurada

> ⚠️ **Importante:**
> Esta versión actual es un **MVP funcional con lógica mock (simulada)**.
> No utiliza IA real ni base de datos todavía.

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

### Frontend

* Node.js 18+
* npm

---

## 🚀 Instalación y ejecución (PASO A PASO)

⚠️ **Sigue este orden exactamente**

---

### 1. Clonar repositorio

```bash
git clone https://github.com/TU_USUARIO/idea-evolution-engine.git
cd idea-evolution-engine
```

---

## 🔧 BACKEND

### 2. Ir al backend

```bash
cd backend
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
pip install fastapi uvicorn pydantic pydantic-settings
```

---

### 6. Configurar variables de entorno

Asegúrate de tener el archivo:

```text
backend/.env
```

Ejemplo:

```env
APP_NAME=Idea Evolution Engine API
APP_VERSION=0.1.0
APP_ENV=development
BACKEND_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

---

### 7. Ejecutar backend

```bash
uvicorn backend.app.main:app --reload
```

---

### ✅ Resultado esperado

Abrir en navegador:

```text
http://127.0.0.1:8000/docs
```

Debes ver la documentación Swagger con todos los endpoints.

---

## 💻 FRONTEND

### 8. Ir al frontend

```bash
cd ../frontend
```

---

### 9. Instalar dependencias

```bash
npm install
```

---

### 10. Configurar variables de entorno

Archivo:

```text
frontend/.env
```

Contenido:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

---

### 11. Ejecutar frontend

```bash
npm run dev
```

---

### ✅ Resultado esperado

Abrir en navegador:

```text
http://localhost:5173/
```

---

## 🧪 Cómo usar la versión actual (V1)

Sigue este flujo dentro de la aplicación:

---

### 1. Escribir una idea

Ejemplo:

```text
A platform that helps people organize their ideas
```

---

### 2. Generar variantes

Click en:

```text
Generate Variants
```

Resultado esperado:

* 3 variantes:

  * Expansion
  * Focus
  * Creative Twist

---

### 3. Seleccionar una variante

Click en:

```text
Select Variant
```

Resultado:

* Se crea **Version 1 activa**

---

### 4. Refinar la versión

Escribir instrucción:

```text
Make the idea clearer and easier to execute for a first MVP.
```

Click en:

```text
Refine Active Version
```

Resultado:

* Se crea **Version 2**
* Con `parent_version_id`

---

### 5. Comparar versiones

Click en:

```text
Compare Versions
```

Resultado:

* Summary
* Strengths A vs B
* Differences
* Recommendation

---

### 6. Explorar perspectiva

Seleccionar:

```text
User Value (o cualquier otra)
```

Click en:

```text
Explore Perspective
```

Resultado:

* Summary
* Observations
* Suggestion

---

### 7. Generar síntesis final

Click en:

```text
Generate Final Synthesis
```

Resultado:

* Title
* Core Concept
* Value Proposition
* Next Step
* Notes

---

## ⚠️ Notas importantes

* Esta versión usa **datos simulados (mock)**
* No hay persistencia (todo se pierde al recargar)
* No hay autenticación
* No hay IA real aún

---

## 🎯 Estado actual del proyecto

✅ Flujo completo funcional (MVP simulado)
✅ Arquitectura modular definida
✅ Integración frontend-backend validada
❌ IA real pendiente
❌ Base de datos pendiente
❌ UX final pendiente

---

## 🧭 Próximos pasos

* Integración con modelos de IA
* Persistencia con base de datos
* Refinamiento de UX/UI
* Escalabilidad del sistema

---

## 👥 Equipo

Proyecto desarrollado de forma colaborativa.
Base técnica inicial construida por el rol Fullstack.

---

## 📄 Licencia

Pendiente de definir.
