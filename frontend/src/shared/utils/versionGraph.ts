import dagre from "dagre";
import { MarkerType, Position, type Edge, type Node } from "reactflow";
import type { VersionResponse } from "../../types/idea";

type BuildVersionGraphResult = {
  nodes: Node[];
  edges: Edge[];
};

const NODE_WIDTH = 248;
const NODE_HEIGHT = 132;

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

export function buildVersionGraph(
  versions: VersionResponse[],
  activeVersionId: string | null,
  selectedVersionId: string | null,
): BuildVersionGraphResult {
  if (!versions.length) {
    return {
      nodes: [],
      edges: [],
    };
  }

  const sortedVersions = [...versions].sort(
    (a, b) => a.version_number - b.version_number,
  );

  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));
  dagreGraph.setGraph({
    rankdir: "LR",
    align: "UL",
    nodesep: 56,
    ranksep: 144,
    marginx: 40,
    marginy: 44,
  });

  const nodes: Node<VersionNodeData>[] = sortedVersions.map((version) => {
    const node: Node<VersionNodeData> = {
      id: version.id,
      type: "versionNode",
      position: { x: 0, y: 0 },
      draggable: false,
      selectable: true,
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
      data: {
        label: {
          versionNumber: version.version_number,
          transformationType: version.transformation_type,
          isActive: version.id === activeVersionId,
          isSelected: version.id === selectedVersionId,
          versionId: version.id,
        },
      },
    };

    dagreGraph.setNode(version.id, {
      width: NODE_WIDTH,
      height: NODE_HEIGHT,
    });

    return node;
  });

  const edges: Edge<VersionEdgeData>[] = sortedVersions
    .filter((version) => version.parent_version_id)
    .map((version) => {
      const isActiveEdge = version.id === activeVersionId;
      const isSelectedEdge =
        version.id === selectedVersionId ||
        version.parent_version_id === selectedVersionId;

      const edge: Edge<VersionEdgeData> = {
        id: `edge-${version.parent_version_id}-${version.id}`,
        source: version.parent_version_id as string,
        target: version.id,
        type: "versionEdge",
        animated: false,
        markerEnd: {
          type: MarkerType.ArrowClosed,
          width: 18,
          height: 18,
          color: isActiveEdge
            ? "rgba(147, 255, 187, 0.96)"
            : isSelectedEdge
              ? "rgba(127, 223, 255, 0.9)"
              : "rgba(135, 191, 224, 0.55)",
        },
        data: {
          isActive: isActiveEdge,
          isSelected: isSelectedEdge,
        },
      };

      dagreGraph.setEdge(version.parent_version_id as string, version.id);

      return edge;
    });

  dagre.layout(dagreGraph);

  const layoutedNodes = nodes.map((node) => {
    const positionedNode = dagreGraph.node(node.id);

    return {
      ...node,
      position: {
        x: positionedNode.x - NODE_WIDTH / 2,
        y: positionedNode.y - NODE_HEIGHT / 2,
      },
    };
  });

  return {
    nodes: layoutedNodes,
    edges,
  };
}