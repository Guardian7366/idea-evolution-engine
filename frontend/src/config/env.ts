// Centralized frontend environment access.
// This avoids scattering import.meta.env usage across the app.
export const env = {
  apiBaseUrl:
    import.meta.env.VITE_API_BASE_URL,
}
