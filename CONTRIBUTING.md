# Guía para clonar, instalar y probar Idea Evolution Engine desde cero

Esta guía está pensada para una persona que no conoce el proyecto y quiere ejecutarlo completo en su computadora.

El proyecto tiene dos partes:

1. Backend: API creada con FastAPI
2. Frontend: interfaz creada con React + Vite

También puede usar IA real con Ollama o modo de prueba con Mock.

---

# 1. Requisitos previos

Antes de clonar el proyecto, instala:

- Git
- Python 3.11 o superior
- Node.js 18 o superior
- npm
- Ollama, solo si quieres usar IA real

Para verificar versiones:

git --version
python --version
node --version
npm --version

---

# 2. Clonar el proyecto

Abre una terminal en la carpeta donde quieras guardar el proyecto.

Ejecuta:

git clone <URL_DEL_REPOSITORIO>

Después entra a la carpeta:

cd idea-evolution-engine2

La estructura debería verse así:

idea-evolution-engine2/
├── backend/
├── frontend/
├── docs/
└── README.md

---

# 3. Configurar el backend

Entra a la carpeta backend:

cd backend

Crea un entorno virtual de Python:

python -m venv .venv

Activa el entorno virtual en Windows PowerShell:

.venv\Scripts\Activate.ps1

Si PowerShell no permite activar el entorno, ejecuta:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Luego intenta activar otra vez:

.venv\Scripts\Activate.ps1

Instala las dependencias:

pip install -r requirements.txt

---

# 4. Crear archivo .env del backend

Dentro de la carpeta backend, crea un archivo llamado:

.env

Pega este contenido:

APP_NAME=Idea Evolution Engine API
APP_ENV=development
APP_DEBUG=True

APP_HOST=127.0.0.1
APP_PORT=8000
API_V1_PREFIX=/api/v1

BACKEND_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

SECURITY_HEADERS_ENABLED=True
TRUSTED_HOSTS=127.0.0.1,localhost

RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=120
RATE_LIMIT_WINDOW_SECONDS=60

SQLITE_PATH=app.db

LLM_PROVIDER=mock
OLLAMA_BASE_URL=http://localhost:11434

OLLAMA_MODEL_DEFAULT=qwen2.5:3b
OLLAMA_MODEL_ES=qwen2.5:3b-enforce-es
OLLAMA_MODEL_EN=qwen2.5:3b-enforce-en

Para probar rápido, deja:

LLM_PROVIDER=mock

Más adelante puedes cambiarlo a:

LLM_PROVIDER=ollama

---

# 5. Ejecutar el backend

Desde la carpeta backend, con el entorno virtual activo, ejecuta:

uvicorn app.main:app --reload

Si todo está bien, verás algo parecido a:

Uvicorn running on http://127.0.0.1:8000
Application startup complete.

Prueba en el navegador:

http://127.0.0.1:8000/health

También puedes abrir la documentación de la API:

http://127.0.0.1:8000/docs

Deja esta terminal abierta.

---

# 6. Configurar el frontend

Abre una segunda terminal.

Desde la raíz del proyecto entra a frontend:

cd frontend

Instala dependencias:

npm install

---

# 7. Crear archivo .env del frontend

Dentro de la carpeta frontend, crea un archivo llamado:

.env

Pega:

VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1

Importante:

No pongas claves privadas ni secretos en variables VITE_ porque el navegador puede verlas.

---

# 8. Ejecutar el frontend

Desde la carpeta frontend ejecuta:

npm run dev

Si todo está bien, verás:

Local: http://127.0.0.1:5173/

Abre en el navegador:

http://127.0.0.1:5173/

---

# 9. Probar el flujo completo en modo Mock

Con backend y frontend corriendo, prueba esto:

1. Crear sesión

Título sugerido:

Proyecto de prueba

2. Registrar idea

Título:

Idea principal

Contenido:

Una plataforma que ayuda a estudiantes a transformar ideas vagas en proyectos estructurados mediante variantes, evolución, análisis y síntesis final.

3. Generar variantes

Resultado esperado:

Deben aparecer 3 variantes.

4. Seleccionar una variante

