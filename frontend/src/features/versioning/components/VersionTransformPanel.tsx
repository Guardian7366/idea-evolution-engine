import { useEffect, useRef, useState } from "react";
import type { FormEvent } from "react";
import { useTranslation } from "react-i18next";
import Button from "../../../components/shared/ui/Button";
import EmptyState from "../../../components/shared/EmptyState";
import SectionCard from "../../../components/shared/ui/SectionCard";
import type { LanguageMode, VersionResponse } from "../../../types/idea";

type VersionTransformPanelProps = {
  activeVersion: VersionResponse | null;
  isLoading: boolean;
  languageMode: LanguageMode;
  onEvolution: () => Promise<void>;
  onMutation: () => Promise<void>;
  onRefinement: (instruction: string) => Promise<void>;
};

type TransformationKind = "evolution" | "mutation" | "refinement";
type SuccessOverlayState = {
  kind: TransformationKind;
  versionNumber: number;
} | null;

const TRANSFORM_SUCCESS_OVERLAY_MS = 1050;

function getDefaultInstruction(languageMode: LanguageMode): string {
  if (languageMode === "en") {
    return "Make it clearer, more specific, and more useful for a university context.";
  }

  return "Hazla más clara, específica y útil para un contexto universitario.";
}

function getLanguageModeLabel(
  languageMode: LanguageMode,
  t: (key: string) => string,
): string {
  if (languageMode === "en") {
    return t("versionTransform.languageModes.en");
  }

  if (languageMode === "es") {
    return t("versionTransform.languageModes.es");
  }

  return t("versionTransform.languageModes.auto");
}

function getTransformationSuccessTitle(
  kind: TransformationKind,
  t: (key: string, options?: Record<string, unknown>) => string,
): string {
  if (kind === "evolution") {
    return t("versionTransform.successOverlay.evolution");
  }

  if (kind === "mutation") {
    return t("versionTransform.successOverlay.mutation");
  }

  return t("versionTransform.successOverlay.refinement");
}

