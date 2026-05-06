import type {
  ComparisonResponse,
  IdeaResponse,
  LanguageMode,
  PerspectiveResponse,
  SessionResponse,
  SynthesisResponse,
  VariantResponse,
  VersionResponse,
} from "../types/idea";

export type IdeaFlowState = {
  session: SessionResponse | null;
  idea: IdeaResponse | null;
  variants: VariantResponse[];
  versions: VersionResponse[];
  activeVersion: VersionResponse | null;
  selectedVersion: VersionResponse | null;
  latestAnalysis: PerspectiveResponse | null;
  latestComparison: ComparisonResponse | null;
  latestSynthesis: SynthesisResponse | null;
  isLoading: boolean;
  error: string | null;
  languageMode: LanguageMode;
};

export const initialIdeaFlowState: IdeaFlowState = {
  session: null,
  idea: null,
  variants: [],
  versions: [],
  activeVersion: null,
  selectedVersion: null,
  latestAnalysis: null,
  latestComparison: null,
  latestSynthesis: null,
  isLoading: false,
  error: null,
  languageMode: "auto",
};