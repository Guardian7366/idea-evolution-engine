import { useTranslation } from "react-i18next";
import type { UiLocale } from "../../i18n/types";

export default function WorkspaceLanguageSwitch() {
  const { i18n, t } = useTranslation();

  const activeLanguage: UiLocale = i18n.language === "en" ? "en" : "es";

  const handleChangeLanguage = async (locale: UiLocale) => {
    if (locale === activeLanguage) {
      return;
    }

    await i18n.changeLanguage(locale);
  };

  return (
    <div
      className="workspace-language-switch"
      role="group"
      aria-label={t("app.languageSwitch.ariaLabel")}
    >
      <div className="workspace-language-switch__backdrop" />

      <div
        className={[
          "workspace-language-switch__thumb",
          activeLanguage === "es"
            ? "workspace-language-switch__thumb--left"
            : "workspace-language-switch__thumb--right",
        ].join(" ")}
      >
        <span className="workspace-language-switch__thumb-glow" />
      </div>

      <button
        type="button"
        className={[
          "workspace-language-switch__option",
          activeLanguage === "es"
            ? "workspace-language-switch__option--active"
            : "",
        ]
          .filter(Boolean)
          .join(" ")}
        aria-pressed={activeLanguage === "es"}
        onClick={() => void handleChangeLanguage("es")}
      >
        <span className="workspace-language-switch__option-label">
          {t("app.languageSwitch.es")}
        </span>
      </button>

      <button
        type="button"
        className={[
          "workspace-language-switch__option",
          activeLanguage === "en"
            ? "workspace-language-switch__option--active"
            : "",
        ]
          .filter(Boolean)
          .join(" ")}
        aria-pressed={activeLanguage === "en"}
        onClick={() => void handleChangeLanguage("en")}
      >
        <span className="workspace-language-switch__option-label">
          {t("app.languageSwitch.en")}
        </span>
      </button>

      <div className="workspace-language-switch__shine" />
      <div className="workspace-language-switch__orb workspace-language-switch__orb--one" />
      <div className="workspace-language-switch__orb workspace-language-switch__orb--two" />
    </div>
  );
}