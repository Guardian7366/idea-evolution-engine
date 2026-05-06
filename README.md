# 🚀 Idea Evolution Engine

**Idea Evolution Engine** is an AI-powered creative thinking system designed to transform vague initial ideas into clear, structured, comparable, and evolved proposals.

---

## 🧠 Description

This platform guides users through a structured creative workflow instead of generating a single AI output.

Flow:

1. Create session
2. Register idea
3. Generate variants
4. Select direction
5. Apply transformations
6. Analyze perspectives
7. Compare versions
8. Generate final synthesis

---

## ❗ Problem It Solves

Most AI tools follow:

input → single output

This causes:

- Loss of traceability
- No structured evolution
- No comparison between alternatives
- No version history
- Weak creative control

---

## ✅ Solution

This system introduces:

idea → variants → selection → evolution → analysis → synthesis

Which enables:

- Iterative thinking
- Version control
- Multi-perspective analysis
- Structured outputs
- Better decision-making

---

## 📌 Project Status

- ✅ Full MVP completed
- ✅ Backend + Frontend connected
- ✅ Ollama integration working
- ✅ Mock mode available
- ✅ Language system (ES / EN / AUTO)
- ✅ Versioning system stable
- ✅ Security layer implemented
- ✅ Frontend persistence after refresh
- ✅ Production build ready

---

## 🧱 Project Architecture

The project is divided into two main applications:

idea-evolution-engine2/
├── backend/   → FastAPI API, business logic, persistence, AI providers
├── frontend/  → React + TypeScript + Vite user interface
├── docs/      → Project documentation and architecture references
└── README.md

---

## 🧩 Backend Architecture

The backend follows a modular clean architecture approach.

backend/app/
├── api/
│   ├── deps.py                 → Dependency injection for services and providers
│   ├── security.py             → API security utilities such as rate limiting
│   └── v1/
│       ├── router.py           → Main API v1 router
│       └── endpoints/          → HTTP endpoints grouped by feature
│           ├── analysis.py
│           ├── ideas.py
│           ├── sessions.py
│           ├── synthesis.py
│           └── versions.py
│
├── application/
│   ├── dto/                    → Request and response schemas
│   └── services/               → Application use cases and orchestration logic
│
├── domain/
│   ├── entities/               → Core domain entities
│   ├── repositories/           → Repository contracts/interfaces
│   ├── rules/                  → Business validation rules
│   └── value_objects/          → Domain value objects and enums
│
├── infrastructure/
│   ├── ai/                     → AI clients, prompts, mappers and providers
│   ├── persistence/            → Database setup and SQLAlchemy models
│   └── repositories/           → SQLite repository implementations
│
├── shared/
│   ├── config/                 → Environment settings
│   ├── errors/                 → Application error hierarchy
│   └── utils/                  → Shared utilities
│
└── main.py                     → FastAPI application factory and middleware setup

---

## 🧠 Backend Layer Responsibilities

### API Layer

Responsible for exposing HTTP endpoints and connecting requests to application services.

Path:

backend/app/api/

Main responsibilities:

- Define API routes
- Inject dependencies
- Apply API-level protection
- Expose versioned endpoints
- Keep controllers thin and simple

---

### Application Layer

Responsible for coordinating the main use cases of the system.

Path:

backend/app/application/

Main responsibilities:

- Create sessions
- Register ideas
- Generate variants
- Select variants
- Transform versions
- Analyze perspectives
- Compare versions
- Generate final synthesis
- Convert domain entities into response DTOs

---

### Domain Layer

Responsible for the core business model of the application.

Path:

backend/app/domain/

Main responsibilities:

- Define core entities
- Define business rules
- Define repository contracts
- Protect domain consistency
- Keep business logic independent from frameworks

---

### Infrastructure Layer

Responsible for external and technical implementations.

Path:

backend/app/infrastructure/

Main responsibilities:

