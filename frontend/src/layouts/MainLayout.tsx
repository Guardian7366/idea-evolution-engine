import type { PropsWithChildren } from "react";
import { useTranslation } from "react-i18next";
import AeroBubbleField from "../components/background/AeroBubbleField";
import WorkspaceLanguageSwitch from "../components/navigation/WorkspaceLanguageSwitch";

export default function MainLayout({ children }: PropsWithChildren) {
  const { t } = useTranslation();

  return (
    <div className="app-shell">
      <AeroBubbleField />

      <header className="app-header">
        <div className="app-header__aurora" />
        <div className="app-header__mesh" />
        <div className="app-header__line app-header__line--one" />
        <div className="app-header__line app-header__line--two" />
        <div className="app-header__halo app-header__halo--one" />
        <div className="app-header__halo app-header__halo--two" />

        <div className="mx-auto max-w-7xl px-5 py-5 md:px-6 md:py-6 xl:px-8 xl:py-7">
          <div className="app-header__utility-row mb-4 flex justify-end">
            <WorkspaceLanguageSwitch />
          </div>

          <div className="app-header__content grid gap-6 xl:grid-cols-[minmax(0,1.18fr)_minmax(320px,0.82fr)] xl:items-end">
            <div className="flex flex-col gap-4">
              <div className="flex flex-wrap items-center gap-2">
                <span className="app-header__pill">{t("header.pills.workspace")}</span>
                <span className="app-header__pill app-header__pill--muted">
                  {t("header.pills.system")}
                </span>
              </div>

              <div className="max-w-4xl">
                <p className="app-header__kicker">{t("header.kicker")}</p>

                <h1 className="app-header__title text-[2.2rem] font-bold md:text-5xl xl:text-[3.55rem]">
                  {t("header.title")}
                </h1>

                <p className="app-header__subtitle mt-3 max-w-3xl text-sm leading-7 md:text-[15px]">
                  {t("header.subtitle")}
                </p>
              </div>
            </div>

            <div className="app-header__status-panel rounded-[1.8rem] p-4 md:p-5">
              <div className="relative z-[1]">
                <div className="mb-4 flex flex-wrap items-center gap-2">
                  <span className="aero-badge">{t("header.badges.seed")}</span>
                  <span className="aero-badge">{t("header.badges.branch")}</span>
                  <span className="aero-badge aero-badge--success">
                    {t("header.badges.evolve")}
                  </span>
                </div>

                <div className="grid gap-3 sm:grid-cols-3 xl:grid-cols-1 2xl:grid-cols-3">
                  <div className="app-header__status-item rounded-2xl p-3">
                    <p className="app-header__status-label">{t("header.zones.zone1Label")}</p>
                    <p className="app-header__status-value">{t("header.zones.zone1Value")}</p>
                  </div>

                  <div className="app-header__status-item rounded-2xl p-3">
                    <p className="app-header__status-label">{t("header.zones.zone2Label")}</p>
                    <p className="app-header__status-value">{t("header.zones.zone2Value")}</p>
                  </div>

                  <div className="app-header__status-item rounded-2xl p-3">
                    <p className="app-header__status-label">{t("header.zones.zone3Label")}</p>
                    <p className="app-header__status-value">{t("header.zones.zone3Value")}</p>
                  </div>
                </div>
              </div>

              <div className="app-header__status-glow" />
            </div>
          </div>
        </div>
      </header>

      <main className="main-workspace relative z-10 mx-auto max-w-7xl px-5 py-7 md:px-6 md:py-9 xl:px-8 xl:py-10">
        {children}
      </main>
    </div>
  );
}