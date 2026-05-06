import type { LanguageMode } from "../../types/idea";
import type { UiLocale } from "../../i18n/types";

const SESSION_ID_KEY = "idea-engine-session-id";
const IDEA_ID_KEY = "idea-engine-idea-id";
const LANGUAGE_MODE_KEY = "idea-engine-language-mode";
const UI_LOCALE_KEY = "idea-engine-ui-locale";
const COLLAPSED_HISTORY_VERSION_IDS_KEY = "idea-engine-collapsed-history-version-ids";
const ANALYSIS_PREVIEW_VISIBILITY_KEY = "idea-engine-analysis-preview-visibility";

export type StoredWorkspace = {
  sessionId: string | null;
  ideaId: string | null;
  languageMode: LanguageMode;
};

export type AnalysisPreviewVisibility = {
  leftOpen: boolean;
  rightOpen: boolean;
};

function isBrowserEnvironment(): boolean {
  return typeof window !== "undefined" && typeof window.localStorage !== "undefined";
}

function normalizeLanguageMode(value: string | null): LanguageMode {
  return value === "es" || value === "en" || value === "auto" ? value : "auto";
}

function normalizeUiLocale(value: string | null): UiLocale {
  return value === "en" ? "en" : "es";
}

function normalizeStoredId(value: string | null): string | null {
  if (!value) {
    return null;
  }

  const trimmed = value.trim();

  if (!/^[a-z]+_[a-f0-9]{32}$/i.test(trimmed)) {
    return null;
  }

  return trimmed;
}

export function loadWorkspaceFromStorage(): StoredWorkspace {
  if (!isBrowserEnvironment()) {
    return {
      sessionId: null,
      ideaId: null,
      languageMode: "auto",
    };
  }

  try {
    const sessionId = window.localStorage.getItem(SESSION_ID_KEY);
    const ideaId = window.localStorage.getItem(IDEA_ID_KEY);
    const rawLanguageMode = window.localStorage.getItem(LANGUAGE_MODE_KEY);

    return {
      sessionId: normalizeStoredId(sessionId),
      ideaId: normalizeStoredId(ideaId),
      languageMode: normalizeLanguageMode(rawLanguageMode),
    };
  } catch {
    return {
      sessionId: null,
      ideaId: null,
      languageMode: "auto",
    };
  }
}

export function saveWorkspaceToStorage(params: {
  sessionId: string | null;
  ideaId: string | null;
  languageMode: LanguageMode;
}) {
  if (!isBrowserEnvironment()) {
    return;
  }

  const { sessionId, ideaId, languageMode } = params;

  try {
    if (sessionId) {
      window.localStorage.setItem(SESSION_ID_KEY, sessionId);
    } else {
      window.localStorage.removeItem(SESSION_ID_KEY);
    }

    if (ideaId) {
      window.localStorage.setItem(IDEA_ID_KEY, ideaId);
    } else {
      window.localStorage.removeItem(IDEA_ID_KEY);
    }

    window.localStorage.setItem(LANGUAGE_MODE_KEY, languageMode);
  } catch {
    // Silencio intencional: no queremos romper el flujo UI si localStorage falla.
  }
}

export function loadUiLocaleFromStorage(): UiLocale {
  if (!isBrowserEnvironment()) {
    return "es";
  }

  try {
    const rawValue = window.localStorage.getItem(UI_LOCALE_KEY);
    return normalizeUiLocale(rawValue);
  } catch {
    return "es";
  }
}

export function saveUiLocaleToStorage(locale: UiLocale) {
  if (!isBrowserEnvironment()) {
    return;
  }

  try {
    window.localStorage.setItem(UI_LOCALE_KEY, locale);
  } catch {
    // Silencio intencional para no romper la UI.
  }
}

export function loadCollapsedHistoryVersionIds(): string[] {
  if (!isBrowserEnvironment()) {
    return [];
  }

  try {
    const rawValue = window.localStorage.getItem(COLLAPSED_HISTORY_VERSION_IDS_KEY);

    if (!rawValue) {
      return [];
    }

    const parsedValue = JSON.parse(rawValue);

    if (!Array.isArray(parsedValue)) {
      return [];
    }

    return parsedValue.filter((value): value is string => typeof value === "string");
  } catch {
    return [];
  }
}

export function saveCollapsedHistoryVersionIds(versionIds: string[]) {
  if (!isBrowserEnvironment()) {
    return;
  }

  try {
    window.localStorage.setItem(
      COLLAPSED_HISTORY_VERSION_IDS_KEY,
      JSON.stringify(versionIds),
    );
  } catch {
    // Silencio intencional para no romper la UI.
  }
}

export function loadAnalysisPreviewVisibility(): AnalysisPreviewVisibility {
  if (!isBrowserEnvironment()) {
    return {
      leftOpen: false,
      rightOpen: false,
    };
  }

  try {
    const rawValue = window.localStorage.getItem(ANALYSIS_PREVIEW_VISIBILITY_KEY);

    if (!rawValue) {
      return {
        leftOpen: false,
        rightOpen: false,
      };
    }

    const parsedValue = JSON.parse(rawValue) as Partial<AnalysisPreviewVisibility>;

    return {
      leftOpen: parsedValue.leftOpen === true,
      rightOpen: parsedValue.rightOpen === true,
    };
  } catch {
    return {
      leftOpen: false,
      rightOpen: false,
    };
  }
}

export function saveAnalysisPreviewVisibility(visibility: AnalysisPreviewVisibility) {
  if (!isBrowserEnvironment()) {
    return;
  }

  try {
    window.localStorage.setItem(
      ANALYSIS_PREVIEW_VISIBILITY_KEY,
      JSON.stringify(visibility),
    );
  } catch {
    // Silencio intencional para no romper la UI.
  }
}

export function clearWorkspaceFromStorage() {
  if (!isBrowserEnvironment()) {
    return;
  }

  try {
    window.localStorage.removeItem(SESSION_ID_KEY);
    window.localStorage.removeItem(IDEA_ID_KEY);
    window.localStorage.removeItem(LANGUAGE_MODE_KEY);
    window.localStorage.removeItem(UI_LOCALE_KEY);
    window.localStorage.removeItem(COLLAPSED_HISTORY_VERSION_IDS_KEY);
    window.localStorage.removeItem(ANALYSIS_PREVIEW_VISIBILITY_KEY);
  } catch {
    // Silencio intencional por misma razón.
  }
}