- SQLite persistence
- SQLAlchemy models
- Repository implementations
- Ollama integration
- Mock AI provider
- AI prompt builders
- AI response mappers

---

## ⚛️ Frontend Architecture

The frontend is organized by application features and shared utilities.

frontend/src/
├── app/
│   ├── App.tsx                 → Root app component
│   └── router.tsx              → React Router configuration
│
├── assets/                     → Static frontend assets
│
├── components/
│   ├── background/             → Visual background components
│   ├── navigation/             → Workspace navigation components
│   └── shared/                 → Shared UI components
│
├── config/
│   └── env.ts                  → Frontend environment configuration
│
├── features/
│   ├── analysis/               → Perspective analysis and version comparison
│   ├── idea-input/             → Session and idea input UI
│   ├── session/                → Flow status and language selector panels
│   ├── synthesis/              → Final synthesis UI
│   ├── variants/               → Variant cards and variant list
│   └── versioning/             → Active version, history, graph and transformations
│
├── hooks/
│   └── useIdeaFlow.ts          → Main frontend workflow state hook
│
├── i18n/                       → Translation setup and locales
│
├── layouts/
│   └── MainLayout.tsx          → Main page shell and header
│
├── pages/
│   └── IdeaWorkspacePage.tsx   → Main workspace page
│
├── services/
│   ├── api.ts                  → Axios API client
│   └── idea.service.ts         → API service functions
│
├── shared/
│   └── utils/                  → Shared frontend utilities
│
├── store/
│   └── idea-flow.store.ts      → Initial idea flow state
│
├── styles/
│   └── tailwind.css            → Tailwind CSS entry
│
├── types/
│   └── idea.ts                 → Frontend TypeScript contracts
│
├── index.css                   → Main visual design system
└── main.tsx                    → React application entry point

---

## 🧠 Frontend Layer Responsibilities

### App Layer

Responsible for bootstrapping the React application.

Path:

frontend/src/app/

Main responsibilities:

- Create the main router
- Render the root app
- Connect the app to React Router

---

### Features Layer

Responsible for separating UI logic by product capability.

Path:

frontend/src/features/

Main responsibilities:

- Keep each feature isolated
- Reduce component coupling
- Organize panels by workflow step
- Improve maintainability

---

### Services Layer

Responsible for communication with the backend API.

Path:

frontend/src/services/

Main responsibilities:

- Configure Axios
- Centralize API calls
- Keep endpoints out of UI components
- Preserve frontend/backend contract clarity

---

### Hooks Layer

Responsible for orchestrating frontend workflow state.

Path:

frontend/src/hooks/

Main responsibilities:

- Manage session state
- Manage idea state
- Manage variants
- Manage versions
- Manage loading and error states
- Restore workspace after refresh
- Coordinate calls to frontend services

---

### Shared Utilities Layer

Responsible for reusable helpers.

Path:

frontend/src/shared/utils/

Main responsibilities:

- Workspace localStorage management
- Version graph helpers
- Text helpers
- Workspace slide registry

---

## 🧩 Architecture Summary

Backend:

FastAPI → API Layer → Application Services → Domain → Infrastructure

Frontend:

React Page → Feature Components → Hook State → Services → Backend API

Core design principles:

- Modular code
- Clear separation of responsibilities
- No spaghetti code
- Backend contracts preserved
- Frontend components organized by features
- AI provider isolated from business logic
- Security controls centralized

---

## 🔁 System Workflow (MVP)

The system follows a structured creative process designed to guide users from a vague idea to a fully developed and structured proposal.

Step-by-step flow:

1. Create a session
2. Register an idea
3. Generate idea variants
4. Select one variant
5. Create initial version
6. Apply transformations
7. Compare versions
8. Analyze perspectives
9. Generate final synthesis

---

## 🔄 Detailed Flow Explanation

### 1. Session Creation

The session acts as a container for the creative process.

