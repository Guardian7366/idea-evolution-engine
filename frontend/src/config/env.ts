const apiBaseUrl =
  import.meta.env.VITE_API_BASE_URL?.trim() ||
  "http://127.0.0.1:8000/api/v1";

if (!apiBaseUrl.startsWith("http://") && !apiBaseUrl.startsWith("https://")) {
  throw new Error("Invalid VITE_API_BASE_URL. It must start with http:// or https://");
}

const env = {
  apiBaseUrl,
};

export default env;