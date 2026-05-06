import { useEffect, useMemo, useState } from "react";

export type WorkspaceSectionIconKey =
  | "home"
  | "controls"
  | "idea"
  | "variants"
  | "transform"
  | "history"
  | "analysis"
  | "synthesis";

export type WorkspaceSectionItem = {
  id: string;
  label: string;
  shortLabel: string;
  icon: WorkspaceSectionIconKey;
};

type WorkspaceSectionSidebarProps = {
  items: WorkspaceSectionItem[];
};

function getHeaderMetrics() {
  const header = document.querySelector(".app-header") as HTMLElement | null;

  const fallbackCompactTop = 14;
  const fallbackScrollOffset = 118;

  if (!header) {
    return {
      headerHeight: fallbackScrollOffset,
      topOffset: fallbackScrollOffset,
      sidebarTop: fallbackCompactTop,
    };
  }

  const rect = header.getBoundingClientRect();
  const visibleBottom = Math.max(rect.bottom, 0);

  // Cuando la cabecera grande aún está visible, la barra se coloca debajo.
  // Cuando el usuario baja, la barra sube y se queda cerca del top.
  const compactTop = 14;
  const dynamicSidebarTop = Math.max(Math.min(visibleBottom + 8, 132), compactTop);

  // Offset de scroll para que al navegar nunca tape la sección.
  const topOffset = Math.max(visibleBottom + 14, 92);

  return {
    headerHeight: header.offsetHeight,
    topOffset,
    sidebarTop: dynamicSidebarTop,
  };
}

function scrollToSection(sectionId: string) {
  const element = document.getElementById(sectionId);

  if (!element) {
    return;
  }

  const { topOffset } = getHeaderMetrics();
  const elementTop = element.getBoundingClientRect().top + window.scrollY;
  const targetTop = Math.max(elementTop - topOffset, 0);

  window.scrollTo({
    top: targetTop,
    behavior: "smooth",
  });
}

function SidebarIcon({ icon }: { icon: WorkspaceSectionIconKey }) {
  switch (icon) {
    case "home":
      return (
        <svg viewBox="0 0 24 24" className="workspace-sidebar__icon-svg" aria-hidden="true">
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
        <svg viewBox="0 0 24 24" className="workspace-sidebar__icon-svg" aria-hidden="true">
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
        <svg viewBox="0 0 24 24" className="workspace-sidebar__icon-svg" aria-hidden="true">
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
        <svg viewBox="0 0 24 24" className="workspace-sidebar__icon-svg" aria-hidden="true">
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
        <svg viewBox="0 0 24 24" className="workspace-sidebar__icon-svg" aria-hidden="true">
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
        <svg viewBox="0 0 24 24" className="workspace-sidebar__icon-svg" aria-hidden="true">
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
        <svg viewBox="0 0 24 24" className="workspace-sidebar__icon-svg" aria-hidden="true">
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
        <svg viewBox="0 0 24 24" className="workspace-sidebar__icon-svg" aria-hidden="true">
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

export default function WorkspaceSectionSidebar({
  items,
}: WorkspaceSectionSidebarProps) {
  const [activeSectionId, setActiveSectionId] = useState(items[0]?.id ?? "");

  const sectionIds = useMemo(() => items.map((item) => item.id), [items]);

  useEffect(() => {
    const syncLayoutVars = () => {
      const { headerHeight, sidebarTop } = getHeaderMetrics();

      document.documentElement.style.setProperty("--app-header-height", `${headerHeight}px`);
      document.documentElement.style.setProperty("--workspace-sidebar-top", `${sidebarTop}px`);
    };

    const handleScroll = () => {
      syncLayoutVars();

      const { topOffset } = getHeaderMetrics();
      const viewportReference = topOffset + 36;
      let currentSectionId = sectionIds[0] ?? "";

      for (const sectionId of sectionIds) {
        const element = document.getElementById(sectionId);

        if (!element) {
          continue;
        }

        const rect = element.getBoundingClientRect();

        if (rect.top <= viewportReference) {
          currentSectionId = sectionId;
        }
      }

      setActiveSectionId(currentSectionId);
    };

    syncLayoutVars();
    handleScroll();

    window.addEventListener("resize", syncLayoutVars);
    window.addEventListener("resize", handleScroll);
    window.addEventListener("scroll", handleScroll, { passive: true });

    return () => {
      window.removeEventListener("resize", syncLayoutVars);
      window.removeEventListener("resize", handleScroll);
      window.removeEventListener("scroll", handleScroll);
    };
  }, [sectionIds]);

  return (
    <aside className="workspace-sidebar" aria-label="Navegación de secciones">
      <div className="workspace-sidebar__shell">
        <div className="workspace-sidebar__header">
          <span className="workspace-sidebar__eyebrow">Quick nav</span>
          <p className="workspace-sidebar__title">Secciones</p>
        </div>

        <nav
          className="workspace-sidebar__nav"
          style={{ gridTemplateRows: `repeat(${items.length}, minmax(0, 1fr))` }}
        >
          {items.map((item, index) => {
            const isActive = item.id === activeSectionId;

            return (
              <button
                key={item.id}
                type="button"
                className={[
                  "workspace-sidebar__item",
                  isActive ? "workspace-sidebar__item--active" : "",
                ]
                  .filter(Boolean)
                  .join(" ")}
                onClick={() => scrollToSection(item.id)}
                aria-current={isActive ? "true" : "false"}
                title={item.label}
              >
                <span className="workspace-sidebar__icon" aria-hidden="true">
                  <span className="workspace-sidebar__icon-ring" />
                  <SidebarIcon icon={item.icon} />
                </span>

                <span className="workspace-sidebar__meta">
                  <span className="workspace-sidebar__index">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <span className="workspace-sidebar__text">{item.shortLabel}</span>
                </span>
              </button>
            );
          })}
        </nav>
      </div>
    </aside>
  );
}