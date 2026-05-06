import { useEffect, useRef, useState } from "react";
import type { FormEvent } from "react";
import { useTranslation } from "react-i18next";
import Button from "../../../components/shared/ui/Button";
import type { IdeaResponse, SessionResponse } from "../../../types/idea";

type IdeaInputSectionProps = {
  session: SessionResponse | null;
  idea: IdeaResponse | null;
  hasSession: boolean;
  isLoading: boolean;
  onCreateSession: (title: string) => Promise<void>;
  onCreateIdea: (payload: { title: string; content: string }) => Promise<void>;
};

function getDefaultSessionTitle(isEnglish: boolean): string {
  return isEnglish ? "Initial working session" : "Sesión inicial de trabajo";
}

function getDefaultIdeaTitle(isEnglish: boolean): string {
  return isEnglish ? "Main idea" : "Idea principal";
}

function getDefaultIdeaContent(isEnglish: boolean): string {
  return isEnglish
    ? "A web platform to evolve simple ideas into clearer, comparable, and more structured proposals."
    : "Una plataforma web para evolucionar ideas simples en propuestas más claras, comparables y estructuradas.";
}

function StepConnector() {
  return (
    <div
      className="pointer-events-none absolute left-1/2 top-1/2 z-0 hidden h-[78%] w-16 -translate-x-1/2 -translate-y-1/2 xl:block"
      aria-hidden="true"
    >
      <div className="relative h-full w-full">
        <div className="absolute left-1/2 top-4 h-[calc(100%-2rem)] w-px -translate-x-1/2 bg-[linear-gradient(180deg,rgba(146,234,255,0.08),rgba(146,255,201,0.2),rgba(146,234,255,0.08))]" />
        <div className="absolute left-1/2 top-1/2 h-28 w-28 -translate-x-1/2 -translate-y-1/2 rounded-full bg-[radial-gradient(circle,rgba(113,236,255,0.14),transparent_70%)] blur-2xl" />
        <div className="absolute left-1/2 top-[18%] h-3.5 w-3.5 -translate-x-1/2 rounded-full border border-cyan-200/20 bg-cyan-200/20 shadow-[0_0_18px_rgba(103,232,249,0.18)]" />
        <div className="absolute left-1/2 top-[50%] h-4 w-4 -translate-x-1/2 -translate-y-1/2 rounded-full border border-emerald-200/18 bg-emerald-200/16 shadow-[0_0_22px_rgba(134,255,182,0.18)]" />
        <div className="absolute left-1/2 bottom-[18%] h-3.5 w-3.5 -translate-x-1/2 rounded-full border border-cyan-200/20 bg-cyan-200/18 shadow-[0_0_18px_rgba(103,232,249,0.16)]" />
      </div>
    </div>
  );
}

