import type { TFunction } from "i18next";
import type { IdeaFlowState } from "../../store/idea-flow.store";

export type WorkspaceSlideIconKey =
  | "home"
  | "controls"
  | "idea"
  | "variants"
  | "transform"
  | "history"
  | "analysis"
  | "synthesis";

export type WorkspaceSlideId =
  | "workspace-hero"
  | "workspace-system"
  | "workspace-seed"
  | "workspace-branch"
  | "workspace-core"
  | "workspace-evolution"
  | "workspace-analysis"
  | "workspace-synthesis";

export type WorkspaceSlideItem = {
  id: WorkspaceSlideId;
  label: string;
  shortLabel: string;
  icon: WorkspaceSlideIconKey;
  isEnabled: (state: IdeaFlowState) => boolean;
};

export function getWorkspaceSlidesRegistry(t: TFunction): WorkspaceSlideItem[] {
  return [
    {
      id: "workspace-hero",
      label: t("slides.hero.label"),
      shortLabel: t("slides.hero.shortLabel"),
      icon: "home",
      isEnabled: () => true,
    },
    {
      id: "workspace-system",
      label: t("slides.system.label"),
      shortLabel: t("slides.system.shortLabel"),
      icon: "controls",
      isEnabled: () => true,
    },
    {
      id: "workspace-seed",
      label: t("slides.seed.label"),
      shortLabel: t("slides.seed.shortLabel"),
      icon: "idea",
      isEnabled: () => true,
    },
    {
      id: "workspace-branch",
      label: t("slides.branch.label"),
      shortLabel: t("slides.branch.shortLabel"),
      icon: "variants",
      isEnabled: (state) => Boolean(state.session && state.idea),
    },
    {
      id: "workspace-core",
      label: t("slides.core.label"),
      shortLabel: t("slides.core.shortLabel"),
      icon: "transform",
      isEnabled: (state) =>
        Boolean(
          state.session &&
            state.idea &&
            (state.variants.length > 0 || state.activeVersion || state.selectedVersion),
        ),
    },
    {
      id: "workspace-evolution",
      label: t("slides.evolution.label"),
      shortLabel: t("slides.evolution.shortLabel"),
      icon: "history",
      isEnabled: (state) => Boolean(state.idea && state.versions.length > 0),
    },
    {
      id: "workspace-analysis",
      label: t("slides.analysis.label"),
      shortLabel: t("slides.analysis.shortLabel"),
      icon: "analysis",
      isEnabled: (state) =>
        Boolean(state.idea && state.activeVersion && state.versions.length > 0),
    },
    {
      id: "workspace-synthesis",
      label: t("slides.synthesis.label"),
      shortLabel: t("slides.synthesis.shortLabel"),
      icon: "synthesis",
      isEnabled: (state) => Boolean(state.idea && state.activeVersion),
    },
  ];
}

export function isWorkspaceSlideEnabled(
  slideId: WorkspaceSlideId,
  state: IdeaFlowState,
  registry: WorkspaceSlideItem[],
): boolean {
  const slide = registry.find((item) => item.id === slideId);

  if (!slide) {
    return false;
  }

  return slide.isEnabled(state);
}

export function getFirstEnabledWorkspaceSlide(
  state: IdeaFlowState,
  registry: WorkspaceSlideItem[],
): WorkspaceSlideId {
  const firstEnabled = registry.find((item) => item.isEnabled(state)) ?? registry[0];
  return firstEnabled.id;
}

export function getNextEnabledWorkspaceSlide(
  currentId: WorkspaceSlideId,
  state: IdeaFlowState,
  registry: WorkspaceSlideItem[],
): WorkspaceSlideId {
  const currentIndex = registry.findIndex((item) => item.id === currentId);

  if (currentIndex === -1) {
    return getFirstEnabledWorkspaceSlide(state, registry);
  }

  for (let step = 1; step <= registry.length; step += 1) {
    const nextIndex = (currentIndex + step) % registry.length;
    const nextSlide = registry[nextIndex];

    if (nextSlide.isEnabled(state)) {
      return nextSlide.id;
    }
  }

  return currentId;
}

export function getPreviousEnabledWorkspaceSlide(
  currentId: WorkspaceSlideId,
  state: IdeaFlowState,
  registry: WorkspaceSlideItem[],
): WorkspaceSlideId {
  const currentIndex = registry.findIndex((item) => item.id === currentId);

  if (currentIndex === -1) {
    return getFirstEnabledWorkspaceSlide(state, registry);
  }

  for (let step = 1; step <= registry.length; step += 1) {
    const previousIndex = (currentIndex - step + registry.length) % registry.length;
    const previousSlide = registry[previousIndex];

    if (previousSlide.isEnabled(state)) {
      return previousSlide.id;
    }
  }

  return currentId;
}