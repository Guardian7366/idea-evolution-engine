import { useMemo } from "react";
import { useTranslation } from "react-i18next";
import ReactFlow, {
  Background,
  BaseEdge,
  Controls,
  Handle,
  MiniMap,
  Position,
  getSmoothStepPath,
  type Edge,
  type EdgeProps,
  type Node,
  type NodeProps,
} from "reactflow";
import "reactflow/dist/style.css";

import Button from "../../../components/shared/ui/Button";
import EmptyState from "../../../components/shared/EmptyState";
import SectionCard from "../../../components/shared/ui/SectionCard";
import { buildVersionGraph } from "../../../shared/utils/versionGraph";
import type { VersionResponse } from "../../../types/idea";

type VersionGraphPanelProps = {
  versions: VersionResponse[];
  activeVersionId: string | null;
  selectedVersionId: string | null;
  isLoading: boolean;
  onSelectVersion: (versionId: string) => void;
  onActivateVersion: (versionId: string) => Promise<void>;
};

type VersionNodeData = {
  label: {
    versionNumber: number;
    transformationType: string;
    isActive: boolean;
    isSelected: boolean;
    versionId: string;
  };
};

type VersionEdgeData = {
  isActive: boolean;
  isSelected: boolean;
};

function VersionNode({ data }: NodeProps<VersionNodeData>) {
  const { t } = useTranslation();
  const isActive = data.label.isActive;
  const isSelected = data.label.isSelected;

  return (
    <div
      data-active={isActive ? "true" : "false"}
      data-selected={isSelected ? "true" : "false"}
      className={[
        "version-graph-node version-graph-node--cultivation min-w-[252px] rounded-[1.55rem] border p-4 shadow-lg transition duration-200",
        isActive
          ? "version-graph-node--active"
          : isSelected
            ? "version-graph-node--selected"
            : "version-graph-node--default",
      ].join(" ")}
    >
      <Handle
        type="target"
        position={Position.Left}
        className="version-graph-node__handle version-graph-node__handle--target"
        isConnectable={false}
      />

      <Handle
        type="source"
        position={Position.Right}
        className="version-graph-node__handle version-graph-node__handle--source"
        isConnectable={false}
      />

      <div className="version-graph-node__backdrop" />
      <div className="version-graph-node__growth-ring version-graph-node__growth-ring--one" />
      <div className="version-graph-node__growth-ring version-graph-node__growth-ring--two" />
      <div className="version-graph-node__grain" />

      <div className="relative z-[1]">
        <div className="flex items-start justify-between gap-3">
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <span className="aero-badge">
                {t("versionGraph.node.versionBadge", {
                  number: data.label.versionNumber,
                })}
              </span>
              <span className="aero-badge">{data.label.transformationType}</span>
            </div>

            <p className="mt-3 text-sm font-semibold tracking-[-0.02em] text-slate-100">
              {isActive
                ? t("versionGraph.node.titles.active")
                : isSelected
                  ? t("versionGraph.node.titles.focused")
                  : t("versionGraph.node.titles.evolutionary")}
            </p>
          </div>

          <div className="version-graph-node__shine" />
        </div>

        <p className="mt-3 text-xs leading-6 text-slate-400">
          {isActive
            ? t("versionGraph.node.messages.active")
            : isSelected
              ? t("versionGraph.node.messages.focused")
              : t("versionGraph.node.messages.evolutionary")}
        </p>

        <div className="mt-4 flex flex-wrap gap-2">
          {isActive ? (
            <span className="aero-badge aero-badge--success">
              {t("versionGraph.node.badges.active")}
            </span>
          ) : null}

          {isSelected && !isActive ? (
            <span className="aero-badge">{t("versionGraph.node.badges.selected")}</span>
          ) : null}
        </div>
      </div>

      <div className="version-graph-node__glow" />
    </div>
  );
}