Resultado esperado:

Se crea una versión activa.

5. Aplicar evolución

Resultado esperado:

Se crea una nueva versión.

6. Aplicar refinamiento

Instrucción sugerida:

Haz la idea más clara para un público universitario y explica mejor su utilidad académica.

Resultado esperado:

Se crea una versión refinada.

7. Aplicar mutación

Resultado esperado:

Se crea una versión diferente pero relacionada.

8. Analizar perspectiva

Perspectiva sugerida:

Viabilidad técnica

Resultado esperado:

Se genera un análisis.

9. Comparar versiones

Selecciona dos versiones distintas.

Resultado esperado:

Se genera una comparación.

10. Generar síntesis final

Resultado esperado:

Debe aparecer una síntesis estructurada.

---

# 10. Probar persistencia después de refrescar

Presiona F5 o recarga la página.

Resultado esperado:

- Se mantiene la sesión
- Se mantiene el título de la idea
- Se mantiene el contenido de la idea
- Se mantienen las variantes
- Se mantienen las versiones
- Se mantiene la versión activa
- Se mantiene el idioma seleccionado

Nota:

Análisis, comparación y síntesis pueden volver a generarse si no aparecen después del refresh.

---

# 11. Limpiar workspace

Presiona la opción de limpiar workspace.

Resultado esperado:

- Se limpia la sesión visible
- Se limpia la idea visible
- Desaparecen variantes y versiones
- Los inputs vuelven a valores por defecto
- El localStorage queda limpio

---

# 12. Usar IA real con Ollama

Este paso es opcional.

Primero instala Ollama desde:

https://ollama.com

Verifica que funciona:

ollama list

Descarga el modelo base:

ollama pull qwen2.5:3b

Desde la raíz del proyecto, crea el modelo español:

ollama create qwen2.5:3b-enforce-es -f backend/ollama_models/Modelfile.es

Crea el modelo inglés:

ollama create qwen2.5:3b-enforce-en -f backend/ollama_models/Modelfile.en

Verifica:

ollama list

Deben aparecer:

qwen2.5:3b
qwen2.5:3b-enforce-es
qwen2.5:3b-enforce-en

Después cambia en backend/.env:

LLM_PROVIDER=mock

por:

LLM_PROVIDER=ollama

Reinicia el backend.

Ahora el flujo usará IA real local.

---

# 13. Comandos finales para correr todo

Terminal 1:

cd backend
.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload

Terminal 2:

cd frontend
npm run dev

Abrir:

http://127.0.0.1:5173/

---

# 14. Problemas comunes

## El backend no inicia

Verifica que estés en backend:

cd backend

Activa entorno:

.venv\Scripts\Activate.ps1

Instala dependencias:

pip install -r requirements.txt

Ejecuta:

uvicorn app.main:app --reload

---

## El frontend no conecta con backend

Verifica que backend esté corriendo:

http://127.0.0.1:8000/health

Verifica frontend/.env:

VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1

Verifica backend/.env:

BACKEND_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

---

## Ollama no responde

Verifica:

ollama list

Prueba:

ollama pull qwen2.5:3b

---

## Error por rate limit

Si haces muchas acciones muy rápido, puede aparecer:

Too many requests. Please slow down.

Puedes subir el límite en backend/.env:

RATE_LIMIT_REQUESTS=120
RATE_LIMIT_WINDOW_SECONDS=60

O desactivarlo temporalmente:

RATE_LIMIT_ENABLED=False

Reinicia backend después de cambiar .env.

---

# 15. Build de producción

Para probar el frontend en modo producción:

cd frontend
npm run build
npm run preview

Abre:

http://127.0.0.1:4173/

Resultado esperado:

La aplicación debe funcionar igual que en desarrollo.

---

# Resultado final esperado

Si todo salió bien, la persona debería poder:

- Ejecutar backend
- Ejecutar frontend
- Usar modo Mock
- Usar modo Ollama
- Crear sesiones
- Registrar ideas
- Generar variantes
- Crear versiones
- Transformar ideas
- Analizar perspectivas
- Comparar versiones
- Generar síntesis final
- Refrescar sin perder el contexto principal