function ActionHint({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  const { t } = useTranslation();

  return (
    <div className="mt-5 rounded-[1.2rem] border border-white/8 bg-slate-950/22 p-3">
      <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
        {t("versionTransform.actionHintLabel")}
      </p>
      <p className="mt-2 text-sm leading-6 text-slate-300/80">
        <span className="font-semibold text-slate-100">{title}: </span>
        {description}
      </p>
    </div>
  );
}

function TransformationSuccessOverlay({
  kind,
  versionNumber,
}: {
  kind: TransformationKind;
  versionNumber: number;
}) {
  const { t } = useTranslation();

  return (
    <div className="transform-success-overlay transform-success-overlay--visible" aria-hidden="true">
      <div className="transform-success-overlay__veil" />
      <div className="transform-success-overlay__ring transform-success-overlay__ring--one" />
      <div className="transform-success-overlay__ring transform-success-overlay__ring--two" />
      <div className="transform-success-overlay__pulse" />

      <div className="transform-success-overlay__core">
        <div className="transform-success-overlay__logo-shell">
          <img
            src="/favicon.png"
            alt=""
            className="transform-success-overlay__logo"
          />
        </div>

        <div className="transform-success-overlay__spark" />

        <div className="transform-success-overlay__text-stack">
          <p className="transform-success-overlay__title">
            {getTransformationSuccessTitle(kind, t)}
          </p>
          <p className="transform-success-overlay__subtitle">
            {t("versionTransform.successOverlay.versionNumber", {
              number: versionNumber,
            })}
          </p>
        </div>
      </div>
    </div>
  );
}

export default function VersionTransformPanel({
  activeVersion,
  isLoading,
  languageMode,
  onEvolution,
  onMutation,
  onRefinement,
}: VersionTransformPanelProps) {
  const { t } = useTranslation();

  const [instruction, setInstruction] = useState(getDefaultInstruction(languageMode));
  const [pendingTransformation, setPendingTransformation] =
    useState<TransformationKind | null>(null);
  const [pendingSourceVersionId, setPendingSourceVersionId] = useState<string | null>(null);
  const [successOverlay, setSuccessOverlay] = useState<SuccessOverlayState>(null);

  const overlayTimeoutRef = useRef<number | null>(null);
  const previousActiveVersionIdRef = useRef<string | null>(activeVersion?.id ?? null);

  useEffect(() => {
    setInstruction(getDefaultInstruction(languageMode));
  }, [languageMode]);

  useEffect(() => {
    return () => {
      if (overlayTimeoutRef.current !== null) {
        window.clearTimeout(overlayTimeoutRef.current);
      }
    };
  }, []);

  useEffect(() => {
    const currentActiveVersionId = activeVersion?.id ?? null;
    const previousActiveVersionId = previousActiveVersionIdRef.current;

    if (
      pendingTransformation &&
      !isLoading &&
      activeVersion &&
      pendingSourceVersionId &&
      currentActiveVersionId !== pendingSourceVersionId &&
      currentActiveVersionId !== previousActiveVersionId
    ) {
      if (overlayTimeoutRef.current !== null) {
        window.clearTimeout(overlayTimeoutRef.current);
        overlayTimeoutRef.current = null;
      }

      setSuccessOverlay({
        kind: pendingTransformation,
        versionNumber: activeVersion.version_number,
      });

      overlayTimeoutRef.current = window.setTimeout(() => {
        setSuccessOverlay(null);
        overlayTimeoutRef.current = null;
      }, TRANSFORM_SUCCESS_OVERLAY_MS);

      setPendingTransformation(null);
      setPendingSourceVersionId(null);
    }

    if (!isLoading && pendingTransformation && !activeVersion) {
      setPendingTransformation(null);
      setPendingSourceVersionId(null);
    }

    previousActiveVersionIdRef.current = currentActiveVersionId;
  }, [activeVersion, isLoading, pendingTransformation, pendingSourceVersionId]);

  const registerTransformationIntent = (kind: TransformationKind) => {
    if (!activeVersion || isLoading) {
      return false;
    }

    setPendingTransformation(kind);
    setPendingSourceVersionId(activeVersion.id);
    return true;
  };

  const handleEvolutionClick = async () => {
    if (!registerTransformationIntent("evolution")) {
      return;
    }

    try {
      await onEvolution();
    } catch (error) {
      setPendingTransformation(null);
      setPendingSourceVersionId(null);
      throw error;
    }
  };

  const handleMutationClick = async () => {
    if (!registerTransformationIntent("mutation")) {
      return;
    }

    try {
      await onMutation();
    } catch (error) {
      setPendingTransformation(null);
      setPendingSourceVersionId(null);
      throw error;
    }
  };

  const handleRefinementSubmit = async (event: FormEvent) => {
    event.preventDefault();

    if (!registerTransformationIntent("refinement")) {
      return;
    }

    try {
      await onRefinement(instruction);
    } catch (error) {
      setPendingTransformation(null);
      setPendingSourceVersionId(null);
      throw error;
    }
  };

  const isTransformationPending = pendingTransformation !== null && isLoading;

  return (
    <SectionCard
      title={t("versionTransform.title")}
      description={t("versionTransform.description")}
    >
      {!activeVersion ? (
        <EmptyState
          title={t("versionTransform.empty.title")}
          description={t("versionTransform.empty.description")}
        />
      ) : (
        <div className="transform-engine-stage relative grid gap-5">
          {successOverlay ? (
            <TransformationSuccessOverlay
              kind={successOverlay.kind}
              versionNumber={successOverlay.versionNumber}
            />
          ) : null}

          <div className="transform-engine-stage__halo transform-engine-stage__halo--one" />
          <div className="transform-engine-stage__halo transform-engine-stage__halo--two" />
          <div className="transform-engine-stage__grid" />

          <div
            className={[
              "transform-engine-status rounded-[1.45rem] border border-white/8 bg-slate-950/20 px-4 py-4 md:px-5",
              isTransformationPending ? "transform-engine-status--processing" : "",
            ].join(" ")}
          >
            <div className="flex flex-wrap items-center gap-2">
              <span className="aero-badge">{t("versionTransform.badges.engine")}</span>
              <span className="aero-badge">
                {t("versionTransform.badges.versionNumber", {
                  number: activeVersion.version_number,
                })}
              </span>
              <span className="aero-badge">{activeVersion.transformation_type}</span>
              <span className="aero-badge aero-badge--success">
                {t("versionTransform.badges.active")}
              </span>
              {isTransformationPending ? (
                <span className="aero-badge aero-badge--loading">
                  {t("versionTransform.processingBadge")}
                </span>
              ) : null}
            </div>

            <div className="mt-4 grid gap-3 md:grid-cols-[minmax(0,1fr)_auto] md:items-start">
              <p className="text-sm leading-7 text-slate-300/84">
                {t("versionTransform.activeDescription")}
              </p>

              <div className="rounded-2xl border border-white/8 bg-white/[0.03] px-3 py-2 text-xs text-slate-300">
                {t("versionTransform.liveNodeLabel")}
              </div>
            </div>

            <div className="transform-engine-status__glow" />
          </div>

          <div className="transform-actions grid gap-4">
            <div className="transform-actions__card transform-actions__card--evolution rounded-[1.6rem] p-5 md:p-6">
              <div className="transform-actions__grain" />
              <div className="transform-actions__orb transform-actions__orb--evolution" />

              <div className="relative z-[1] flex h-full flex-col">
                <div className="mb-4 flex flex-wrap items-center gap-2">
                  <span className="aero-badge aero-badge--success">
                    {t("versionTransform.evolution.badgePrimary")}
                  </span>
                  <span className="aero-badge">
                    {t("versionTransform.evolution.badgeSecondary")}
                  </span>
                </div>

                <h3 className="text-lg font-semibold tracking-[-0.02em] text-slate-50">
                  {t("versionTransform.evolution.title")}
                </h3>

                <p className="mt-2 text-sm leading-7 text-slate-300/84">
                  {t("versionTransform.evolution.description")}
                </p>

                <ActionHint
                  title={t("versionTransform.evolution.hintTitle")}
                  description={t("versionTransform.evolution.hintDescription")}
                />

                <div className="mt-5 flex justify-end">
                  <div className="w-full sm:w-[220px]">
                    <Button
                      type="button"
                      variant="success"
                      onClick={handleEvolutionClick}
                      disabled={isLoading}
                      fullWidth
                    >
                      {t("versionTransform.evolution.action")}
                    </Button>
                  </div>
                </div>
              </div>
            </div>

            <div className="transform-actions__card transform-actions__card--mutation rounded-[1.6rem] p-5 md:p-6">
              <div className="transform-actions__grain" />
              <div className="transform-actions__orb transform-actions__orb--mutation" />

              <div className="relative z-[1] flex h-full flex-col">
                <div className="mb-4 flex flex-wrap items-center gap-2">
                  <span className="aero-badge transform-mutation-badge">
                    {t("versionTransform.mutation.badgePrimary")}
                  </span>
                  <span className="aero-badge">
                    {t("versionTransform.mutation.badgeSecondary")}
                  </span>
                </div>

                <h3 className="text-lg font-semibold tracking-[-0.02em] text-slate-50">
                  {t("versionTransform.mutation.title")}
                </h3>

                <p className="mt-2 text-sm leading-7 text-slate-300/84">
                  {t("versionTransform.mutation.description")}
                </p>

                <ActionHint
                  title={t("versionTransform.mutation.hintTitle")}
                  description={t("versionTransform.mutation.hintDescription")}
                />

                <div className="mt-5 flex justify-end">
                  <div className="w-full sm:w-[220px]">
                    <Button
                      type="button"
                      variant="warning"
                      onClick={handleMutationClick}
                      disabled={isLoading}
                      fullWidth
                    >
                      {t("versionTransform.mutation.action")}
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <form
            onSubmit={handleRefinementSubmit}
            className="transform-refinement-panel rounded-[1.65rem] p-5 md:p-6"
          >
            <div className="transform-refinement-panel__grain" />
            <div className="transform-refinement-panel__orb" />

            <div className="relative z-[1]">
              <div className="mb-4 flex flex-wrap items-center gap-2">
                <span className="aero-badge">{t("versionTransform.refinement.badgePrimary")}</span>
                <span className="aero-badge">
                  {getLanguageModeLabel(languageMode, t)}
                </span>
                <span className="aero-badge">
                  {t("versionTransform.refinement.badgeTertiary")}
                </span>
              </div>

              <h3 className="text-lg font-semibold tracking-[-0.02em] text-slate-50">
                {t("versionTransform.refinement.title")}
              </h3>

              <p className="mt-2 text-sm leading-7 text-slate-300/84">
                {t("versionTransform.refinement.description")}
              </p>

              <div className="mt-5 grid gap-4 xl:grid-cols-[minmax(0,1.15fr)_minmax(280px,0.85fr)] xl:items-start">
                <div className="rounded-[1.2rem] border border-white/8 bg-slate-950/22 p-4">
                  <label className="aero-label mb-2 block">
                    {t("versionTransform.refinement.instructionLabel")}
                  </label>

                  <textarea
                    value={instruction}
                    onChange={(e) => setInstruction(e.target.value)}
                    rows={7}
                    disabled={isLoading}
                    className="aero-textarea min-h-[210px] px-4 py-3 text-sm leading-7"
                    placeholder={t("versionTransform.refinement.placeholder")}
                  />
                </div>

                <div className="rounded-[1.35rem] border border-white/8 bg-slate-950/22 p-4">
                  <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                    {t("versionTransform.refinement.usageTitle")}
                  </p>

                  <div className="mt-3 grid gap-3">
                    <div className="rounded-[1rem] border border-white/8 bg-white/[0.03] p-3">
                      <p className="text-sm font-semibold text-slate-100">
                        {t("versionTransform.refinement.tips.clarity.title")}
                      </p>
                      <p className="mt-1 text-sm leading-6 text-slate-300/80">
                        {t("versionTransform.refinement.tips.clarity.description")}
                      </p>
                    </div>

                    <div className="rounded-[1rem] border border-white/8 bg-white/[0.03] p-3">
                      <p className="text-sm font-semibold text-slate-100">
                        {t("versionTransform.refinement.tips.focus.title")}
                      </p>
                      <p className="mt-1 text-sm leading-6 text-slate-300/80">
                        {t("versionTransform.refinement.tips.focus.description")}
                      </p>
                    </div>

                    <div className="rounded-[1rem] border border-white/8 bg-white/[0.03] p-3">
                      <p className="text-sm font-semibold text-slate-100">
                        {t("versionTransform.refinement.tips.depth.title")}
                      </p>
                      <p className="mt-1 text-sm leading-6 text-slate-300/80">
                        {t("versionTransform.refinement.tips.depth.description")}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-5 flex flex-wrap items-center justify-between gap-3">
                <p className="max-w-xl text-xs leading-6 text-slate-400">
                  {t("versionTransform.refinement.footerText")}
                </p>

                <Button type="submit" disabled={isLoading || !instruction.trim()}>
                  {t("versionTransform.refinement.action")}
                </Button>
              </div>
            </div>

            <div className="transform-refinement-panel__glow" />
          </form>
        </div>
      )}
    </SectionCard>
  );
}