function VersionEdge({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  markerEnd,
  data,
}: EdgeProps<VersionEdgeData>) {
  const [edgePath] = getSmoothStepPath({
    sourceX,
    sourceY,
    targetX,
    targetY,
    sourcePosition,
    targetPosition,
    borderRadius: 22,
    offset: 18,
  });

  const glowStyle = data?.isActive
    ? {
        stroke: "rgba(122, 255, 186, 0.34)",
        strokeWidth: 10,
        opacity: 0.22,
        filter: "blur(4px)",
        strokeLinecap: "round" as const,
        strokeLinejoin: "round" as const,
      }
    : data?.isSelected
      ? {
          stroke: "rgba(102, 227, 255, 0.3)",
          strokeWidth: 10,
          opacity: 0.22,
          filter: "blur(4px)",
          strokeLinecap: "round" as const,
          strokeLinejoin: "round" as const,
        }
      : {
          stroke: "rgba(126, 197, 235, 0.22)",
          strokeWidth: 10,
          opacity: 0.18,
          filter: "blur(4px)",
          strokeLinecap: "round" as const,
          strokeLinejoin: "round" as const,
        };

  const coreStyle = data?.isActive
    ? {
        stroke: "rgba(147, 255, 187, 0.96)",
        strokeWidth: 2.6,
        strokeLinecap: "round" as const,
        strokeLinejoin: "round" as const,
      }
    : data?.isSelected
      ? {
          stroke: "rgba(126, 239, 255, 0.88)",
          strokeWidth: 2.6,
          strokeLinecap: "round" as const,
          strokeLinejoin: "round" as const,
        }
      : {
          stroke: "rgba(138, 193, 224, 0.58)",
          strokeWidth: 2.6,
          strokeLinecap: "round" as const,
          strokeLinejoin: "round" as const,
        };

  return (
    <>
      <BaseEdge
        id={`${id}-glow`}
        path={edgePath}
        style={glowStyle}
      />
      <BaseEdge
        id={id}
        path={edgePath}
        markerEnd={markerEnd}
        style={coreStyle}
      />
    </>
  );
}

const nodeTypes = {
  versionNode: VersionNode,
};

const edgeTypes = {
  versionEdge: VersionEdge,
};

