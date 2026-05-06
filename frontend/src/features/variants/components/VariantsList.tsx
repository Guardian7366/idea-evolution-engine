import { useEffect, useMemo, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import EmptyState from "../../../components/shared/EmptyState";
import SectionCard from "../../../components/shared/ui/SectionCard";
import type { VariantResponse } from "../../../types/idea";
import VariantCard from "./VariantCard";

type VariantsListProps = {
  variants: VariantResponse[];
  isLoading: boolean;
  onSelect: (variantId: string) => Promise<void>;
};

const FINAL_CELEBRATION_MS = 900;
const FINAL_HIGHLIGHT_MS = 1400;

export default function VariantsList({
  variants,
  isLoading,
  onSelect,
}: VariantsListProps) {
  const { t } = useTranslation();

  const selectedVariant = variants.find((variant) => variant.is_selected) ?? null;

  const [pendingVariantId, setPendingVariantId] = useState<string | null>(null);
  const [celebratingVariantId, setCelebratingVariantId] = useState<string | null>(null);
  const [highlightedVariantId, setHighlightedVariantId] = useState<string | null>(null);

  const selectionLockRef = useRef(false);
  const celebrationTimeoutRef = useRef<number | null>(null);
  const highlightTimeoutRef = useRef<number | null>(null);

  const clearAnimationTimeouts = () => {
    if (celebrationTimeoutRef.current) {
      window.clearTimeout(celebrationTimeoutRef.current);
      celebrationTimeoutRef.current = null;
    }

    if (highlightTimeoutRef.current) {
      window.clearTimeout(highlightTimeoutRef.current);
      highlightTimeoutRef.current = null;
    }
  };

  useEffect(() => {
    return () => {
      clearAnimationTimeouts();
      selectionLockRef.current = false;
    };
  }, []);

  const selectedRouteIndex = useMemo(() => {
    if (!selectedVariant) {
      return null;
    }

    const index = variants.findIndex((variant) => variant.id === selectedVariant.id);
    return index >= 0 ? index + 1 : null;
  }, [selectedVariant, variants]);

  const handleSelect = async (variantId: string) => {
    const alreadySelected = variantId === selectedVariant?.id;

    if (
      isLoading ||
      selectionLockRef.current ||
      pendingVariantId !== null ||
      alreadySelected
    ) {
      return;
    }

    selectionLockRef.current = true;
    clearAnimationTimeouts();

    setPendingVariantId(variantId);
    setCelebratingVariantId(null);
    setHighlightedVariantId(null);

    try {
      await onSelect(variantId);

      setPendingVariantId(null);
      setCelebratingVariantId(variantId);

      celebrationTimeoutRef.current = window.setTimeout(() => {
        setCelebratingVariantId(null);
        setHighlightedVariantId(variantId);
        celebrationTimeoutRef.current = null;

        highlightTimeoutRef.current = window.setTimeout(() => {
          setHighlightedVariantId(null);
          highlightTimeoutRef.current = null;
          selectionLockRef.current = false;
        }, FINAL_HIGHLIGHT_MS);
      }, FINAL_CELEBRATION_MS);
    } catch (error) {
      setPendingVariantId(null);
      setCelebratingVariantId(null);
      setHighlightedVariantId(null);
      selectionLockRef.current = false;
      throw error;
    }
  };

  return (
    <SectionCard
      title={t("variantsList.title")}
      description={t("variantsList.description")}
    >
      {variants.length === 0 ? (
        <EmptyState
          title={t("variantsList.empty.title")}
          description={t("variantsList.empty.description")}
        />
      ) : (
        <div className="grid gap-5">
          <div
            className={[
              "variants-topbar rounded-[1.45rem] border border-white/8 bg-slate-950/20 px-4 py-4",
              selectedVariant ? "variants-topbar--selected" : "",
            ]
              .filter(Boolean)
              .join(" ")}
          >
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div className="flex flex-wrap items-center gap-2">
                <span className="aero-badge">{t("variantsList.badges.branchStage")}</span>
                <span className="aero-badge">
                  {t("variantsList.badges.alternatives", { count: variants.length })}
                </span>
                <span className="aero-badge">{t("variantsList.badges.guidedSelection")}</span>
                {selectedVariant ? (
                  <span className="aero-badge aero-badge--success">
                    {t("variantCard.selectedBadge")}
                  </span>
                ) : null}
              </div>

              <div className="rounded-full border border-white/8 bg-white/[0.03] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">
                {t("variantsList.routesSlide")}
              </div>
            </div>

            <div className="mt-4 grid gap-3 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-start">
              <p className="text-sm leading-7 text-slate-300/84">
                {t("variantsList.mainDescription")}
              </p>

              <div className="variants-topbar__state rounded-[1.1rem] border border-white/8 bg-slate-950/22 px-4 py-3 text-sm text-slate-300">
                <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-500">
                  {t("variantsList.currentStateLabel")}
                </p>

                <p className="mt-2 font-medium text-slate-100">
                  {selectedVariant
                    ? t("variantsList.currentState.selected")
                    : t("variantsList.currentState.waiting")}
                </p>

                {selectedVariant && selectedRouteIndex ? (
                  <p className="mt-2 text-xs leading-6 text-emerald-100/82">
                    {t("variantCard.routeBadge", { index: selectedRouteIndex })}
                  </p>
                ) : null}
              </div>
            </div>

            <div className="variants-topbar__glow" />
          </div>

          <div className="variants-stage grid gap-4 md:grid-cols-2 2xl:grid-cols-3">
            {variants.map((variant, index) => (
              <VariantCard
                key={variant.id}
                variant={variant}
                isLoading={isLoading}
                isSelecting={pendingVariantId === variant.id}
                isCelebrating={celebratingVariantId === variant.id}
                isHighlighted={highlightedVariantId === variant.id}
                onSelect={handleSelect}
                index={index}
              />
            ))}
          </div>
        </div>
      )}
    </SectionCard>
  );
}