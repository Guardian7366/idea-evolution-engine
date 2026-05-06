import { useTranslation } from "react-i18next";
import Button from "../../../components/shared/ui/Button";
import SectionCard from "../../../components/shared/ui/SectionCard";

type FlowStatusPanelProps = {
  sessionId: string | null;
  ideaId: string | null;
  activeVersionId: string | null;
  isLoading: boolean;
  error: string | null;
  onClearWorkspace: () => void;
};

type StatusItemProps = {
  label: string;
  value: string | null;
  emptyText: string;
};

function StatusItem({ label, value, emptyText }: StatusItemProps) {
  return (
    <div className="status-item-card rounded-[1.45rem] p-4">
      <div className="relative z-[1]">
        <p className="aero-status-label text-[11px] font-semibold uppercase tracking-[0.22em]">
          {label}
        </p>

        <p className="aero-status-value mt-3 break-all text-sm leading-7">
          {value ?? emptyText}
        </p>
      </div>

      <div className="status-item-card__shine" />
    </div>
  );
}

export default function FlowStatusPanel({
  sessionId,
  ideaId,
  activeVersionId,
  isLoading,
  error,
  onClearWorkspace,
}: FlowStatusPanelProps) {
  const { t } = useTranslation();
  const hasOperationalFlow = Boolean(sessionId || ideaId || activeVersionId);

  return (
    <SectionCard
      title={t("flowStatus.title")}
      description={t("flowStatus.description")}
      action={
        <Button
          type="button"
          variant="secondary"
          onClick={onClearWorkspace}
          disabled={isLoading}
        >
          {t("flowStatus.clearWorkspace")}
        </Button>
      }
    >
      <div className="rounded-[1.45rem] border border-white/8 bg-slate-950/18 p-4 md:p-5">
        <div className="mb-4 flex flex-wrap items-start justify-between gap-3">
          <div className="flex flex-wrap items-center gap-2">
            <span className="aero-badge">{t("flowStatus.badges.status")}</span>
            <span
              className={
                isLoading
                  ? "aero-badge aero-badge--loading"
                  : "aero-badge aero-badge--success"
              }
            >
              {isLoading ? t("flowStatus.states.processing") : t("flowStatus.states.ready")}
            </span>
          </div>

          <div className="rounded-full border border-white/8 bg-white/[0.03] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">
            {t("flowStatus.controlBoard")}
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <StatusItem
            label={t("flowStatus.items.session.label")}
            value={sessionId}
            emptyText={t("flowStatus.items.session.empty")}
          />
          <StatusItem
            label={t("flowStatus.items.idea.label")}
            value={ideaId}
            emptyText={t("flowStatus.items.idea.empty")}
          />
          <StatusItem
            label={t("flowStatus.items.activeVersion.label")}
            value={activeVersionId}
            emptyText={t("flowStatus.items.activeVersion.empty")}
          />
        </div>

        <div className="flow-status-bar mt-4 flex flex-wrap items-center justify-between gap-3 rounded-[1.35rem] p-4">
          <div className="max-w-2xl">
            <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
              {t("flowStatus.operationalStateTitle")}
            </p>
            <p className="mt-2 text-sm leading-6 text-slate-300/82">
              {hasOperationalFlow
                ? t("flowStatus.operationalMessages.active")
                : t("flowStatus.operationalMessages.empty")}
            </p>
          </div>

          <span
            className={
              isLoading
                ? "aero-badge aero-badge--loading"
                : "aero-badge aero-badge--success"
            }
          >
            {isLoading ? t("flowStatus.states.processing") : t("flowStatus.states.ready")}
          </span>
        </div>

        {error ? (
          <div className="aero-error mt-4 rounded-2xl p-4 text-sm leading-7">{error}</div>
        ) : null}
      </div>
    </SectionCard>
  );
}