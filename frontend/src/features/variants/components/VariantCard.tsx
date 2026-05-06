import { useTranslation } from "react-i18next";
import Button from "../../../components/shared/ui/Button";
import type { VariantResponse } from "../../../types/idea";

type VariantCardProps = {
  variant: VariantResponse;
  isLoading: boolean;
  isSelecting: boolean;
  isCelebrating: boolean;
  isHighlighted: boolean;
  onSelect: (variantId: string) => Promise<void>;
  index: number;
};

function VariantSelectionOverlay({
  visible,
  title,
}: {
  visible: boolean;
  title: string;
}) {
  return (
    <div
      className={[
        "variant-selection-overlay",
        visible ? "variant-selection-overlay--visible" : "",
      ]
        .filter(Boolean)
        .join(" ")}
      aria-hidden={!visible}
    >
      <div className="variant-selection-overlay__veil" />
      <div className="variant-selection-overlay__ring variant-selection-overlay__ring--one" />
      <div className="variant-selection-overlay__ring variant-selection-overlay__ring--two" />
      <div className="variant-selection-overlay__pulse" />

      <div className="variant-selection-overlay__core">
        <div className="variant-selection-overlay__icon-shell">
          <div className="variant-selection-overlay__icon" />
        </div>

        <p className="variant-selection-overlay__title">{title}</p>
      </div>
    </div>
  );
}

export default function VariantCard({
  variant,
  isLoading,
  isSelecting,
  isCelebrating,
  isHighlighted,
  onSelect,
  index,
}: VariantCardProps) {
  const { t } = useTranslation();

  return (
    <article
      className={[
        "variant-card rounded-[1.7rem] p-5 transition duration-200 md:p-6",
        variant.is_selected
          ? "variant-card--selected"
          : "variant-card--default hover:-translate-y-[2px]",
        isSelecting ? "variant-card--selecting" : "",
        isCelebrating ? "variant-card--celebrating" : "",
        isHighlighted ? "variant-card--highlighted" : "",
      ]
        .filter(Boolean)
        .join(" ")}
    >
      <VariantSelectionOverlay
        visible={isCelebrating}
        title={t("variantCard.actions.selected")}
      />

      <div className="relative z-[1] flex h-full flex-col">
        <div className="mb-4 flex flex-wrap items-start justify-between gap-3">
          <div className="min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <span className="aero-badge">
                {t("variantCard.routeBadge", { index: index + 1 })}
              </span>
              <span className="aero-badge">{t("variantCard.variantBadge")}</span>
              {variant.is_selected ? (
                <span className="aero-badge aero-badge--success">
                  {t("variantCard.selectedBadge")}
                </span>
              ) : (
                <span className="aero-badge">{t("variantCard.availableBadge")}</span>
              )}
            </div>

            <h3 className="mt-4 text-lg font-semibold leading-7 tracking-[-0.02em] text-slate-50">
              {variant.title}
            </h3>
          </div>

          <div className="rounded-full border border-white/8 bg-white/[0.03] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">
            {t("variantCard.branchLabel")}
          </div>
        </div>

        <div className="rounded-[1.35rem] border border-white/8 bg-slate-950/20 p-4">
          <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
            {t("variantCard.proposedDirectionLabel")}
          </p>
          <p className="mt-3 text-sm leading-7 text-slate-300/84">{variant.description}</p>
        </div>

        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <div className="rounded-[1.1rem] border border-white/8 bg-slate-950/22 px-3 py-3">
            <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-500">
              {t("variantCard.functionLabel")}
            </p>
            <p className="mt-2 text-sm text-slate-200">
              {variant.is_selected
                ? t("variantCard.function.selected")
                : t("variantCard.function.candidate")}
            </p>
          </div>

          <div className="rounded-[1.1rem] border border-white/8 bg-slate-950/22 px-3 py-3">
            <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-500">
              {t("variantCard.resultLabel")}
            </p>
            <p className="mt-2 text-sm text-slate-200">
              {variant.is_selected
                ? t("variantCard.result.selected")
                : t("variantCard.result.available")}
            </p>
          </div>
        </div>

        <div className="mt-5 flex-1" />

        <div className="mt-5 flex flex-wrap items-center justify-between gap-3">
          <p className="max-w-[16rem] text-xs leading-6 text-slate-400">
            {variant.is_selected
              ? t("variantCard.footer.selected")
              : t("variantCard.footer.available")}
          </p>

          <div className="min-w-[190px]">
            <Button
              type="button"
              variant={variant.is_selected ? "success" : "primary"}
              disabled={isLoading || variant.is_selected || isSelecting}
              onClick={() => onSelect(variant.id)}
              fullWidth
              className={isSelecting ? "variant-card__action-button--busy" : ""}
            >
              {isSelecting
                ? t("flowStatus.states.processing")
                : variant.is_selected
                  ? t("variantCard.actions.selected")
                  : t("variantCard.actions.select")}
            </Button>
          </div>
        </div>
      </div>

      <div className="variant-card__orb variant-card__orb--one" />
      <div className="variant-card__orb variant-card__orb--two" />
      <div className="variant-card__selection-glow" />
    </article>
  );
}