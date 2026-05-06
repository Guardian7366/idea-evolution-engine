import { useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import Button from "../../../components/shared/ui/Button";
import EmptyState from "../../../components/shared/EmptyState";
import SectionCard from "../../../components/shared/ui/SectionCard";
import type { PerspectiveResponse, VersionResponse } from "../../../types/idea";

type PerspectiveExplorerPanelProps = {
  activeVersion: VersionResponse | null;
  latestAnalysis: PerspectiveResponse | null;
  isLoading: boolean;
  onAnalyze: (perspective: string) => Promise<void>;
};

const ANALYSIS_SUCCESS_OVERLAY_MS = 1050;

function getPerspectiveOptions(t: (key: string) => string) {
  return [
    { value: "business_potential", label: t("perspectiveExplorer.options.businessPotential") },
    { value: "user_value", label: t("perspectiveExplorer.options.userValue") },
    { value: "innovation", label: t("perspectiveExplorer.options.innovation") },
    { value: "feasibility", label: t("perspectiveExplorer.options.feasibility") },
  ];
}

function getPerspectiveDescription(
  value: string,
  t: (key: string) => string,
): string {
  if (value === "business_potential") {
    return t("perspectiveExplorer.descriptions.businessPotential");
  }

  if (value === "user_value") {
    return t("perspectiveExplorer.descriptions.userValue");
  }

  if (value === "innovation") {
    return t("perspectiveExplorer.descriptions.innovation");
  }

  if (value === "feasibility") {
    return t("perspectiveExplorer.descriptions.feasibility");
  }

  return t("perspectiveExplorer.descriptions.default");
}

function AnalysisSuccessOverlay({
  title,
  subtitle,
}: {
  title: string;
  subtitle: string;
}) {
  return (
    <div className="analysis-success-overlay analysis-success-overlay--visible" aria-hidden="true">
      <div className="analysis-success-overlay__veil" />
      <div className="analysis-success-overlay__lens analysis-success-overlay__lens--one" />
      <div className="analysis-success-overlay__lens analysis-success-overlay__lens--two" />
      <div className="analysis-success-overlay__scan" />

      <div className="analysis-success-overlay__core">
        <div className="analysis-success-overlay__logo-shell">
          <img src="/favicon.png" alt="" className="analysis-success-overlay__logo" />
        </div>

        <div className="analysis-success-overlay__spark" />

        <div className="analysis-success-overlay__text-stack">
          <p className="analysis-success-overlay__title">{title}</p>
          <p className="analysis-success-overlay__subtitle">{subtitle}</p>
        </div>
      </div>
    </div>
  );
}

export default function PerspectiveExplorerPanel({
  activeVersion,
  latestAnalysis,
  isLoading,
  onAnalyze,
}: PerspectiveExplorerPanelProps) {
  const { t } = useTranslation();
  const [selectedPerspective, setSelectedPerspective] = useState("business_potential");
  const [isPerspectiveCelebrating, setIsPerspectiveCelebrating] = useState(false);
  const perspectiveOptions = getPerspectiveOptions(t);

  const perspectiveOverlayTimeoutRef = useRef<number | null>(null);

  useEffect(() => {
    return () => {
      if (perspectiveOverlayTimeoutRef.current !== null) {
        window.clearTimeout(perspectiveOverlayTimeoutRef.current);
      }
    };
  }, []);

  const showPerspectiveSuccessOverlay = () => {
    if (perspectiveOverlayTimeoutRef.current !== null) {
      window.clearTimeout(perspectiveOverlayTimeoutRef.current);
      perspectiveOverlayTimeoutRef.current = null;
    }

    setIsPerspectiveCelebrating(true);

    perspectiveOverlayTimeoutRef.current = window.setTimeout(() => {
      setIsPerspectiveCelebrating(false);
      perspectiveOverlayTimeoutRef.current = null;
    }, ANALYSIS_SUCCESS_OVERLAY_MS);
  };

  const handleAnalyzeClick = async () => {
    await onAnalyze(selectedPerspective);
    showPerspectiveSuccessOverlay();
  };

  return (
    <SectionCard
      title={t("perspectiveExplorer.title")}
      description={t("perspectiveExplorer.description")}
    >
      {!activeVersion ? (
        <EmptyState
          title={t("perspectiveExplorer.empty.title")}
          description={t("perspectiveExplorer.empty.description")}
        />
      ) : (
        <div className="analysis-perspective-stage relative grid gap-5">

          <div className="analysis-perspective-stage__halo analysis-perspective-stage__halo--one" />
          <div className="analysis-perspective-stage__halo analysis-perspective-stage__halo--two" />
          <div className="analysis-perspective-stage__grid" />

          <div className="relative z-[1] rounded-[1.45rem] border border-white/8 bg-slate-950/20 p-4">
            <div className="flex flex-wrap items-center gap-2">
              <span className="aero-badge">{t("perspectiveExplorer.badges.conceptLens")}</span>
              <span className="aero-badge">{t("perspectiveExplorer.badges.focusedReading")}</span>
              <span className="aero-badge">
                {t("perspectiveExplorer.badges.version", {
                  number: activeVersion.version_number,
                })}
              </span>
            </div>

            <p className="mt-3 text-sm leading-7 text-slate-300/84">
              {t("perspectiveExplorer.intro")}
            </p>
          </div>

          <div className="analysis-perspective-stage__controls relative z-[1] rounded-[1.6rem] border border-white/8 bg-slate-950/20 p-5 md:p-6">
            <div className="grid gap-5 xl:grid-cols-[minmax(0,1.04fr)_minmax(280px,0.96fr)] xl:items-start">
              <div>
                <label className="aero-label mb-2 block">
                  {t("perspectiveExplorer.perspectiveLabel")}
                </label>

                <select
                  value={selectedPerspective}
                  onChange={(e) => setSelectedPerspective(e.target.value)}
                  disabled={isLoading}
                  className="aero-select px-4 py-3 text-sm"
                >
                  {perspectiveOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>

                <p className="mt-3 text-sm leading-7 text-slate-300/84">
                  {getPerspectiveDescription(selectedPerspective, t)}
                </p>

                <div className="mt-5">
                  <Button
                    type="button"
                    variant="secondary"
                    disabled={isLoading}
                    onClick={handleAnalyzeClick}
                  >
                    {t("perspectiveExplorer.analyzeAction")}
                  </Button>
                </div>
              </div>

              <div className="rounded-[1.25rem] border border-white/8 bg-slate-950/22 p-4">
                <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                  {t("perspectiveExplorer.expectedReadingTitle")}
                </p>

                <p className="mt-3 text-sm leading-7 text-slate-300/82">
                  {t("perspectiveExplorer.expectedReadingDescription")}
                </p>

                <div className="mt-4 grid gap-3">
                  <div className="rounded-[1rem] border border-white/8 bg-white/[0.03] p-3">
                    <p className="text-sm font-semibold text-slate-100">
                      {t("perspectiveExplorer.cards.business.title")}
                    </p>
                    <p className="mt-1 text-sm leading-6 text-slate-300/80">
                      {t("perspectiveExplorer.cards.business.description")}
                    </p>
                  </div>

                  <div className="rounded-[1rem] border border-white/8 bg-white/[0.03] p-3">
                    <p className="text-sm font-semibold text-slate-100">
                      {t("perspectiveExplorer.cards.user.title")}
                    </p>
                    <p className="mt-1 text-sm leading-6 text-slate-300/80">
                      {t("perspectiveExplorer.cards.user.description")}
                    </p>
                  </div>

                  <div className="rounded-[1rem] border border-white/8 bg-white/[0.03] p-3">
                    <p className="text-sm font-semibold text-slate-100">
                      {t("perspectiveExplorer.cards.execution.title")}
                    </p>
                    <p className="mt-1 text-sm leading-6 text-slate-300/80">
                      {t("perspectiveExplorer.cards.execution.description")}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="analysis-result-panel relative z-[1] overflow-hidden rounded-[1.7rem] p-5 md:p-6">
            {isPerspectiveCelebrating ? (
              <AnalysisSuccessOverlay
                title={t("perspectiveExplorer.result.badges.generated")}
                subtitle={t("perspectiveExplorer.result.title")}
              />
            ) : null}

            <div className="relative z-[1]">

              <div className="flex flex-wrap items-center gap-2">
                <span className="aero-badge">
                  {t("perspectiveExplorer.result.badges.perspectiveReading")}
                </span>
                {latestAnalysis ? (
                  <span className="aero-badge">{latestAnalysis.analysis_type}</span>
                ) : null}
              </div>

              <h3 className="mt-4 text-lg font-semibold tracking-[-0.02em] text-slate-50">
                {t("perspectiveExplorer.result.title")}
              </h3>

              {!latestAnalysis ? (
                <p className="mt-3 text-sm leading-7 text-slate-300/84">
                  {t("perspectiveExplorer.result.empty")}
                </p>
              ) : (
                <div className="mt-4 grid gap-4">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="aero-badge">
                      {t("perspectiveExplorer.result.badges.generated")}
                    </span>
                    <span className="aero-badge">{latestAnalysis.analysis_type}</span>
                  </div>

                  <div className="rounded-[1.3rem] border border-white/8 bg-slate-950/22 p-4">
                    <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                      {t("perspectiveExplorer.result.outputLabel")}
                    </p>

                    <p className="mt-3 whitespace-pre-wrap text-sm leading-8 text-slate-200">
                      {latestAnalysis.content}
                    </p>
                  </div>
                </div>
              )}
            </div>

            <div className="analysis-result-panel__orb analysis-result-panel__orb--one" />
            <div className="analysis-result-panel__orb analysis-result-panel__orb--two" />
          </div>
        </div>
      )}
    </SectionCard>
  );
}