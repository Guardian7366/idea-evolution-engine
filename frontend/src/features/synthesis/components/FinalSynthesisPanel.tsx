import { useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import EmptyState from "../../../components/shared/EmptyState";
import Button from "../../../components/shared/ui/Button";
import SectionCard from "../../../components/shared/ui/SectionCard";
import type { SynthesisResponse, VersionResponse } from "../../../types/idea";

type FinalSynthesisPanelProps = {
  activeVersion: VersionResponse | null;
  synthesis: SynthesisResponse | null;
  isLoading: boolean;
  onGenerate: () => Promise<void>;
};

type SynthesisBlockProps = {
  title: string;
  content: string;
  variant?: "primary" | "secondary" | "wide";
};

const SYNTHESIS_CELEBRATION_MS = 1450;

function SynthesisCompletionOverlay({
  title,
  subtitle,
}: {
  title: string;
  subtitle: string;
}) {
  return (
    <div className="synthesis-completion-overlay synthesis-completion-overlay--visible" aria-hidden="true">
      <div className="synthesis-completion-overlay__veil" />
      <div className="synthesis-completion-overlay__aurora synthesis-completion-overlay__aurora--one" />
      <div className="synthesis-completion-overlay__aurora synthesis-completion-overlay__aurora--two" />
      <div className="synthesis-completion-overlay__ring synthesis-completion-overlay__ring--one" />
      <div className="synthesis-completion-overlay__ring synthesis-completion-overlay__ring--two" />
      <div className="synthesis-completion-overlay__beam" />

      <div className="synthesis-completion-overlay__core">
        <div className="synthesis-completion-overlay__logo-shell">
          <img src="/favicon.png" alt="" className="synthesis-completion-overlay__logo" />
        </div>

        <div className="synthesis-completion-overlay__spark synthesis-completion-overlay__spark--one" />
        <div className="synthesis-completion-overlay__spark synthesis-completion-overlay__spark--two" />
        <div className="synthesis-completion-overlay__spark synthesis-completion-overlay__spark--three" />

        <div className="synthesis-completion-overlay__text-stack">
          <p className="synthesis-completion-overlay__title">{title}</p>
          <p className="synthesis-completion-overlay__subtitle">{subtitle}</p>
        </div>
      </div>
    </div>
  );
}

function SynthesisBlock({ title, content, variant = "secondary" }: SynthesisBlockProps) {
  return (
    <div
      className={[
        "synthesis-block synthesis-block--final rounded-[1.6rem] p-5 md:p-6",
        variant === "primary" ? "synthesis-block--primary" : "",
        variant === "wide" ? "synthesis-block--wide" : "",
      ]
        .filter(Boolean)
        .join(" ")}
    >
      <div className="synthesis-block__glow" />
      <div className="synthesis-block__shine" />

      <div className="relative z-[1]">
        <p className="text-[11px] font-semibold uppercase tracking-[0.22em] text-slate-500">
          {title}
        </p>
        <p className="mt-4 whitespace-pre-wrap text-sm leading-8 text-slate-200">
          {content}
        </p>
      </div>
    </div>
  );
}

export default function FinalSynthesisPanel({
  activeVersion,
  synthesis,
  isLoading,
  onGenerate,
}: FinalSynthesisPanelProps) {
  const { t } = useTranslation();
  const [isSynthesisCelebrating, setIsSynthesisCelebrating] = useState(false);
  const celebrationTimeoutRef = useRef<number | null>(null);

  useEffect(() => {
    return () => {
      if (celebrationTimeoutRef.current !== null) {
        window.clearTimeout(celebrationTimeoutRef.current);
      }
    };
  }, []);

  const showSynthesisCelebration = () => {
    if (celebrationTimeoutRef.current !== null) {
      window.clearTimeout(celebrationTimeoutRef.current);
      celebrationTimeoutRef.current = null;
    }

    setIsSynthesisCelebrating(true);

    celebrationTimeoutRef.current = window.setTimeout(() => {
      setIsSynthesisCelebrating(false);
      celebrationTimeoutRef.current = null;
    }, SYNTHESIS_CELEBRATION_MS);
  };

  const handleGenerateSynthesis = async () => {
    await onGenerate();
    showSynthesisCelebration();
  };

  return (
    <SectionCard
      title={t("finalSynthesis.title")}
      description={t("finalSynthesis.description")}
      action={
        <Button
          type="button"
          variant="primary"
          disabled={!activeVersion || isLoading}
          onClick={handleGenerateSynthesis}
        >
          {t("finalSynthesis.generateAction")}
        </Button>
      }
    >
      <div className="synthesis-stage-shell relative">
        <div className="synthesis-stage-shell__halo synthesis-stage-shell__halo--one" />
        <div className="synthesis-stage-shell__halo synthesis-stage-shell__halo--two" />
        <div className="synthesis-stage-shell__grid" />

        {!synthesis ? (
          <div className="synthesis-empty-shell relative z-[1]">
            <EmptyState
              title={t("finalSynthesis.empty.title")}
              description={t("finalSynthesis.empty.description")}
            />
          </div>
        ) : (
          <div className="synthesis-stage relative z-[1] grid gap-5">
            <div className="synthesis-finale-hero relative overflow-hidden rounded-[1.65rem] border border-white/8 bg-slate-950/20 p-5 md:p-6">
              {isSynthesisCelebrating ? (
                <SynthesisCompletionOverlay
                  title={t("finalSynthesis.badges.generated")}
                  subtitle={t("finalSynthesis.headerTitle")}
                />
              ) : null}

              <div className="synthesis-finale-hero__orb synthesis-finale-hero__orb--one" />
              <div className="synthesis-finale-hero__orb synthesis-finale-hero__orb--two" />
              <div className="synthesis-finale-hero__arc synthesis-finale-hero__arc--one" />
              <div className="synthesis-finale-hero__arc synthesis-finale-hero__arc--two" />

              <div className="relative z-[1]">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="aero-badge">{t("finalSynthesis.badges.flowClosure")}</span>
                  <span className="aero-badge aero-badge--success">
                    {t("finalSynthesis.badges.generated")}
                  </span>
                  <span className="aero-badge">
                    {t("finalSynthesis.badges.consolidatedResult")}
                  </span>
                </div>

                <h3 className="mt-4 text-xl font-semibold tracking-[-0.02em] text-slate-50 md:text-2xl">
                  {t("finalSynthesis.headerTitle")}
                </h3>

                <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-300/84">
                  {t("finalSynthesis.headerDescription")}
                </p>

                <div className="mt-5 grid gap-3 sm:grid-cols-3">
                  <div className="synthesis-summary-card rounded-[1.2rem] px-3 py-3">
                    <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                      {t("finalSynthesis.summaryCards.state.label")}
                    </p>
                    <p className="mt-2 text-sm text-slate-200">
                      {t("finalSynthesis.summaryCards.state.value")}
                    </p>
                  </div>

                  <div className="synthesis-summary-card rounded-[1.2rem] px-3 py-3">
                    <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                      {t("finalSynthesis.summaryCards.base.label")}
                    </p>
                    <p className="mt-2 text-sm text-slate-200">
                      {t("finalSynthesis.summaryCards.base.value", {
                        number: activeVersion?.version_number ?? "-",
                      })}
                    </p>
                  </div>

                  <div className="synthesis-summary-card rounded-[1.2rem] px-3 py-3">
                    <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                      {t("finalSynthesis.summaryCards.result.label")}
                    </p>
                    <p className="mt-2 text-sm text-slate-200">
                      {t("finalSynthesis.summaryCards.result.value")}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="grid gap-5 xl:grid-cols-2">
              <SynthesisBlock
                variant="primary"
                title={t("finalSynthesis.blocks.summary")}
                content={synthesis.summary}
              />
              <SynthesisBlock
                title={t("finalSynthesis.blocks.valueProposition")}
                content={synthesis.value_proposition}
              />
              <SynthesisBlock
                title={t("finalSynthesis.blocks.targetAudience")}
                content={synthesis.target_audience}
              />
              <SynthesisBlock
                title={t("finalSynthesis.blocks.nextSteps")}
                content={synthesis.next_steps}
              />
            </div>

            <SynthesisBlock
              variant="wide"
              title={t("finalSynthesis.blocks.structuredDescription")}
              content={synthesis.structured_description}
            />
          </div>
        )}
      </div>
    </SectionCard>
  );
}