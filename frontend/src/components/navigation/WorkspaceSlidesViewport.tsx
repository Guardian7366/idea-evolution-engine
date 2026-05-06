import type { ReactNode } from "react";
import { useTranslation } from "react-i18next";
import type { WorkspaceSlideId } from "../../shared/utils/workspaceSlides";

type WorkspaceSlidesViewportItem = {
  id: WorkspaceSlideId;
  content: ReactNode;
};

type WorkspaceSlidesViewportProps = {
  slides: WorkspaceSlidesViewportItem[];
  activeSlideId: WorkspaceSlideId;
  onPrevious: () => void;
  onNext: () => void;
};

function ArrowButton({
  direction,
  onClick,
}: {
  direction: "left" | "right";
  onClick: () => void;
}) {
  const { t } = useTranslation();
  const isLeft = direction === "left";

  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={isLeft ? t("viewport.previousSlide") : t("viewport.nextSlide")}
      className={[
        "workspace-slides-arrow group hidden lg:flex",
        isLeft
          ? "workspace-slides-arrow--left"
          : "workspace-slides-arrow--right",
      ].join(" ")}
    >
      <span className="workspace-slides-arrow__glow" />

      <svg viewBox="0 0 24 24" className="relative h-7 w-7" aria-hidden="true">
        {isLeft ? (
          <path
            d="M14.5 5.5L8 12l6.5 6.5"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.9"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        ) : (
          <path
            d="M9.5 5.5L16 12l-6.5 6.5"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.9"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        )}
      </svg>
    </button>
  );
}

export default function WorkspaceSlidesViewport({
  slides,
  activeSlideId,
  onPrevious,
  onNext,
}: WorkspaceSlidesViewportProps) {
  const { t } = useTranslation();

  return (
    <section className="workspace-slides-viewport relative" aria-label={t("viewport.ariaLabel")}>
      <ArrowButton direction="left" onClick={onPrevious} />
      <ArrowButton direction="right" onClick={onNext} />

      <div className="relative">
        {slides.map((slide) => {
          const isActive = slide.id === activeSlideId;

          return (
            <div
              key={slide.id}
              hidden={!isActive}
              aria-hidden={!isActive}
              data-active={isActive ? "true" : "false"}
              className={[
                "transition-all duration-500",
                isActive ? "animate-[fadeSlideIn_420ms_ease]" : "",
              ].join(" ")}
            >
              {slide.content}
            </div>
          );
        })}
      </div>

      <div className="mt-5 flex items-center justify-center gap-2 lg:hidden">
        <button
          type="button"
          onClick={onPrevious}
          className="inline-flex items-center gap-2 rounded-full border border-cyan-300/16 bg-slate-950/40 px-4 py-2 text-sm text-slate-100 backdrop-blur-xl transition hover:border-cyan-300/30 hover:bg-slate-900/60"
        >
          <svg viewBox="0 0 24 24" className="h-4 w-4" aria-hidden="true">
            <path
              d="M14.5 5.5L8 12l6.5 6.5"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.9"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          {t("viewport.previous")}
        </button>

        <button
          type="button"
          onClick={onNext}
          className="inline-flex items-center gap-2 rounded-full border border-cyan-300/16 bg-slate-950/40 px-4 py-2 text-sm text-slate-100 backdrop-blur-xl transition hover:border-cyan-300/30 hover:bg-slate-900/60"
        >
          {t("viewport.next")}
          <svg viewBox="0 0 24 24" className="h-4 w-4" aria-hidden="true">
            <path
              d="M9.5 5.5L16 12l-6.5 6.5"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.9"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
      </div>
    </section>
  );
}