export default function VersionGraphPanel({
  versions,
  activeVersionId,
  selectedVersionId,
  isLoading,
  onSelectVersion,
  onActivateVersion,
}: VersionGraphPanelProps) {
  const { t } = useTranslation();

  const graph = useMemo(
    () => buildVersionGraph(versions, activeVersionId, selectedVersionId),
    [versions, activeVersionId, selectedVersionId],
  );

  const selectedVersion =
    versions.find((version) => version.id === selectedVersionId) ?? null;

  const nodes = graph.nodes as Node<VersionNodeData>[];
  const edges = graph.edges as Edge<VersionEdgeData>[];

  const rootVersionCount = useMemo(
    () => versions.filter((version) => !version.parent_version_id).length,
    [versions],
  );

  const handleNodeClick = (_event: React.MouseEvent, node: Node<VersionNodeData>) => {
    onSelectVersion(node.id);
  };

  const canActivate =
    selectedVersion !== null && selectedVersion.id !== activeVersionId;

  return (
    <SectionCard
      title={t("versionGraph.title")}
      description={t("versionGraph.description")}
    >
      {versions.length === 0 ? (
        <EmptyState
          title={t("versionGraph.empty.title")}
          description={t("versionGraph.empty.description")}
        />
      ) : (
        <div className="evolution-graph-stage grid gap-5">
          <div className="rounded-[1.45rem] border border-white/8 bg-slate-950/20 px-4 py-4 md:px-5">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div className="flex flex-wrap items-center gap-2">
                <span className="aero-badge">{t("versionGraph.badges.visualMap")}</span>
                <span className="aero-badge">
                  {t("versionGraph.badges.potentialNodes", { count: versions.length })}
                </span>
                <span className="aero-badge">{t("versionGraph.badges.interactivePath")}</span>
              </div>

              <div className="rounded-full border border-white/8 bg-white/[0.03] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">
                {t("versionGraph.graphView")}
              </div>
            </div>

            <div className="mt-4 grid gap-3 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-start">
              <p className="text-sm leading-7 text-slate-300/84">
                {t("versionGraph.intro")}
              </p>

              <div className="rounded-[1.1rem] border border-white/8 bg-slate-950/22 px-4 py-3 text-sm text-slate-300">
                <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-500">
                  {t("versionHistory.meta.origin")}
                </p>
                <p className="mt-2 font-medium text-slate-100">
                  {rootVersionCount === 1
                    ? t("versionHistory.origin.root")
                    : t("versionHistory.badges.records", { count: rootVersionCount })}
                </p>
              </div>
            </div>
          </div>

          <div className="version-graph-shell overflow-hidden rounded-[1.95rem] border">
            <div className="version-graph-shell__glow version-graph-shell__glow--one" />
            <div className="version-graph-shell__glow version-graph-shell__glow--two" />
            <div className="version-graph-shell__glow version-graph-shell__glow--three" />
            <div className="version-graph-shell__arc version-graph-shell__arc--one" />
            <div className="version-graph-shell__arc version-graph-shell__arc--two" />
            <div className="version-graph-shell__grid" />
            <div className="version-graph-shell__pulse version-graph-shell__pulse--one" />
            <div className="version-graph-shell__pulse version-graph-shell__pulse--two" />

            <div className="h-[520px] md:h-[560px]">
              <ReactFlow
                className="version-graph-flow"
                nodes={nodes}
                edges={edges}
                nodeTypes={nodeTypes}
                edgeTypes={edgeTypes}
                fitView
                fitViewOptions={{ padding: 0.24 }}
                proOptions={{ hideAttribution: true }}
                onNodeClick={handleNodeClick}
              >
                <MiniMap zoomable pannable />
                <Controls />
                <Background gap={24} size={1.2} />
              </ReactFlow>
            </div>
          </div>

          <div className="graph-detail-panel graph-detail-panel--cultivation rounded-[1.65rem] p-5 md:p-6">
            <div className="graph-detail-panel__backdrop" />

            <div className="relative z-[1] grid gap-5">
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div className="max-w-2xl">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="aero-badge">
                      {t("versionGraph.detail.badges.nodeInspection")}
                    </span>
                    <span className="aero-badge">
                      {t("versionGraph.detail.badges.interactiveFocus")}
                    </span>
                    <span className="aero-badge">
                      {t("versionGraph.detail.badges.reactivationControl")}
                    </span>
                  </div>

                  <h3 className="mt-4 text-lg font-semibold tracking-[-0.02em] text-slate-50">
                    {t("versionGraph.detail.title")}
                  </h3>

                  <p className="mt-2 text-sm leading-7 text-slate-300/84">
                    {t("versionGraph.detail.description")}
                  </p>
                </div>

                <Button
                  type="button"
                  variant="success"
                  disabled={!canActivate || isLoading}
                  onClick={() => {
                    if (selectedVersion) {
                      void onActivateVersion(selectedVersion.id);
                    }
                  }}
                  className="px-4 py-2 text-xs"
                >
                  {selectedVersion?.id === activeVersionId
                    ? t("versionGraph.detail.actions.alreadyActive")
                    : t("versionGraph.detail.actions.makeActive")}
                </Button>
              </div>

              {!selectedVersion ? (
                <div className="rounded-[1.35rem] border border-white/8 bg-slate-950/24 p-4 md:p-5">
                  <p className="text-sm leading-7 text-slate-300/82">
                    {t("versionGraph.detail.noSelection")}
                  </p>
                </div>
              ) : (
                <>
                  <div className="flex flex-wrap gap-2">
                    <span className="aero-badge">
                      {t("versionGraph.node.versionBadge", {
                        number: selectedVersion.version_number,
                      })}
                    </span>
                    <span className="aero-badge">{selectedVersion.transformation_type}</span>
                    {selectedVersion.id === activeVersionId ? (
                      <span className="aero-badge aero-badge--success">
                        {t("versionGraph.node.badges.active")}
                      </span>
                    ) : null}
                  </div>

                  <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
                    <div className="rounded-[1.25rem] border border-white/8 bg-slate-950/24 p-4">
                      <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                        {t("versionGraph.detail.blocks.nodeReading")}
                      </p>

                      <p className="mt-3 text-sm leading-7 text-slate-300/84">
                        {selectedVersion.id === activeVersionId
                          ? t("versionGraph.detail.reading.active")
                          : t("versionGraph.detail.reading.available")}
                      </p>
                    </div>

                    <div className="rounded-[1.25rem] border border-white/8 bg-slate-950/24 p-4">
                      <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                        {t("versionGraph.detail.blocks.structureRelation")}
                      </p>

                      <p className="mt-3 text-sm leading-7 text-slate-300/84">
                        {selectedVersion.parent_version_id
                          ? t("versionGraph.detail.structure.derived")
                          : t("versionGraph.detail.structure.root")}
                      </p>
                    </div>

                    <div className="rounded-[1.25rem] border border-white/8 bg-slate-950/24 p-4 md:col-span-2 xl:col-span-1">
                      <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                        {t("versionGraph.detail.blocks.nodeId")}
                      </p>

                      <p className="mt-3 break-all text-sm leading-7 text-slate-300/84">
                        {selectedVersion.id}
                      </p>
                    </div>
                  </div>

                  <div className="rounded-[1.35rem] border border-white/8 bg-slate-950/24 p-4 md:p-5">
                    <div className="mb-3 flex flex-wrap items-center gap-2">
                      <span className="aero-badge">
                        {t("versionGraph.detail.contentBadges.associated")}
                      </span>
                      <span className="aero-badge">
                        {t("versionGraph.detail.contentBadges.focusedReading")}
                      </span>
                    </div>

                    <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                      {t("versionGraph.detail.contentLabel")}
                    </p>

                    <p className="mt-3 whitespace-pre-wrap text-sm leading-8 text-slate-300">
                      {selectedVersion.content}
                    </p>
                  </div>
                </>
              )}
            </div>

            <div className="graph-detail-panel__glow" />
          </div>
        </div>
      )}
    </SectionCard>
  );
}