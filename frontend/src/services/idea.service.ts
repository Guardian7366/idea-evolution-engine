import { apiClient } from "./api";
import type {
  ActivateVersionPayload,
  AnalyzePerspectivePayload,
  CompareVersionsPayload,
  ComparisonResponse,
  CreateIdeaPayload,
  CreateSessionPayload,
  GenerateSynthesisPayload,
  IdeaResponse,
  LanguageMode,
  PerspectiveResponse,
  SelectVariantPayload,
  SessionResponse,
  SynthesisResponse,
  TransformVersionPayload,
  VariantListResponse,
  VersionListResponse,
  VersionResponse,
} from "../types/idea";

function buildLanguageQuery(language: LanguageMode): string {
  return `language=${encodeURIComponent(language)}`;
}

export const ideaService = {
  async createSession(payload: CreateSessionPayload): Promise<SessionResponse> {
    const { data } = await apiClient.post<SessionResponse>("/sessions/", payload);
    return data;
  },

  async createIdea(payload: CreateIdeaPayload): Promise<IdeaResponse> {
    const { data } = await apiClient.post<IdeaResponse>("/ideas/", payload);
    return data;
  },

  async generateVariants(
    ideaId: string,
    language: LanguageMode = "auto",
  ): Promise<VariantListResponse> {
    const { data } = await apiClient.post<VariantListResponse>(
      `/ideas/${ideaId}/variants?${buildLanguageQuery(language)}`,
    );
    return data;
  },

  async getSessionById(sessionId: string): Promise<SessionResponse> {
    const { data } = await apiClient.get<SessionResponse>(`/sessions/${sessionId}`);
    return data;
  },

  async getIdeaById(ideaId: string): Promise<IdeaResponse> {
    const { data } = await apiClient.get<IdeaResponse>(`/ideas/${ideaId}`);
    return data;
  },

  async listVariants(ideaId: string): Promise<VariantListResponse> {
    const { data } = await apiClient.get<VariantListResponse>(`/ideas/${ideaId}/variants`);
    return data;
  },

  async selectVariant(payload: SelectVariantPayload): Promise<VersionResponse> {
    const { data } = await apiClient.post<VersionResponse>("/versions/select", payload);
    return data;
  },

  async listVersions(ideaId: string): Promise<VersionListResponse> {
    const { data } = await apiClient.get<VersionListResponse>(`/versions/idea/${ideaId}`);
    return data;
  },

  async transformVersion(payload: TransformVersionPayload): Promise<VersionResponse> {
    const { data } = await apiClient.post<VersionResponse>("/versions/transform", payload);
    return data;
  },

  async activateVersion(payload: ActivateVersionPayload): Promise<VersionResponse> {
    const { data } = await apiClient.post<VersionResponse>("/versions/activate", payload);
    return data;
  },

  async analyzePerspective(
    payload: AnalyzePerspectivePayload,
  ): Promise<PerspectiveResponse> {
    const { data } = await apiClient.post<PerspectiveResponse>(
      "/analysis/perspective",
      payload,
    );
    return data;
  },

  async generateSynthesis(
    payload: GenerateSynthesisPayload,
  ): Promise<SynthesisResponse> {
    const { data } = await apiClient.post<SynthesisResponse>("/synthesis/", payload);
    return data;
  },

  async compareVersions(
    payload: CompareVersionsPayload,
  ): Promise<ComparisonResponse> {
    const { data } = await apiClient.post<ComparisonResponse>(
      "/analysis/compare",
      payload,
    );
    return data;
  },
};