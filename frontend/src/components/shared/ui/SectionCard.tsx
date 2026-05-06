import type { PropsWithChildren, ReactNode } from "react";
import { useTranslation } from "react-i18next";

type SectionCardProps = PropsWithChildren<{
  title: string;
  description?: string;
  action?: ReactNode;
}>;

export default function SectionCard({
  title,
  description,
  action,
  children,
}: SectionCardProps) {
  const { t } = useTranslation();

  return (
    <section className="section-card-shell rounded-[1.9rem] p-6 md:p-7">
      <div className="section-card-shell__ambient section-card-shell__ambient--one" />
      <div className="section-card-shell__ambient section-card-shell__ambient--two" />
      <div className="section-card-shell__grid" />
      <div className="section-card-shell__beam" />
      <div className="section-card-shell__line" />

      <div className="relative z-[1]">
        <div className="section-card-shell__header flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
          <div className="max-w-3xl">
            <div className="section-card-shell__eyebrow-wrap mb-3 flex flex-wrap items-center gap-2">
              <span className="section-card-shell__eyebrow">
                {t("sectionCard.eyebrowPrimary")}
              </span>
              <span className="section-card-shell__eyebrow section-card-shell__eyebrow--muted">
                {t("sectionCard.eyebrowSecondary")}
              </span>
            </div>

            <h2 className="aero-section-title text-lg font-semibold leading-tight md:text-xl">
              {title}
            </h2>

            {description ? (
              <p className="aero-section-description mt-2 max-w-3xl text-sm leading-7">
                {description}
              </p>
            ) : null}
          </div>

          {action ? (
            <div className="section-card-shell__action shrink-0 self-start xl:ml-6">
              {action}
            </div>
          ) : null}
        </div>

        <div className="section-card-shell__content mt-6">{children}</div>
      </div>
    </section>
  );
}