import axios from 'axios'

import { env } from '../config/env'

// Central API client for backend communication.
export const apiClient = axios.create({
  baseURL: env.apiBaseUrl,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// IMPORTANTE:
// Ollama puede tardar más que una API normal.
// Se aumenta timeout para evitar fallos falsos en frontend.