- Stores the working context
- Groups ideas and versions
- Enables traceability

---

### 2. Idea Registration

User provides:

- Idea title
- Idea description/content

This becomes the base input for the system.

---

### 3. Variant Generation

The system generates exactly 3 variants using AI.

Each variant:

- Maintains the original concept
- Explores a different direction
- Is concise but meaningful

---

### 4. Variant Selection

User selects one variant.

This action:

- Creates the first version
- Marks it as active
- Starts the evolution process

---

### 5. Version System

Each idea evolves through versions.

A version represents:

- A state of the idea
- A transformation result
- A step in the evolution chain

---

### 6. Transformations

Users can apply three types of transformations:

Evolution:

- Expands and deepens the idea

Refinement:

- Improves clarity
- Aligns with specific instructions

Mutation:

- Introduces creative variation
- Keeps the original concept intact

---

### 7. Version History

All versions are stored and visualized.

Features:

- Track evolution
- Compare changes
- Activate any previous version

---

### 8. Version Comparison

Users can compare two versions.

The system:

- Highlights differences
- Explains improvements
- Shows divergence between ideas

---

### 9. Perspective Analysis

Users can analyze a version from a specific perspective.

Examples:

- Business
- Technical
- Educational
- Market viability

---

### 10. Final Synthesis

The system generates a structured output including:

- Summary
- Value proposition
- Target audience
- Structured description
- Next steps

---

## 🌐 Language System

The system supports:

- Spanish (es)
- English (en)
- Auto mode

---

### How Language Works

1. User selects language in UI
2. Frontend sends language in requests
3. Backend resolves language mode
4. AI provider selects correct model
5. Prompts enforce strict language rules
6. Output is validated and normalized

---

### Language Enforcement Rules

- No mixing languages
- Output must be fully consistent
- AI responses follow strict prompt instructions
- Optional rewrite layer ensures compliance

---

## 🧠 AI Provider System

The backend supports two AI providers:

---

### Mock Provider

Used for:

- Testing
- Development without AI
- Faster iteration

Behavior:

- Returns static or simulated responses
- No external dependency required

---

### Ollama Provider

Used for:

- Real AI generation
- Local LLM execution

Features:

- Runs locally
- No external API cost
- Supports custom models
- Supports language-specific models

---

### Model Strategy

Three models are used:

- Default model
- Spanish-enforced model
- English-enforced model

This ensures:

- Language consistency
- Better output quality
- Reduced prompt leakage

---

## 🧪 State Management (Frontend)

The frontend uses a centralized workflow hook:

useIdeaFlow

---

### Responsibilities

- Manage session state
- Manage idea state
- Manage variants
- Manage versions
- Manage active version
- Manage analysis and synthesis
- Handle loading states
- Handle errors
- Persist workspace in localStorage

---

### Workspace Persistence

After refresh:

- Session is restored
- Idea is restored
- Variants are restored
- Versions are restored
- Active version is restored

Not persisted:

- Analysis
- Comparisons
- Synthesis

Reason:

These can be regenerated safely.

---

## 🧩 Design Principles

- Modular architecture
- Clean separation of concerns
- No spaghetti code
- Strong typing (DTOs)
- Backend contracts respected
- AI isolated from business logic
- Deterministic workflow
- Reproducible state

---

## ⚙️ Requirements

Before installing the project, make sure you have:

- Python 3.11+
- Node.js 18+
- npm
- Git
- Ollama (optional but recommended)

---

# ⚙️ Complete Installation Guide

This guide explains how to install and run the project from zero after cloning the repository.

The project requires running two applications:

- Backend: FastAPI API
- Frontend: React + Vite application

Optional:

- Ollama for real local AI generation
- Mock mode for testing without Ollama

---

## 1. Clone the Repository

Open a terminal and run:

git clone <your-repository-url>
cd idea-evolution-engine2

Example:

