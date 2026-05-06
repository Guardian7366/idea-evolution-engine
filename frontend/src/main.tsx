import React from "react";
import ReactDOM from "react-dom/client";
import "./i18n";
import App from "./app/App";
import "./index.css";
import "./styles/tailwind.css";

const rootElement = document.getElementById("root");

if (!rootElement) {
  throw new Error("No se encontró el elemento raíz #root para montar la aplicación.");
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);