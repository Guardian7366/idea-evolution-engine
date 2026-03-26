# AGENTS.md

## Project overview
Monorepo with:
- /backend -> FastAPI backend
- /frontend -> React + Vite + TypeScript frontend

## Setup
Backend:
- cd backend
- pip install -r requirements.txt

Frontend:
- cd frontend
- npm install

## Validation
Frontend:
- cd frontend
- npm run build

Backend:
- cd backend
- python -m compileall app

## Working rules
- Respect existing folder structure
- Do not introduce spaghetti code
- Prefer modular changes
- Keep frontend types aligned with backend DTOs
- Do not rename public API contracts unless explicitly requested
- Before changing code, inspect related files first