git clone https://github.com/your-username/idea-evolution-engine2.git
cd idea-evolution-engine2

---

## 2. Verify Project Structure

After cloning, you should see:

idea-evolution-engine2/
├── backend/
├── frontend/
├── docs/
├── .gitignore
└── README.md

---

# 🐍 Backend Installation

## 3. Enter Backend Folder

cd backend

---

## 4. Create Python Virtual Environment

Windows PowerShell:

python -m venv .venv

Activate it:

.venv\Scripts\Activate.ps1

If PowerShell blocks script execution, run:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Then activate again:

.venv\Scripts\Activate.ps1

Windows CMD:

python -m venv .venv
.venv\Scripts\activate.bat

macOS / Linux:

python3 -m venv .venv
source .venv/bin/activate

---

## 5. Install Backend Dependencies

pip install -r requirements.txt

Expected dependencies include:

- fastapi
- uvicorn
- pydantic
- pydantic-settings
- sqlalchemy
- httpx
- pytest

---

## 6. Create Backend Environment File

Inside the backend folder, create:

.env

Full recommended local configuration:

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

---

## 7. Choose AI Provider Mode

The backend supports two modes:

Mock mode:

LLM_PROVIDER=mock

Use this if:

- You want to test quickly
- You do not have Ollama installed
- You want predictable simulated AI responses

Ollama mode:

LLM_PROVIDER=ollama

Use this if:

- You want real AI-generated responses
- You have Ollama installed
- You created the required models

For first-time installation, it is recommended to start with:

LLM_PROVIDER=mock

---

## 8. Run Backend

From the backend folder:

uvicorn app.main:app --reload

Expected output:

INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.

Open backend root:

http://127.0.0.1:8000

Open health endpoint:

http://127.0.0.1:8000/health

Open API documentation:

http://127.0.0.1:8000/docs

---

# 🤖 Ollama Installation and Setup

This section is required only if you want to use real local AI generation.

If you are using mock mode, you can skip this section.

---

## 9. Install Ollama

Download Ollama from:

https://ollama.com

Install it according to your operating system.

---

## 10. Verify Ollama Installation

Run:

ollama list

If Ollama is installed correctly, the command should execute without errors.

---

## 11. Pull Base Model

Run:

ollama pull qwen2.5:3b

This downloads the base model used by the project.

---

## 12. Create Spanish-Enforced Model

The project includes this file:

backend/ollama_models/Modelfile.es

From the project root, run:

ollama create qwen2.5:3b-enforce-es -f backend/ollama_models/Modelfile.es

---

## 13. Create English-Enforced Model

The project includes this file:

backend/ollama_models/Modelfile.en

From the project root, run:

ollama create qwen2.5:3b-enforce-en -f backend/ollama_models/Modelfile.en

---

## 14. Verify Ollama Models

Run:

ollama list

You should see:

qwen2.5:3b
qwen2.5:3b-enforce-es
qwen2.5:3b-enforce-en

---

## 15. Test Ollama API Manually

PowerShell:

