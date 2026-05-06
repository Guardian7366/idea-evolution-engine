import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import en from "./locales/en";
import es from "./locales/es";
import type { UiLocale } from "./types";

export const DEFAULT_UI_LOCALE: UiLocale = "es";

export const UI_LOCALE_STORAGE_KEY = "idea-engine-ui-locale";

export function normalizeUiLocale(value: string | null | undefined): UiLocale {
  return value === "en" ? "en" : "es";
}

export function loadStoredUiLocale(): UiLocale {
  if (typeof window === "undefined" || typeof window.localStorage === "undefined") {
    return DEFAULT_UI_LOCALE;
  }

  try {
    const rawValue = window.localStorage.getItem(UI_LOCALE_STORAGE_KEY);
    return normalizeUiLocale(rawValue);
  } catch {
    return DEFAULT_UI_LOCALE;
  }
}

export function persistUiLocale(locale: UiLocale) {
  if (typeof window === "undefined" || typeof window.localStorage === "undefined") {
    return;
  }

  try {
    window.localStorage.setItem(UI_LOCALE_STORAGE_KEY, locale);
  } catch {
    // Silencio intencional para no romper la UI.
  }
}

const resources = {
  es: {
    translation: es,
  },
  en: {
    translation: en,
  },
} as const;

void i18n.use(initReactI18next).init({
  resources,
  lng: loadStoredUiLocale(),
  fallbackLng: DEFAULT_UI_LOCALE,
  interpolation: {
    escapeValue: false,
  },
});

i18n.on("languageChanged", (language) => {
  persistUiLocale(normalizeUiLocale(language));
});

export default i18n;