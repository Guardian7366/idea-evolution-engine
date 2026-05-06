import { useTranslation } from "react-i18next";
import SectionCard from "../../../components/shared/ui/SectionCard";
import type { LanguageMode } from "../../../types/idea";

type LanguageSelectorPanelProps = {
  value: LanguageMode;
  isLoading: boolean;
  onChange: (value: LanguageMode) => void;
};

function getLanguageHint(value: LanguageMode, t: (key: string) => string): string {
  if (value === "es") {
    return t("languageSelector.hints.es");
  }

  if (value === "en") {
    return t("languageSelector.hints.en");
  }

  return t("languageSelector.hints.auto");
}

function getLanguageDescription(value: LanguageMode, t: (key: string) => string): string {
  if (value === "es") {
    return t("languageSelector.descriptions.es");
  }

  if (value === "en") {
    return t("languageSelector.descriptions.en");
  }

  return t("languageSelector.descriptions.auto");
}

export default function LanguageSelectorPanel({
  value,
  isLoading,
  onChange,
}: LanguageSelectorPanelProps) {
  const { t } = useTranslation();

  return (
    <SectionCard
      title={t("languageSelector.title")}
      description={t("languageSelector.description")}
    >
      <div className="language-panel-shell rounded-[1.6rem] p-5 md:p-6">
        <div className="relative z-[1]">
          <div className="mb-4 flex flex-wrap items-start justify-between gap-3">
            <div className="flex flex-wrap items-center gap-2">
              <span className="aero-badge">{t("languageSelector.badges.control")}</span>
              <span className="aero-badge">{getLanguageHint(value, t)}</span>
            </div>

            <div className="rounded-full border border-white/8 bg-white/[0.03] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">
              {t("languageSelector.outputMode")}
            </div>
          </div>

          <div className="grid gap-4 xl:grid-cols-[minmax(0,1.04fr)_minmax(250px,0.96fr)] xl:items-start">
            <div className="rounded-[1.25rem] border border-white/8 bg-slate-950/20 p-4">
              <label className="aero-label mb-2 block">{t("languageSelector.modeLabel")}</label>

              <select
                value={value}
                disabled={isLoading}
                onChange={(e) => onChange(e.target.value as LanguageMode)}
                className="aero-select px-4 py-3 text-sm"
              >
                <option value="auto">{t("languageSelector.options.auto")}</option>
                <option value="es">{t("languageSelector.options.es")}</option>
                <option value="en">{t("languageSelector.options.en")}</option>
              </select>

              <p className="mt-3 text-sm leading-7 text-slate-300/82">
                {getLanguageDescription(value, t)}
              </p>
            </div>

            <div className="rounded-[1.25rem] border border-white/8 bg-slate-950/22 p-4">
              <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                {t("languageSelector.expectedBehaviorTitle")}
              </p>

              <div className="mt-3 grid gap-3">
                <div className="rounded-[1rem] border border-white/8 bg-white/[0.03] p-3">
                  <p className="text-sm font-semibold text-slate-100">
                    {t("languageSelector.behaviors.auto.title")}
                  </p>
                  <p className="mt-1 text-sm leading-6 text-slate-300/80">
                    {t("languageSelector.behaviors.auto.description")}
                  </p>
                </div>

                <div className="rounded-[1rem] border border-white/8 bg-white/[0.03] p-3">
                  <p className="text-sm font-semibold text-slate-100">
                    {t("languageSelector.behaviors.manual.title")}
                  </p>
                  <p className="mt-1 text-sm leading-6 text-slate-300/80">
                    {t("languageSelector.behaviors.manual.description")}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="language-panel-shell__orb" />
      </div>
    </SectionCard>
  );
}