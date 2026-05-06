import { useTranslation } from "react-i18next";
import EmptyState from "../../../components/shared/EmptyState";
import SectionCard from "../../../components/shared/ui/SectionCard";
import type { VersionResponse } from "../../../types/idea";

type ActiveVersionPanelProps = {
  activeVersion: VersionResponse | null;
  selectedVersion: VersionResponse | null;
};

function InfoBlock({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="focused-version-info rounded-[1.45rem] p-4">
      <div className="relative z-[1]">
        <p className="text-[11px] font-semibold uppercase tracking-[0.22em] text-slate-500">
          {label}
        </p>
        <p className="mt-2 break-all text-sm leading-7 text-slate-200">{value}</p>
      </div>
    </div>
  );
}

export default function ActiveVersionPanel({
  activeVersion,
  selectedVersion,
}: ActiveVersionPanelProps) {
  const { t } = useTranslation();
  const versionToDisplay = selectedVersion ?? activeVersion;
  const isRealActive = versionToDisplay?.id === activeVersion?.id;

  return (
    <SectionCard
      title={t("activeVersion.title")}
      description={t("activeVersion.description")}
    >
      {!versionToDisplay ? (
        <EmptyState
          title={t("activeVersion.empty.title")}
          description={t("activeVersion.empty.description")}
        />
      ) : (
        <div className="focused-version-stage grid gap-4">
          <div className="focused-version-banner rounded-[1.65rem] p-5 md:p-6">
            <div className="relative z-[1] grid gap-4 xl:grid-cols-[minmax(0,1fr)_auto] xl:items-start">
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <span className="aero-badge">{t("activeVersion.badges.coreVersion")}</span>
                  <span className="aero-badge">
                    {t("activeVersion.badges.versionNumber", {
                      number: versionToDisplay.version_number,
                    })}
                  </span>
                  <span className="aero-badge">{versionToDisplay.transformation_type}</span>
                  {isRealActive ? (
                    <span className="aero-badge aero-badge--success">
                      {t("activeVersion.badges.realActive")}
                    </span>
                  ) : (
                    <span className="aero-badge">
                      {t("activeVersion.badges.inspection")}
                    </span>
                  )}
                </div>

                <h3 className="mt-4 text-xl font-semibold tracking-[-0.02em] text-slate-50">
                  {isRealActive
                    ? t("activeVersion.headers.realActive")
                    : t("activeVersion.headers.inspection")}
                </h3>

                <p className="mt-2 max-w-3xl text-sm leading-7 text-slate-300/84">
                  {isRealActive
                    ? t("activeVersion.messages.realActive")
                    : t("activeVersion.messages.inspection")}
                </p>
              </div>

              <div className="rounded-[1.2rem] border border-white/8 bg-slate-950/22 px-4 py-3 text-sm text-slate-300">
                <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-500">
                  {t("activeVersion.visualModeLabel")}
                </p>
                <p className="mt-2 font-medium text-slate-100">
                  {isRealActive
                    ? t("activeVersion.visualModes.activeCore")
                    : t("activeVersion.visualModes.temporaryInspection")}
                </p>
              </div>
            </div>

            <div className="focused-version-banner__orb focused-version-banner__orb--one" />
            <div className="focused-version-banner__orb focused-version-banner__orb--two" />
          </div>

          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            <InfoBlock
              label={t("activeVersion.info.versionId")}
              value={versionToDisplay.id}
            />
            <InfoBlock
              label={t("activeVersion.info.appliedTransformation")}
              value={versionToDisplay.transformation_type}
            />
            <InfoBlock
              label={t("activeVersion.info.versionNumber")}
              value={t("activeVersion.badges.versionNumber", {
                number: versionToDisplay.version_number,
              })}
            />
          </div>

          <div className="focused-version-body rounded-[1.5rem] p-5 md:p-6">
            <div className="relative z-[1]">
              <div className="mb-3 flex flex-wrap items-center gap-2">
                <span className="aero-badge">{t("activeVersion.contentBadges.versionContent")}</span>
                <span className="aero-badge">{t("activeVersion.contentBadges.readableCore")}</span>
                <span className="aero-badge">
                  {isRealActive
                    ? t("activeVersion.contentBadges.currentState")
                    : t("activeVersion.contentBadges.focusedView")}
                </span>
              </div>

              <p className="text-[11px] font-semibold uppercase tracking-[0.22em] text-slate-500">
                {t("activeVersion.centralContentLabel")}
              </p>

              <div className="mt-4 rounded-[1.3rem] border border-white/8 bg-slate-950/20 p-4 md:p-5">
                <p className="whitespace-pre-wrap text-sm leading-8 text-slate-200">
                  {versionToDisplay.content}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </SectionCard>
  );
}