import { useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import Button from "../../../components/shared/ui/Button";
import EmptyState from "../../../components/shared/EmptyState";
import SectionCard from "../../../components/shared/ui/SectionCard";
import {
  loadCollapsedHistoryVersionIds,
  saveCollapsedHistoryVersionIds,
} from "../../../shared/utils/workspaceStorage";
import type { VersionResponse } from "../../../types/idea";

type VersionHistoryPanelProps = {
  versions: VersionResponse[];
  activeVersionId: string | null;
  selectedVersionId: string | null;
  isLoading: boolean;
  onSelectVersion: (versionId: string) => void;
  onActivateVersion: (versionId: string) => Promise<void>;
};

function getInitialCollapsedIds(versions: VersionResponse[]): string[] {
  return versions.map((version) => version.id);
}

export default function VersionHistoryPanel({
  versions,
  activeVersionId,
  selectedVersionId,
  isLoading,
  onSelectVersion,
  onActivateVersion,
}: VersionHistoryPanelProps) {
  const { t } = useTranslation();
  const versionIds = useMemo(() => versions.map((version) => version.id), [versions]);

  const [collapsedVersionIds, setCollapsedVersionIds] = useState<string[]>([]);

  useEffect(() => {
    if (versions.length === 0) {
      setCollapsedVersionIds([]);
      return;
    }

    const storedCollapsedIds = loadCollapsedHistoryVersionIds();
    const validStoredIds = storedCollapsedIds.filter((id) => versionIds.includes(id));

    if (validStoredIds.length > 0) {
      const missingIds = versionIds.filter((id) => !validStoredIds.includes(id));
      setCollapsedVersionIds([...validStoredIds, ...missingIds]);
      return;
    }

    setCollapsedVersionIds(getInitialCollapsedIds(versions));
  }, [versions, versionIds]);

  useEffect(() => {
    saveCollapsedHistoryVersionIds(collapsedVersionIds);
  }, [collapsedVersionIds]);

  const toggleVersionCollapsed = (versionId: string) => {
    setCollapsedVersionIds((current) => {
      if (current.includes(versionId)) {
        return current.filter((id) => id !== versionId);
      }

      return [...current, versionId];
    });
  };

  const expandAllVersions = () => {
    setCollapsedVersionIds([]);
  };

  const collapseAllVersions = () => {
    setCollapsedVersionIds(getInitialCollapsedIds(versions));
  };

  return (
    <SectionCard
      title={t("versionHistory.title")}
      description={t("versionHistory.description")}
      action={
        versions.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            <Button
              type="button"
              variant="secondary"
              onClick={expandAllVersions}
              className="px-4 py-2 text-xs"
            >
              {t("versionHistory.actions.expandAll")}
            </Button>

            <Button
              type="button"
              variant="secondary"
              onClick={collapseAllVersions}
              className="px-4 py-2 text-xs"
            >
              {t("versionHistory.actions.collapseAll")}
            </Button>
          </div>
        ) : null
      }
    >
      {versions.length === 0 ? (
        <EmptyState
          title={t("versionHistory.empty.title")}
          description={t("versionHistory.empty.description")}
        />
      ) : (
        <div className="grid gap-5">
          <div className="rounded-[1.45rem] border border-white/8 bg-slate-950/20 px-4 py-4 md:px-5">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div className="flex flex-wrap items-center gap-2">
                <span className="aero-badge">{t("versionHistory.badges.trail")}</span>
                <span className="aero-badge">
                  {t("versionHistory.badges.records", { count: versions.length })}
                </span>
                <span className="aero-badge">{t("versionHistory.badges.timeline")}</span>
              </div>

              <div className="rounded-full border border-white/8 bg-white/[0.03] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">
                {t("versionHistory.liveHistory")}
              </div>
            </div>

            <p className="mt-4 text-sm leading-7 text-slate-300/84">
              {t("versionHistory.intro")}
            </p>
          </div>

          <div className="grid gap-4">
            {versions.map((version, index) => {
              const isActive = version.id === activeVersionId;
              const isSelected = version.id === selectedVersionId;
              const isRoot = !version.parent_version_id;
              const isCollapsed = collapsedVersionIds.includes(version.id);

              return (
                <article
                  key={version.id}
                  className={[
                    "history-version-card rounded-[1.65rem] p-5 transition duration-200 md:p-6",
                    isActive
                      ? "history-version-card--active"
                      : isSelected
                        ? "history-version-card--selected"
                        : "history-version-card--default",
                  ].join(" ")}
                >
                  <div className="relative z-[1] grid gap-4">
                    <div className="flex flex-wrap items-start justify-between gap-4">
                      <div className="max-w-3xl">
                        <div className="flex flex-wrap items-center gap-2">
                          <span className="aero-badge">
                            {t("versionHistory.versionBadge", {
                              number: version.version_number,
                            })}
                          </span>
                          <span className="aero-badge">{version.transformation_type}</span>

                          {isActive ? (
                            <span className="aero-badge aero-badge--success">
                              {t("versionHistory.activeBadge")}
                            </span>
                          ) : null}

                          {isSelected && !isActive ? (
                            <span className="aero-badge">
                              {t("versionHistory.selectedBadge")}
                            </span>
                          ) : null}

                          {isCollapsed ? (
                            <span className="aero-badge">
                              {t("versionHistory.compactViewBadge")}
                            </span>
                          ) : (
                            <span className="aero-badge">
                              {t("versionHistory.expandedViewBadge")}
                            </span>
                          )}
                        </div>

                        <h3 className="mt-4 text-lg font-semibold tracking-[-0.02em] text-slate-50">
                          {isActive
                            ? t("versionHistory.stateLabels.current")
                            : isSelected
                              ? t("versionHistory.stateLabels.observing")
                              : t("versionHistory.stateLabels.previous")}
                        </h3>

                        <p className="mt-2 text-sm leading-7 text-slate-300/84">
                          {isActive
                            ? t("versionHistory.stateMessages.current")
                            : isSelected
                              ? t("versionHistory.stateMessages.observing")
                              : t("versionHistory.stateMessages.previous")}
                        </p>
                      </div>

                      <div className="flex flex-wrap gap-2">
                        <Button
                          type="button"
                          variant="secondary"
                          onClick={() => toggleVersionCollapsed(version.id)}
                          className="history-version-card__toggle px-4 py-2 text-xs"
                          aria-expanded={!isCollapsed}
                          aria-label={
                            isCollapsed
                              ? t("versionHistory.actions.expandVersionAria", {
                                  number: version.version_number,
                                })
                              : t("versionHistory.actions.collapseVersionAria", {
                                  number: version.version_number,
                                })
                          }
                          title={
                            isCollapsed
                              ? t("versionHistory.actions.expandVersionAria", {
                                  number: version.version_number,
                                })
                              : t("versionHistory.actions.collapseVersionAria", {
                                  number: version.version_number,
                                })
                          }
                        >
                          <span className="history-version-card__toggle-icon" aria-hidden="true">
                            {isCollapsed ? "▾" : "▴"}
                          </span>
                          {isCollapsed
                            ? t("versionHistory.actions.viewFull")
                            : t("versionHistory.actions.hideDetail")}
                        </Button>

                        <Button
                          type="button"
                          variant="secondary"
                          onClick={() => onSelectVersion(version.id)}
                          className="px-4 py-2 text-xs"
                        >
                          {t("versionHistory.actions.focus")}
                        </Button>

                        <Button
                          type="button"
                          variant="success"
                          disabled={isActive || isLoading}
                          onClick={() => {
                            void onActivateVersion(version.id);
                          }}
                          className="px-4 py-2 text-xs"
                        >
                          {isActive
                            ? t("versionHistory.actions.alreadyActive")
                            : t("versionHistory.actions.makeActive")}
                        </Button>
                      </div>
                    </div>

                    <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
                      <div className="rounded-[1.2rem] border border-white/8 bg-slate-950/22 px-3 py-3">
                        <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                          {t("versionHistory.meta.position")}
                        </p>
                        <p className="mt-2 text-sm text-slate-200">
                          {t("versionHistory.meta.node", { index: index + 1 })}
                        </p>
                      </div>

                      <div className="rounded-[1.2rem] border border-white/8 bg-slate-950/22 px-3 py-3">
                        <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                          {t("versionHistory.meta.origin")}
                        </p>
                        <p className="mt-2 text-sm text-slate-200">
                          {isRoot
                            ? t("versionHistory.origin.root")
                            : t("versionHistory.origin.derived")}
                        </p>
                      </div>

                      <div className="rounded-[1.2rem] border border-white/8 bg-slate-950/22 px-3 py-3">
                        <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                          {t("versionHistory.meta.state")}
                        </p>
                        <p className="mt-2 text-sm text-slate-200">
                          {isActive
                            ? t("versionHistory.states.governing")
                            : isSelected
                              ? t("versionHistory.states.reading")
                              : t("versionHistory.states.archived")}
                        </p>
                      </div>

                      <div className="rounded-[1.2rem] border border-white/8 bg-slate-950/22 px-3 py-3">
                        <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                          {t("versionHistory.meta.identity")}
                        </p>
                        <p className="mt-2 break-all text-sm text-slate-200">{version.id}</p>
                      </div>
                    </div>

                    {isCollapsed ? (
                      <div className="history-version-card__collapsed rounded-[1.4rem] border border-white/8 bg-slate-950/24 px-4 py-4 md:px-5">
                        <div className="flex flex-wrap items-center gap-2">
                          <span className="aero-badge">{t("versionHistory.content.stageContent")}</span>
                          <span className="aero-badge">{t("versionHistory.content.compactView")}</span>
                        </div>

                        <p className="mt-3 text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                          {t("versionHistory.content.hiddenTemporarily")}
                        </p>

                        <p className="mt-3 text-sm leading-7 text-slate-300/78">
                          {t("versionHistory.content.compactMessagePrefix")}
                          <span className="font-semibold text-slate-100">
                            {" "}
                            {t("versionHistory.actions.viewFull")}{" "}
                          </span>
                          {t("versionHistory.content.compactMessageSuffix")}
                        </p>
                      </div>
                    ) : (
                      <div className="rounded-[1.4rem] border border-white/8 bg-slate-950/24 p-4 md:p-5">
                        <div className="mb-3 flex flex-wrap items-center gap-2">
                          <span className="aero-badge">{t("versionHistory.content.stageContent")}</span>
                          <span className="aero-badge">{t("versionHistory.content.readableSnapshot")}</span>
                        </div>

                        <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                          {t("versionHistory.content.stageLabel")}
                        </p>

                        <p className="mt-3 whitespace-pre-wrap text-sm leading-8 text-slate-200">
                          {version.content}
                        </p>
                      </div>
                    )}
                  </div>

                  <div className="history-version-card__flow" />
                </article>
              );
            })}
          </div>
        </div>
      )}
    </SectionCard>
  );
}