function StageHint({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  const { t } = useTranslation();

  return (
    <div className="rounded-[1.2rem] border border-white/8 bg-slate-950/22 p-3">
      <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
        {t("ideaInput.contextLabel")}
      </p>
      <p className="mt-2 text-sm leading-6 text-slate-300/80">
        <span className="font-semibold text-slate-100">{title}: </span>
        {description}
      </p>
    </div>
  );
}

function IdeaBirthOverlay({
  logoSrc,
  title,
}: {
  logoSrc: string;
  title: string;
}) {
  return (
    <div className="idea-birth-overlay idea-birth-overlay--visible" aria-hidden="true">
      <div className="idea-birth-overlay__veil" />
      <div className="idea-birth-overlay__ring idea-birth-overlay__ring--one" />
      <div className="idea-birth-overlay__ring idea-birth-overlay__ring--two" />
      <div className="idea-birth-overlay__pulse" />

      <div className="idea-birth-overlay__core">
        <div className="idea-birth-overlay__logo-shell">
          <img
            src={logoSrc}
            alt={title}
            className="idea-birth-overlay__logo"
          />
        </div>

        <div className="idea-birth-overlay__spark" />
        <p className="idea-birth-overlay__text">{title}</p>
      </div>
    </div>
  );
}

export default function IdeaInputSection({
  session,
  idea,
  hasSession,
  isLoading,
  onCreateSession,
  onCreateIdea,
}: IdeaInputSectionProps) {
  const { t, i18n } = useTranslation();
  const isEnglish = i18n.language === "en";

  const [sessionTitle, setSessionTitle] = useState(() =>
  getDefaultSessionTitle(isEnglish),
  );

  const [ideaTitle, setIdeaTitle] = useState(() =>
    getDefaultIdeaTitle(isEnglish),
  );

  const [ideaContent, setIdeaContent] = useState(() =>
    getDefaultIdeaContent(isEnglish),
  );

  const [isIdeaCelebrating, setIsIdeaCelebrating] = useState(false);
  const [ideaJustCreated, setIdeaJustCreated] = useState(false);
  const [celebrationKey, setCelebrationKey] = useState(0);

  const celebrationTimeoutRef = useRef<number | null>(null);

  useEffect(() => {
    if (session) {
      setSessionTitle(session.title?.trim() || "");
      return;
    }

    setSessionTitle(getDefaultSessionTitle(isEnglish));
  }, [session?.id, session?.title, isEnglish]);

  useEffect(() => {
    if (idea) {
      setIdeaTitle(idea.title?.trim() || "");
      setIdeaContent(idea.content);
      return;
    }

    setIdeaTitle(getDefaultIdeaTitle(isEnglish));
    setIdeaContent(getDefaultIdeaContent(isEnglish));
  }, [idea?.id, idea?.title, idea?.content, isEnglish]);

  const handleSessionSubmit = async (event: FormEvent) => {
    event.preventDefault();
    await onCreateSession(sessionTitle);
  };

  const handleIdeaSubmit = async (event: FormEvent) => {
    event.preventDefault();

    if (celebrationTimeoutRef.current !== null) {
      window.clearTimeout(celebrationTimeoutRef.current);
      celebrationTimeoutRef.current = null;
    }

    try {
      await onCreateIdea({
        title: ideaTitle,
        content: ideaContent,
      });

      setCelebrationKey((prev) => prev + 1);
      setIdeaJustCreated(true);
      setIsIdeaCelebrating(true);

      celebrationTimeoutRef.current = window.setTimeout(() => {
        setIsIdeaCelebrating(false);
        setIdeaJustCreated(false);
        celebrationTimeoutRef.current = null;
      }, 1150);
    } catch (error) {
      setIsIdeaCelebrating(false);
      setIdeaJustCreated(false);
      throw error;
    }
  };

  return (
    <section className="relative grid gap-6 xl:grid-cols-2 xl:items-stretch">
      <StepConnector />

      <form
        onSubmit={handleSessionSubmit}
        className="idea-form-panel idea-form-panel--session relative flex min-h-full flex-col rounded-[1.85rem] p-6 md:p-7"
      >
        <div className="relative z-[1] flex h-full flex-col">
          <div className="mb-5 flex flex-wrap items-start justify-between gap-4">
            <div className="max-w-xl">
              <div className="mb-3 flex flex-wrap items-center gap-2">
                <span className="aero-badge">{t("ideaInput.session.badges.container")}</span>
                <span className="aero-badge">{t("ideaInput.session.badges.stage")}</span>
              </div>

              <h2 className="text-xl font-semibold tracking-[-0.02em] text-slate-50 md:text-[1.35rem]">
                {t("ideaInput.session.title")}
              </h2>

              <p className="mt-2 text-sm leading-7 text-slate-300/82">
                {t("ideaInput.session.description")}
              </p>
            </div>

            <div className="rounded-full border border-cyan-200/12 bg-cyan-200/5 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.2em] text-cyan-100/80">
              {t("ideaInput.session.status")}
            </div>
          </div>

          <div className="grid gap-4">
            <div className="rounded-[1.45rem] border border-white/8 bg-slate-950/22 p-4">
              <label className="aero-label mb-2 block">
                {t("ideaInput.session.fields.titleLabel")}
              </label>
              <input
                type="text"
                value={sessionTitle}
                onChange={(e) => setSessionTitle(e.target.value)}
                className="aero-input px-4 py-3 text-sm"
                placeholder={t("ideaInput.session.fields.titlePlaceholder")}
                disabled={isLoading}
              />
            </div>

            <StageHint
              title={t("ideaInput.session.hint.title")}
              description={t("ideaInput.session.hint.description")}
            />
          </div>

          <div className="mt-5 flex-1" />

          <div className="mt-6 flex flex-wrap items-center justify-between gap-3">
            <p className="max-w-md text-xs leading-6 text-slate-400">
              {t("ideaInput.session.footerText")}
            </p>

            <Button type="submit" disabled={isLoading || !sessionTitle.trim()}>
              {t("ideaInput.session.submit")}
            </Button>
          </div>
        </div>

        <div className="idea-form-panel__glow" />
      </form>

      <form
        onSubmit={handleIdeaSubmit}
        className={[
          "idea-form-panel",
          "idea-form-panel--idea",
          "idea-form-panel--idea-premium",
          "relative flex min-h-full flex-col rounded-[1.85rem] p-6 md:p-7",
          hasSession ? "idea-form-panel--idea-ready" : "",
          ideaJustCreated ? "idea-form-panel--idea-created" : "",
        ]
          .filter(Boolean)
          .join(" ")}
      >
        <div className="idea-form-panel__seed-grid" />
        <div className="idea-form-panel__seed-orb idea-form-panel__seed-orb--one" />
        <div className="idea-form-panel__seed-orb idea-form-panel__seed-orb--two" />
        <div className="idea-form-panel__seed-beam" />

        {isIdeaCelebrating ? (
          <IdeaBirthOverlay
            key={celebrationKey}
            logoSrc="/favicon.png"
            title={t("ideaInput.idea.title")}
          />
        ) : null}

        <div className="relative z-[1] flex h-full flex-col">
          <div className="mb-5 flex flex-wrap items-start justify-between gap-4">
            <div className="max-w-xl">
              <div className="mb-3 flex flex-wrap items-center gap-2">
                <span className="aero-badge aero-badge--success">
                  {t("ideaInput.idea.badges.seed")}
                </span>
                <span className="aero-badge">{t("ideaInput.idea.badges.stage")}</span>
              </div>

              <h2 className="text-xl font-semibold tracking-[-0.02em] text-slate-50 md:text-[1.35rem]">
                {t("ideaInput.idea.title")}
              </h2>

              <p className="mt-2 text-sm leading-7 text-slate-300/82">
                {t("ideaInput.idea.description")}
              </p>
            </div>

            <div className="rounded-full border border-emerald-200/12 bg-emerald-200/5 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.2em] text-emerald-100/80">
              {t("ideaInput.idea.status")}
            </div>
          </div>

          <div className="grid gap-4">
            <div className="rounded-[1.45rem] border border-white/8 bg-slate-950/22 p-4">
              <label className="aero-label mb-2 block">
                {t("ideaInput.idea.fields.titleLabel")}
              </label>
              <input
                type="text"
                value={ideaTitle}
                onChange={(e) => setIdeaTitle(e.target.value)}
                className="aero-input px-4 py-3 text-sm"
                placeholder={t("ideaInput.idea.fields.titlePlaceholder")}
                disabled={!hasSession || isLoading}
              />
            </div>

            <div className="idea-content-shell rounded-[1.45rem] border border-white/8 bg-slate-950/22 p-4">
              <label className="aero-label mb-2 block">
                {t("ideaInput.idea.fields.contentLabel")}
              </label>
              <textarea
                value={ideaContent}
                onChange={(e) => setIdeaContent(e.target.value)}
                rows={7}
                className="aero-textarea min-h-[210px] px-4 py-3 text-sm leading-6"
                placeholder={t("ideaInput.idea.fields.contentPlaceholder")}
                disabled={!hasSession || isLoading}
              />
            </div>

            <StageHint
              title={t("ideaInput.idea.hint.title")}
              description={t("ideaInput.idea.hint.description")}
            />
          </div>

          <div className="mt-5 flex-1" />

          <div className="mt-6 flex flex-wrap items-center justify-between gap-3">
            <p className="max-w-md text-xs leading-6 text-slate-400">
              {!hasSession
                ? t("ideaInput.idea.footerNeedsSession")
                : t("ideaInput.idea.footerReady")}
            </p>

            <Button
              type="submit"
              className="idea-submit-button"
              disabled={!hasSession || isLoading || !ideaTitle.trim() || !ideaContent.trim()}
            >
              {t("ideaInput.idea.submit")}
            </Button>
          </div>
        </div>

        <div className="idea-form-panel__glow" />
      </form>
    </section>
  );
}