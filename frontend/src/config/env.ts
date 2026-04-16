// Centralized frontend environment access.
// This avoids scattering import.meta.env usage across the app.
export const env = {
  apiBaseUrl:
    import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1",
}