Invoke-RestMethod -Uri "http://localhost:11434/api/generate" `
-Method Post `
-ContentType "application/json" `
-Body '{"model":"qwen2.5:3b","prompt":"Say OK","stream":false}'

curl:

curl http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5:3b","prompt":"Say OK","stream":false}'

Expected result:

The response should include generated text from the model.

---

## 16. Enable Ollama Mode

In backend/.env, change:

LLM_PROVIDER=mock

to:

LLM_PROVIDER=ollama

Restart backend:

uvicorn app.main:app --reload

---

# ⚛️ Frontend Installation

## 17. Open a New Terminal

Keep backend running in the first terminal.

Open a second terminal from the project root.

---

## 18. Enter Frontend Folder

cd frontend

If you are inside backend, use:

cd ../frontend

---

## 19. Install Frontend Dependencies

npm install

This installs:

- React
- TypeScript
- Vite
- Tailwind CSS
- Axios
- React Router
- React i18next
- React Flow
- Dagre

---

## 20. Create Frontend Environment File

Inside the frontend folder, create:

.env

Recommended content:

VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1

Important:

Do not place secrets inside VITE_* variables.

Anything prefixed with VITE_ is exposed to the browser.

If frontend/.env does not exist, the app uses this fallback:

http://127.0.0.1:8000/api/v1

---

## 21. Run Frontend

From the frontend folder:

npm run dev

Expected output:

VITE ready
Local: http://127.0.0.1:5173/

Open:

http://127.0.0.1:5173/

---

# 🚀 Running the Full Project Locally

You need two terminals.

---

## Terminal 1: Backend

cd backend
.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload

Backend runs at:

http://127.0.0.1:8000

---

## Terminal 2: Frontend

cd frontend
npm run dev

Frontend runs at:

http://127.0.0.1:5173/

---

# ✅ First Run Checklist

After opening the frontend:

1. Create a session
2. Register an idea
3. Generate variants
4. Select a variant
5. Apply a transformation
6. Analyze a perspective
7. Compare versions
8. Generate final synthesis
9. Refresh the page
10. Confirm session, idea, variants and versions are restored

---

# 🧪 Recommended Test Inputs

Session title:

Proyecto QA Seguridad

Idea title:

Idea principal

Idea content:

Una plataforma que ayuda a estudiantes a transformar ideas vagas en proyectos estructurados mediante variantes, evolución, análisis y síntesis final.

Refinement instruction:

Haz la idea más clara para un público universitario y explica mejor su utilidad académica.

Perspective:

Viabilidad técnica

Expected result:

- Session is created
- Idea is registered
- 3 variants are generated
- A version is created after selecting a variant
- Transformations create new versions
- Analysis generates a useful response
- Comparison works between two versions
- Final synthesis contains all expected sections

---

# 🏗️ Production Build

## 22. Build Frontend

cd frontend
npm run build

Expected result:

dist/ folder is generated.

---

## 23. Preview Production Build

npm run preview

Open:

http://127.0.0.1:4173/

Expected result:

The production build works correctly.

---

# 🧹 Clean Local Database

The SQLite database is generated automatically.

Default file:

backend/app.db

To reset local data:

1. Stop backend
2. Delete backend/app.db
3. Restart backend

The database tables will be recreated automatically.

---

# 🧯 Common Installation Issues

## Backend does not start

Check that virtual environment is active:

.venv\Scripts\Activate.ps1

Reinstall dependencies:

pip install -r requirements.txt

Run again:

uvicorn app.main:app --reload

---

## Frontend cannot connect to backend

Check backend health:

http://127.0.0.1:8000/health

Check frontend .env:

VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1

Check backend .env:

BACKEND_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

---

## CORS error

Make sure the frontend is running on one of these origins:

http://localhost:5173
http://127.0.0.1:5173

Make sure both are listed in:

BACKEND_CORS_ORIGINS

---

## Ollama does not respond

Check Ollama:

ollama list

Pull base model:

ollama pull qwen2.5:3b

Test Ollama API:

curl http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5:3b","prompt":"Say OK","stream":false}'

---

## AI responses use the wrong language

Check backend .env:

OLLAMA_MODEL_ES=qwen2.5:3b-enforce-es
OLLAMA_MODEL_EN=qwen2.5:3b-enforce-en

Check models:

ollama list

Check frontend language selector:

ES / EN / AUTO

Restart backend after changing .env.

---

## Rate limit triggers too quickly

Default:

RATE_LIMIT_REQUESTS=120
RATE_LIMIT_WINDOW_SECONDS=60

For development, you can temporarily disable it:

RATE_LIMIT_ENABLED=False

Then restart backend.

---

# 📦 Environment Variables Summary

Backend:

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

Frontend:

VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1

---
