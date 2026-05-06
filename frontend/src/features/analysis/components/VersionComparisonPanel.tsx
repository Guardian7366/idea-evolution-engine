import { useEffect, useMemo, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import Button from "../../../components/shared/ui/Button";
import EmptyState from "../../../components/shared/EmptyState";
import SectionCard from "../../../components/shared/ui/SectionCard";
import {
  loadAnalysisPreviewVisibility,
  saveAnalysisPreviewVisibility,
} from "../../../shared/utils/workspaceStorage";
import type { ComparisonResponse, VersionResponse } from "../../../types/idea";

type VersionComparisonPanelProps = {
  ideaId: string | null;
  versions: VersionResponse[];
  latestComparison: ComparisonResponse | null;
  isLoading: boolean;
  onCompare: (payload: {
    leftVersionId: string;
    rightVersionId: string;
  }) => Promise<void>;
};

type PreviewBlockProps = {
  storageKey: "left" | "right";
  title: string;
  badges: string[];
  content: string;
  isOpen: boolean;
  onToggle: () => void;
};

const ANALYSIS_SUCCESS_OVERLAY_MS = 1050;

function getVersionLabel(
  version: VersionResponse,
  t: (key: string, options?: Record<string, unknown>) => string,
): string {
  return t("versionComparison.versionLabel", {
    number: version.version_number,
    transformation: version.transformation_type,
  });
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

function PreviewBlock({
  storageKey,
  title,
  badges,
  content,
  isOpen,
  onToggle,
}: PreviewBlockProps) {
  const { t } = useTranslation();
  const toggleLabel = isOpen
    ? t("versionComparison.preview.hideContent")
    : t("versionComparison.preview.showContent");
  const arrowSymbol = isOpen ? "▾" : "▸";

  return (
    <div className="comparison-preview-card rounded-[1.55rem] p-5 md:p-6">
      <div className="relative z-[1]">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div className="flex flex-wrap items-center gap-2">
            {badges.map((badge) => (
              <span key={badge} className="aero-badge">
                {badge}
              </span>
            ))}
          </div>

          <button
            type="button"
            onClick={onToggle}
            aria-expanded={isOpen}
            aria-label={toggleLabel}
            className="analysis-preview-toggle"
          >
            <span className="analysis-preview-toggle__symbol" aria-hidden="true">
              {arrowSymbol}
            </span>
          </button>
        </div>

        <h3 className="mt-4 text-lg font-semibold tracking-[-0.02em] text-slate-50">
          {title}
        </h3>

        {!isOpen ? (
          <div className="mt-4 rounded-[1.25rem] border border-white/8 bg-slate-950/22 px-4 py-3">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                {t("versionComparison.preview.associatedContent")}
              </p>

              <span className="text-xs text-slate-400">
                {storageKey === "left"
                  ? t("versionComparison.preview.collapsedView")
                  : t("versionComparison.preview.collapsedView")}
              </span>
            </div>

            <p className="mt-3 text-sm leading-7 text-slate-400">
              {t("versionComparison.preview.closedMessage")}
            </p>
          </div>
        ) : (
          <div className="mt-4 rounded-[1.25rem] border border-white/8 bg-slate-950/22 p-4">
            <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
              {t("versionComparison.preview.associatedContent")}
            </p>

            <p className="mt-3 whitespace-pre-wrap break-words text-sm leading-8 text-slate-300">
              {content}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default function VersionComparisonPanel({
  ideaId,
  versions,
  latestComparison,
  isLoading,
  onCompare,
}: VersionComparisonPanelProps) {
  const { t } = useTranslation();

  const selectableVersions = useMemo(
    () =>
      versions.map((version) => ({
        value: version.id,
        label: getVersionLabel(version, t),
      })),
    [versions, t],
  );

  const [leftVersionId, setLeftVersionId] = useState("");
  const [rightVersionId, setRightVersionId] = useState("");
  const [previewVisibility, setPreviewVisibility] = useState(() =>
    loadAnalysisPreviewVisibility(),
  );
  const [isComparisonCelebrating, setIsComparisonCelebrating] = useState(false);

  const comparisonOverlayTimeoutRef = useRef<number | null>(null);

  const leftVersion = versions.find((version) => version.id === leftVersionId) ?? null;
  const rightVersion = versions.find((version) => version.id === rightVersionId) ?? null;

  const isSameVersion =
    leftVersionId.length > 0 &&
    rightVersionId.length > 0 &&
    leftVersionId === rightVersionId;

  const isCompareDisabled =
    isLoading || !ideaId || !leftVersionId || !rightVersionId || isSameVersion;

  useEffect(() => {
    saveAnalysisPreviewVisibility(previewVisibility);
  }, [previewVisibility]);

  useEffect(() => {
    return () => {
      if (comparisonOverlayTimeoutRef.current !== null) {
        window.clearTimeout(comparisonOverlayTimeoutRef.current);
      }
    };
  }, []);

  const showComparisonSuccessOverlay = () => {
    if (comparisonOverlayTimeoutRef.current !== null) {
      window.clearTimeout(comparisonOverlayTimeoutRef.current);
      comparisonOverlayTimeoutRef.current = null;
    }

    setIsComparisonCelebrating(true);

    comparisonOverlayTimeoutRef.current = window.setTimeout(() => {
      setIsComparisonCelebrating(false);
      comparisonOverlayTimeoutRef.current = null;
    }, ANALYSIS_SUCCESS_OVERLAY_MS);
  };

  const handleToggleLeftPreview = () => {
    setPreviewVisibility((current) => ({
      ...current,
      leftOpen: !current.leftOpen,
    }));
  };

  const handleToggleRightPreview = () => {
    setPreviewVisibility((current) => ({
      ...current,
      rightOpen: !current.rightOpen,
    }));
  };

  const handleCompareClick = async () => {
    if (isCompareDisabled) {
      return;
    }

    await onCompare({
      leftVersionId,
      rightVersionId,
    });

    showComparisonSuccessOverlay();
  };

  return (
    <SectionCard
      title={t("versionComparison.title")}
      description={t("versionComparison.description")}
    >
      {versions.length < 2 ? (
        <EmptyState
          title={t("versionComparison.empty.title")}
          description={t("versionComparison.empty.description")}
        />
      ) : (
        <div className="analysis-comparison-stage relative grid gap-5">
          <div className="analysis-comparison-stage__halo analysis-comparison-stage__halo--one" />
          <div className="analysis-comparison-stage__halo analysis-comparison-stage__halo--two" />
          <div className="analysis-comparison-stage__grid" />

          <div className="relative z-[1] rounded-[1.45rem] border border-white/8 bg-slate-950/20 px-4 py-4 md:px-5">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div className="flex flex-wrap items-center gap-2">
                <span className="aero-badge">{t("versionComparison.badges.dualReading")}</span>
                <span className="aero-badge">
                  {t("versionComparison.badges.comparativeLens")}
                </span>
                <span className="aero-badge">
                  {t("versionComparison.badges.conceptualTension")}
                </span>
              </div>

              <div className="rounded-full border border-white/8 bg-white/[0.03] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">
                {t("versionComparison.contrastMode")}
              </div>
            </div>

            <p className="mt-3 text-sm leading-7 text-slate-300/84">
              {t("versionComparison.intro")}
            </p>
          </div>

          <div className="relative z-[1] analysis-comparison-control rounded-[1.55rem] border border-white/8 bg-slate-950/20 p-5 md:p-6">
            <div className="grid gap-4 lg:grid-cols-2">
              <div className="rounded-[1.25rem] border border-white/8 bg-slate-950/22 p-4">
                <label className="aero-label mb-2 block">
                  {t("versionComparison.leftVersionLabel")}
                </label>
                <select
                  value={leftVersionId}
                  onChange={(e) => setLeftVersionId(e.target.value)}
                  disabled={isLoading}
                  className="aero-select px-4 py-3 text-sm"
                >
                  <option value="">{t("versionComparison.selectVersionPlaceholder")}</option>
                  {selectableVersions.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>

                <p className="mt-3 text-xs leading-6 text-slate-400">
                  {t("versionComparison.leftVersionHelp")}
                </p>
              </div>

              <div className="rounded-[1.25rem] border border-white/8 bg-slate-950/22 p-4">
                <label className="aero-label mb-2 block">
                  {t("versionComparison.rightVersionLabel")}
                </label>
                <select
                  value={rightVersionId}
                  onChange={(e) => setRightVersionId(e.target.value)}
                  disabled={isLoading}
                  className="aero-select px-4 py-3 text-sm"
                >
                  <option value="">{t("versionComparison.selectVersionPlaceholder")}</option>
                  {selectableVersions.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>

                <p className="mt-3 text-xs leading-6 text-slate-400">
                  {t("versionComparison.rightVersionHelp")}
                </p>
              </div>
            </div>

            {isSameVersion ? (
              <div className="mt-4 rounded-[1.2rem] border border-amber-300/18 bg-amber-400/8 p-4 text-sm leading-6 text-amber-100">
                {t("versionComparison.sameVersionWarning")}
              </div>
            ) : null}

            <div className="mt-5 flex flex-wrap items-center gap-3">
              <Button
                type="button"
                variant="secondary"
                disabled={isCompareDisabled}
                onClick={handleCompareClick}
              >
                {t("versionComparison.compareAction")}
              </Button>

              <p className="text-xs leading-6 text-slate-400">
                {t("versionComparison.compareHelp")}
              </p>
            </div>
          </div>

          {leftVersion && rightVersion && !isSameVersion ? (
            <div className="relative z-[1] grid gap-4">
              <PreviewBlock
                storageKey="left"
                title={t("versionComparison.preview.referenceTitle")}
                badges={[
                  t("versionComparison.preview.leftSide"),
                  t("versionComparison.preview.versionBadge", {
                    number: leftVersion.version_number,
                  }),
                  leftVersion.transformation_type,
                ]}
                content={leftVersion.content}
                isOpen={previewVisibility.leftOpen}
                onToggle={handleToggleLeftPreview}
              />

              <PreviewBlock
                storageKey="right"
                title={t("versionComparison.preview.contrastedTitle")}
                badges={[
                  t("versionComparison.preview.rightSide"),
                  t("versionComparison.preview.versionBadge", {
                    number: rightVersion.version_number,
                  }),
                  rightVersion.transformation_type,
                ]}
                content={rightVersion.content}
                isOpen={previewVisibility.rightOpen}
                onToggle={handleToggleRightPreview}
              />
            </div>
          ) : null}

          <div className="comparison-result-panel relative z-[1] overflow-hidden rounded-[1.7rem] p-5 md:p-6">
            {isComparisonCelebrating ? (
              <AnalysisSuccessOverlay
                title={t("versionComparison.result.badges.generated")}
                subtitle={t("versionComparison.result.title")}
              />
            ) : null}

            <div className="relative z-[1]">

              <div className="flex flex-wrap items-center gap-2">
                <span className="aero-badge">
                  {t("versionComparison.result.badges.comparativeResult")}
                </span>
                <span className="aero-badge">
                  {t("versionComparison.result.badges.dualReading")}
                </span>
              </div>

              <h3 className="mt-4 text-lg font-semibold tracking-[-0.02em] text-slate-50">
                {t("versionComparison.result.title")}
              </h3>

              {!latestComparison ? (
                <p className="mt-3 text-sm leading-7 text-slate-300/84">
                  {t("versionComparison.result.empty")}
                </p>
              ) : (
                <div className="mt-4 grid gap-4">
                  <div className="flex flex-wrap gap-2">
                    <span className="aero-badge">
                      {t("versionComparison.result.badges.generated")}
                    </span>
                    <span className="aero-badge">
                      {t("versionComparison.result.badges.dualAnalysis")}
                    </span>
                  </div>

                  <div className="rounded-[1.3rem] border border-white/8 bg-slate-950/22 p-4">
                    <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                      {t("versionComparison.result.outputLabel")}
                    </p>

                    <p className="mt-3 whitespace-pre-wrap break-words text-sm leading-8 text-slate-200">
                      {latestComparison.comparison_text || t("versionComparison.result.noText")}
                    </p>
                  </div>
                </div>
              )}
            </div>

            <div className="comparison-result-panel__glow" />
          </div>
        </div>
      )}
    </SectionCard>
  );
}