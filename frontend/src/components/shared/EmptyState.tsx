import { useTranslation } from "react-i18next";

type EmptyStateProps = {
  title: string;
  description: string;
};

export default function EmptyState({ title, description }: EmptyStateProps) {
  const { t } = useTranslation();

  return (
    <div className="empty-state-shell rounded-[1.65rem] p-5 md:p-6 shadow-[0_10px_24px_rgba(0,0,0,0.14)]">
      <div className="relative z-[1]">
        <div className="mb-3 flex flex-wrap items-center gap-2">
          <span className="aero-badge empty-state-shell__badge">
            {t("emptyState.initialState")}
          </span>
          <span className="aero-badge">{t("emptyState.waitingState")}</span>
        </div>

        <div className="max-w-3xl">
          <h3 className="text-base font-semibold tracking-[-0.02em] text-slate-100 md:text-[1.02rem]">
            {title}
          </h3>

          <p className="mt-3 text-sm leading-7 text-slate-300/84">{description}</p>
        </div>
      </div>

      <div className="empty-state-shell__orb empty-state-shell__orb--one" />
      <div className="empty-state-shell__orb empty-state-shell__orb--two" />
      <div className="empty-state-shell__line" />
    </div>
  );
}