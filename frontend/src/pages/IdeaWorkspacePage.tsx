import { useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import PerspectiveExplorerPanel from "../features/analysis/components/PerspectiveExplorerPanel";
import VersionComparisonPanel from "../features/analysis/components/VersionComparisonPanel";
import IdeaInputSection from "../features/idea-input/components/IdeaInputSection";
import FlowStatusPanel from "../features/session/components/FlowStatusPanel";
import LanguageSelectorPanel from "../features/session/components/LanguageSelectorPanel";
import FinalSynthesisPanel from "../features/synthesis/components/FinalSynthesisPanel";
import VariantsList from "../features/variants/components/VariantsList";
import ActiveVersionPanel from "../features/versioning/components/ActiveVersionPanel";
import VersionGraphPanel from "../features/versioning/components/VersionGraphPanel";
import VersionHistoryPanel from "../features/versioning/components/VersionHistoryPanel";
import VersionTransformPanel from "../features/versioning/components/VersionTransformPanel";
import WorkspaceSectionNavbar from "../components/navigation/WorkspaceSectionNavbar";
import WorkspaceSlidesViewport from "../components/navigation/WorkspaceSlidesViewport";
import { useIdeaFlow } from "../hooks/useIdeaFlow";
import heroBanner from "../assets/images/hero-horizontal-banner.png";
import {
  getFirstEnabledWorkspaceSlide,
  getNextEnabledWorkspaceSlide,
  getPreviousEnabledWorkspaceSlide,
  getWorkspaceSlidesRegistry,
  isWorkspaceSlideEnabled,
  type WorkspaceSlideId,
} from "../shared/utils/workspaceSlides";

export default function IdeaWorkspacePage() {
  const { t } = useTranslation();
  const { state, actions } = useIdeaFlow();
  const [activeSlideId, setActiveSlideId] = useState<WorkspaceSlideId>("workspace-hero");

  const workspaceSlidesRegistry = useMemo(() => getWorkspaceSlidesRegistry(t), [t]);

  const handleCreateSession = async (title: string): Promise<void> => {
    await actions.createSession({ title });
  };

  const handleCreateIdea = async ({
    title,
    content,
  }: {
    title: string;
    content: string;
  }): Promise<void> => {
    if (!state.session) {
      return;
    }

    const createdIdea = await actions.createIdea({
      session_id: state.session.id,
      title,
      content,
    });

    await actions.generateVariants(createdIdea.id);
  };

  const handleSelectVariant = async (variantId: string): Promise<void> => {
    if (!state.idea) {
      return;
    }

    await actions.selectVariant({
      idea_id: state.idea.id,
      variant_id: variantId,
    });
  };

  const handleActivateVersion = async (versionId: string): Promise<void> => {
    await actions.activateVersion(versionId);
  };

  const handleEvolution = async (): Promise<void> => {
    if (!state.activeVersion || !state.idea) {
      return;
    }

    await actions.transformVersion(
      {
        version_id: state.activeVersion.id,
        transformation_type: "evolution",
        instruction: null,
      },
      state.idea.id,
    );
  };

  const handleMutation = async (): Promise<void> => {
    if (!state.activeVersion || !state.idea) {
      return;
    }

    await actions.transformVersion(
      {
        version_id: state.activeVersion.id,
        transformation_type: "mutation",
        instruction: null,
      },
      state.idea.id,
    );
  };

  const handleRefinement = async (instruction: string): Promise<void> => {
    if (!state.activeVersion || !state.idea) {
      return;
    }

    await actions.transformVersion(
      {
        version_id: state.activeVersion.id,
        transformation_type: "refinement",
        instruction,
      },
      state.idea.id,
    );
  };

  const handleAnalyzePerspective = async (perspective: string): Promise<void> => {
    if (!state.activeVersion) {
      return;
    }

    await actions.analyzePerspective({
      version_id: state.activeVersion.id,
      perspective,
    });
  };

  const handleGenerateSynthesis = async (): Promise<void> => {
    if (!state.activeVersion || !state.idea) {
      return;
    }

    await actions.generateSynthesis({
      idea_id: state.idea.id,
      version_id: state.activeVersion.id,
    });
  };

  const handleCompareVersions = async ({
    leftVersionId,
    rightVersionId,
  }: {
    leftVersionId: string;
    rightVersionId: string;
  }): Promise<void> => {
    if (!state.idea) {
      return;
    }

    await actions.compareVersions({
      idea_id: state.idea.id,
      left_version_id: leftVersionId,
      right_version_id: rightVersionId,
    });
  };

  const navigationItems = useMemo(
    () =>
      workspaceSlidesRegistry.map((item) => ({
        ...item,
        enabled: item.isEnabled(state),
      })),
    [state, workspaceSlidesRegistry],
  );

  useEffect(() => {
    if (!isWorkspaceSlideEnabled(activeSlideId, state, workspaceSlidesRegistry)) {
      setActiveSlideId(getFirstEnabledWorkspaceSlide(state, workspaceSlidesRegistry));
    }
  }, [activeSlideId, state, workspaceSlidesRegistry]);

  const handleSelectSlide = (slideId: WorkspaceSlideId) => {
    if (!isWorkspaceSlideEnabled(slideId, state, workspaceSlidesRegistry)) {
      return;
    }

    setActiveSlideId(slideId);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleGoToPreviousSlide = () => {
    const previousSlideId = getPreviousEnabledWorkspaceSlide(
      activeSlideId,
      state,
      workspaceSlidesRegistry,
    );
    setActiveSlideId(previousSlideId);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleGoToNextSlide = () => {
    const nextSlideId = getNextEnabledWorkspaceSlide(
      activeSlideId,
      state,
      workspaceSlidesRegistry,
    );
    setActiveSlideId(nextSlideId);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const slides = useMemo(
    () => [
      {
        id: "workspace-hero" as WorkspaceSlideId,
        content: (
          <section className="workspace-hero aero-panel rounded-[2rem] p-6 md:p-7 xl:p-8">
            <div className="workspace-hero__orb workspace-hero__orb--one" />
            <div className="workspace-hero__orb workspace-hero__orb--two" />
            <div className="workspace-hero__orb workspace-hero__orb--three" />
            <div className="workspace-hero__arc workspace-hero__arc--one" />
            <div className="workspace-hero__arc workspace-hero__arc--two" />
            <div className="workspace-hero__stream workspace-hero__stream--one" />
            <div className="workspace-hero__stream workspace-hero__stream--two" />
            <div className="workspace-hero__grid" />

            <div className="relative z-[1] grid gap-6 xl:grid-cols-[minmax(0,1.08fr)_minmax(320px,0.92fr)] xl:items-start">
              <div className="workspace-hero__content-column xl:pr-4">
                <div className="mb-4 flex flex-wrap items-center gap-2">
                  <span className="aero-badge">{t("workspaceHero.badges.creativeEvolution")}</span>
                  <span className="aero-badge">{t("workspaceHero.badges.systemContinuity")}</span>
                  <span className="aero-badge aero-badge--success">
                    {t("workspaceHero.badges.livingWorkspace")}
                  </span>
                </div>

                <div className="max-w-4xl">
                  <p className="workspace-hero__kicker">{t("workspaceHero.kicker")}</p>

                  <h2 className="workspace-hero__title text-[1.9rem] font-semibold text-slate-50 md:text-[2.3rem]">
                    {t("workspaceHero.title")}
                  </h2>

                  <p className="mt-4 max-w-3xl text-sm leading-7 text-slate-300/84 md:text-[15px]">
                    {t("workspaceHero.description")}
                  </p>
                </div>

                <div className="workspace-hero__image-slot">
                  <img
                    src={heroBanner}
                    alt={t("workspaceHero.bannerAlt")}
                    className="h-full w-full rounded-[1.6rem] object-cover"
                  />
                </div>
              </div>

              <div className="workspace-hero__stage-panel rounded-[1.8rem] p-4 md:p-5">
                <div className="relative z-[1] grid gap-3">
                  <div className="workspace-hero__stage-card rounded-2xl p-4">
                    <span className="aero-badge mb-3">{t("workspaceHero.stages.stage1.badge")}</span>
                    <p className="font-semibold text-slate-100">
                      {t("workspaceHero.stages.stage1.title")}
                    </p>
                    <p className="mt-2 text-sm leading-6 text-slate-300/82">
                      {t("workspaceHero.stages.stage1.description")}
                    </p>
                  </div>

                  <div className="workspace-hero__stage-card rounded-2xl p-4">
                    <span className="aero-badge mb-3">{t("workspaceHero.stages.stage2.badge")}</span>
                    <p className="font-semibold text-slate-100">
                      {t("workspaceHero.stages.stage2.title")}
                    </p>
                    <p className="mt-2 text-sm leading-6 text-slate-300/82">
                      {t("workspaceHero.stages.stage2.description")}
                    </p>
                  </div>

                  <div className="workspace-hero__stage-card rounded-2xl p-4">
                    <span className="aero-badge mb-3">{t("workspaceHero.stages.stage3.badge")}</span>
                    <p className="font-semibold text-slate-100">
                      {t("workspaceHero.stages.stage3.title")}
                    </p>
                    <p className="mt-2 text-sm leading-6 text-slate-300/82">
                      {t("workspaceHero.stages.stage3.description")}
                    </p>
                  </div>
                </div>

                <div className="workspace-hero__stage-glow" />
              </div>
            </div>
          </section>
        ),
      },
      {
        id: "workspace-system" as WorkspaceSlideId,
        content: (
          <section className="workspace-zone workspace-zone--system">
            <div className="workspace-zone__header">
              <span className="workspace-zone__eyebrow">{t("workspaceSystem.kicker")}</span>
              <h3 className="workspace-zone__title">{t("workspaceSystem.title")}</h3>
            </div>

            <div className="grid gap-6 xl:grid-cols-[minmax(320px,0.88fr)_minmax(0,1.12fr)] xl:items-start">
              <LanguageSelectorPanel
                value={state.languageMode}
                isLoading={state.isLoading}
                onChange={actions.setLanguageMode}
              />

              <FlowStatusPanel
                sessionId={state.session?.id ?? null}
                ideaId={state.idea?.id ?? null}
                activeVersionId={state.activeVersion?.id ?? null}
                isLoading={state.isLoading}
                error={state.error}
                onClearWorkspace={actions.clearWorkspace}
              />
            </div>
          </section>
        ),
      },
      {
        id: "workspace-seed" as WorkspaceSlideId,
        content: (
          <section className="workspace-zone workspace-zone--seed">
            <div className="workspace-zone__header">
              <span className="workspace-zone__eyebrow">{t("workspaceSeed.kicker")}</span>
              <h3 className="workspace-zone__title">{t("workspaceSeed.title")}</h3>
            </div>

            <IdeaInputSection
              session={state.session}
              idea={state.idea}
              hasSession={Boolean(state.session)}
              isLoading={state.isLoading}
              onCreateSession={handleCreateSession}
              onCreateIdea={handleCreateIdea}
            />
          </section>
        ),
      },
      {
        id: "workspace-branch" as WorkspaceSlideId,
        content: (
          <section className="workspace-zone workspace-zone--branch">
            <div className="workspace-zone__header">
              <span className="workspace-zone__eyebrow">{t("workspaceBranch.kicker")}</span>
              <h3 className="workspace-zone__title">{t("workspaceBranch.title")}</h3>
            </div>

            <VariantsList
              variants={state.variants}
              isLoading={state.isLoading}
              onSelect={handleSelectVariant}
            />
          </section>
        ),
      },
      {
        id: "workspace-core" as WorkspaceSlideId,
        content: (
          <section className="workspace-zone workspace-zone--core">
            <div className="workspace-zone__header">
              <span className="workspace-zone__eyebrow">{t("workspaceCore.kicker")}</span>
              <h3 className="workspace-zone__title">{t("workspaceCore.title")}</h3>
            </div>

            <div className="mx-auto grid w-full max-w-5xl gap-6">
              <ActiveVersionPanel
                activeVersion={state.activeVersion}
                selectedVersion={state.selectedVersion}
              />

              <VersionTransformPanel
                activeVersion={state.activeVersion}
                isLoading={state.isLoading}
                languageMode={state.languageMode}
                onEvolution={handleEvolution}
                onMutation={handleMutation}
                onRefinement={handleRefinement}
              />
            </div>
          </section>
        ),
      },
      {
        id: "workspace-evolution" as WorkspaceSlideId,
        content: (
          <section className="workspace-zone workspace-zone--evolution">
            <div className="workspace-zone__header">
              <span className="workspace-zone__eyebrow">{t("workspaceEvolution.kicker")}</span>
              <h3 className="workspace-zone__title">{t("workspaceEvolution.title")}</h3>
            </div>

            <div className="mx-auto grid w-full max-w-5xl gap-6">
              <VersionHistoryPanel
                versions={state.versions}
                activeVersionId={state.activeVersion?.id ?? null}
                selectedVersionId={state.selectedVersion?.id ?? null}
                isLoading={state.isLoading}
                onSelectVersion={actions.selectVersionFromHistory}
                onActivateVersion={handleActivateVersion}
              />

              <VersionGraphPanel
                versions={state.versions}
                activeVersionId={state.activeVersion?.id ?? null}
                selectedVersionId={state.selectedVersion?.id ?? null}
                isLoading={state.isLoading}
                onSelectVersion={actions.selectVersionFromHistory}
                onActivateVersion={handleActivateVersion}
              />
            </div>
          </section>
        ),
      },
      {
        id: "workspace-analysis" as WorkspaceSlideId,
        content: (
          <section className="workspace-zone workspace-zone--analysis">
            <div className="workspace-zone__header">
              <span className="workspace-zone__eyebrow">{t("workspaceAnalysis.kicker")}</span>
              <h3 className="workspace-zone__title">{t("workspaceAnalysis.title")}</h3>
            </div>

            <div className="mx-auto grid w-full max-w-5xl gap-6">
              <VersionComparisonPanel
                ideaId={state.idea?.id ?? null}
                versions={state.versions}
                latestComparison={state.latestComparison}
                isLoading={state.isLoading}
                onCompare={handleCompareVersions}
              />

              <PerspectiveExplorerPanel
                activeVersion={state.activeVersion}
                latestAnalysis={state.latestAnalysis}
                isLoading={state.isLoading}
                onAnalyze={handleAnalyzePerspective}
              />
            </div>
          </section>
        ),
      },
      {
        id: "workspace-synthesis" as WorkspaceSlideId,
        content: (
          <section className="workspace-zone workspace-zone--synthesis">
            <div className="workspace-zone__header">
              <span className="workspace-zone__eyebrow">{t("workspaceSynthesis.kicker")}</span>
              <h3 className="workspace-zone__title">{t("workspaceSynthesis.title")}</h3>
            </div>

            <FinalSynthesisPanel
              activeVersion={state.activeVersion}
              synthesis={state.latestSynthesis}
              isLoading={state.isLoading}
              onGenerate={handleGenerateSynthesis}
            />
          </section>
        ),
      },
    ],
    [
      actions.clearWorkspace,
      actions.selectVersionFromHistory,
      actions.setLanguageMode,
      handleActivateVersion,
      handleAnalyzePerspective,
      handleCompareVersions,
      handleCreateSession,
      handleGenerateSynthesis,
      handleMutation,
      handleRefinement,
      handleSelectVariant,
      handleEvolution,
      handleCreateIdea,
      heroBanner,
      state.activeVersion,
      state.error,
      state.idea,
      state.isLoading,
      state.languageMode,
      state.latestAnalysis,
      state.latestComparison,
      state.latestSynthesis,
      state.selectedVersion,
      state.session,
      state.variants,
      state.versions,
      t,
    ],
  );

  return (
    <div className="workspace-page-layout">
      <div className="workspace-page grid gap-6 md:gap-7">
        <WorkspaceSectionNavbar
          items={navigationItems}
          activeSlideId={activeSlideId}
          onSelect={handleSelectSlide}
        />

        <WorkspaceSlidesViewport
          slides={slides}
          activeSlideId={activeSlideId}
          onPrevious={handleGoToPreviousSlide}
          onNext={handleGoToNextSlide}
        />
      </div>
    </div>
  );
}