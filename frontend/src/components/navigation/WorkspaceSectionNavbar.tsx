import { useTranslation } from "react-i18next";
import type { WorkspaceSlideIconKey, WorkspaceSlideId } from "../../shared/utils/workspaceSlides";

type WorkspaceSectionNavbarItem = {
  id: WorkspaceSlideId;
  label: string;
  shortLabel: string;
  icon: WorkspaceSlideIconKey;
  enabled: boolean;
};

type WorkspaceSectionNavbarProps = {
  items: WorkspaceSectionNavbarItem[];
  activeSlideId: WorkspaceSlideId;
  onSelect: (slideId: WorkspaceSlideId) => void;
};

function NavbarIcon({ icon }: { icon: WorkspaceSlideIconKey }) {
  switch (icon) {
    case "home":
      return (
        <svg viewBox="0 0 24 24" className="h-[18px] w-[18px]" aria-hidden="true">
          <path
            d="M4 11.5L12 5l8 6.5"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.9"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <path
            d="M7.5 10.5V19h9v-8.5"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.9"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      );

    case "controls":
      return (
        <svg viewBox="0 0 24 24" className="h-[18px] w-[18px]" aria-hidden="true">
          <path
            d="M5 7h14M5 12h14M5 17h14"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.9"
            strokeLinecap="round"
          />
          <circle cx="9" cy="7" r="2" fill="currentColor" />
          <circle cx="15" cy="12" r="2" fill="currentColor" />
          <circle cx="11" cy="17" r="2" fill="currentColor" />
        </svg>
      );

    case "idea":
      return (
        <svg viewBox="0 0 24 24" className="h-[18px] w-[18px]" aria-hidden="true">
          <path
            d="M12 4.5a6 6 0 0 0-3.8 10.65c.8.68 1.3 1.46 1.48 2.35h4.64c.18-.89.68-1.67 1.48-2.35A6 6 0 0 0 12 4.5Z"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinejoin="round"
          />
          <path
            d="M9.8 19h4.4M10.3 21h3.4"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
          />
        </svg>
      );

    case "variants":
      return (
        <svg viewBox="0 0 24 24" className="h-[18px] w-[18px]" aria-hidden="true">
          <path
            d="M7 6h6a4 4 0 0 1 4 4v1"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.9"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <path
            d="M17 8l2.5 3L17 14"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.9"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <path
            d="M17 18H11a4 4 0 0 1-4-4v-1"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.9"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <path
            d="M7 16l-2.5-3L7 10"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.9"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      );

    case "transform":
      return (
        <svg viewBox="0 0 24 24" className="h-[18px] w-[18px]" aria-hidden="true">
          <path
            d="M12 4l1.4 3.6L17 9l-3.6 1.4L12 14l-1.4-3.6L7 9l3.6-1.4L12 4Z"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinejoin="round"
          />
          <path
            d="M18.5 14.5l.8 2.1 2.2.8-2.2.8-.8 2.1-.8-2.1-2.2-.8 2.2-.8.8-2.1Z"
            fill="currentColor"
          />
          <path
            d="M6 15.5l.5 1.3 1.3.5-1.3.5-.5 1.3-.5-1.3-1.3-.5 1.3-.5.5-1.3Z"
            fill="currentColor"
          />
        </svg>
      );

    case "history":
      return (
        <svg viewBox="0 0 24 24" className="h-[18px] w-[18px]" aria-hidden="true">
          <circle cx="6" cy="6" r="2" fill="none" stroke="currentColor" strokeWidth="1.8" />
          <circle cx="18" cy="12" r="2" fill="none" stroke="currentColor" strokeWidth="1.8" />
          <circle cx="6" cy="18" r="2" fill="none" stroke="currentColor" strokeWidth="1.8" />
          <path
            d="M8 7.2l8 3.6M8 16.8l8-3.6"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
          />
        </svg>
      );

    case "analysis":
      return (
        <svg viewBox="0 0 24 24" className="h-[18px] w-[18px]" aria-hidden="true">
          <circle cx="10.5" cy="10.5" r="5" fill="none" stroke="currentColor" strokeWidth="1.8" />
          <path
            d="M14.2 14.2L19 19"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.9"
            strokeLinecap="round"
          />
          <path
            d="M10.5 8v5M8 10.5h5"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.7"
            strokeLinecap="round"
          />
        </svg>
      );

    case "synthesis":
      return (
        <svg viewBox="0 0 24 24" className="h-[18px] w-[18px]" aria-hidden="true">
          <path
            d="M12 4l2 4 4 .6-3 3 .7 4.4L12 14l-3.7 2 .7-4.4-3-3L10 8l2-4Z"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinejoin="round"
          />
        </svg>
      );

    default:
      return null;
  }
}

export default function WorkspaceSectionNavbar({
  items,
  activeSlideId,
  onSelect,
}: WorkspaceSectionNavbarProps) {
  const { t } = useTranslation();

  return (
    <section
      className="sticky top-3 z-30 mb-6 md:mb-7"
      aria-label={t("workspaceNavbar.ariaLabel")}
    >
      <div className="aero-panel overflow-hidden rounded-[1.7rem] border border-cyan-300/12 bg-slate-950/48 px-3 py-3 shadow-[0_18px_60px_rgba(2,12,27,0.34)] backdrop-blur-xl md:px-4">
        <div className="mb-3 flex flex-wrap items-center justify-between gap-2 px-1">
          <div className="flex flex-wrap items-center gap-2">
            <span className="aero-badge">{t("workspaceNavbar.deckBadge")}</span>
            <span className="aero-badge aero-badge--success">
              {t("workspaceNavbar.linkedSlidesBadge", { count: items.length })}
            </span>
          </div>

          <p className="text-[11px] font-medium uppercase tracking-[0.24em] text-cyan-100/55">
            {t("workspaceNavbar.orchestrationLabel")}
          </p>
        </div>

        <nav className="grid grid-cols-2 gap-2 md:grid-cols-4 xl:grid-cols-8">
          {items.map((item, index) => {
            const isActive = item.id === activeSlideId;

            return (
              <button
                key={item.id}
                type="button"
                onClick={() => {
                  if (!item.enabled) {
                    return;
                  }

                  onSelect(item.id);
                }}
                disabled={!item.enabled}
                aria-current={isActive ? "page" : undefined}
                aria-label={item.label}
                title={item.label}
                className={[
                  "group relative flex min-h-[74px] flex-col items-start justify-between rounded-[1.3rem] border px-3 py-3 text-left transition-all duration-300",
                  item.enabled
                    ? "border-cyan-300/12 bg-slate-950/44 text-slate-100 hover:-translate-y-0.5 hover:border-cyan-300/30 hover:bg-slate-900/62"
                    : "cursor-not-allowed border-white/8 bg-slate-950/22 text-slate-500 opacity-65",
                  isActive
                    ? "border-cyan-300/45 bg-[linear-gradient(135deg,rgba(27,125,255,0.34),rgba(55,229,210,0.16),rgba(7,15,35,0.9))] shadow-[0_0_0_1px_rgba(88,228,255,0.12),0_16px_36px_rgba(0,100,255,0.24),0_0_24px_rgba(95,224,255,0.1)]"
                    : "",
                ].join(" ")}
              >
                <div className="flex w-full items-start justify-between gap-2">
                  <span
                    className={[
                      "inline-flex h-9 w-9 items-center justify-center rounded-full border transition-all duration-300",
                      isActive
                        ? "border-cyan-200/50 bg-cyan-300/18 text-cyan-50 shadow-[0_0_18px_rgba(102,227,255,0.16)]"
                        : "border-white/10 bg-white/5 text-slate-200/85",
                    ].join(" ")}
                  >
                    <NavbarIcon icon={item.icon} />
                  </span>

                  <span className="text-[10px] font-semibold uppercase tracking-[0.22em] text-slate-300/52">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                </div>

                <div className="mt-3 min-w-0">
                  <p className="truncate text-sm font-semibold">{item.shortLabel}</p>
                  <p className="mt-1 text-[11px] leading-5 text-slate-300/62">
                    {item.enabled
                      ? t("workspaceNavbar.available")
                      : t("workspaceNavbar.blockedByFlow")}
                  </p>
                </div>

                {isActive ? (
                  <span className="pointer-events-none absolute inset-x-3 bottom-1 h-px rounded-full bg-cyan-200/60" />
                ) : null}
              </button>
            );
          })}
        </nav>
      </div>
    </section>
  );
}