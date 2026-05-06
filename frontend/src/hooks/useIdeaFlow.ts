import { useEffect, useState } from "react";
import { ideaService } from "../services/idea.service";
import { initialIdeaFlowState } from "../store/idea-flow.store";
import type {
  AnalyzePerspectivePayload,
  CompareVersionsPayload,
  CreateIdeaPayload,
  CreateSessionPayload,
  GenerateSynthesisPayload,
  LanguageMode,
  SelectVariantPayload,
  TransformVersionPayload,
} from "../types/idea";
import {
  clearWorkspaceFromStorage,
  loadWorkspaceFromStorage,
  saveWorkspaceToStorage,
} from "../shared/utils/workspaceStorage";

function extractApiError(error: unknown, fallbackMessage: string): string {
  const maxMessageLength = 300;

  function normalizeMessage(message: string): string {
    const trimmed = message.trim();

    if (!trimmed) {
      return fallbackMessage;
    }

    if (trimmed.length > maxMessageLength) {
      return `${trimmed.slice(0, maxMessageLength).trim()}...`;
    }

    return trimmed;
  }

  if (typeof error === "object" && error !== null && "response" in error) {
    const response = (error as { response?: { data?: unknown } }).response;
    const data = response?.data;

    if (typeof data === "object" && data !== null) {
      const detail = (data as { detail?: unknown }).detail;
      const apiError = (data as { error?: { message?: unknown } }).error;

      if (typeof detail === "string") {
        return normalizeMessage(detail);
      }

      if (typeof apiError?.message === "string") {
        return normalizeMessage(apiError.message);
      }
    }
  }

  if (error instanceof Error) {
    return normalizeMessage(error.message);
  }

  return fallbackMessage;
}

export function useIdeaFlow() {
  const [state, setState] = useState(initialIdeaFlowState);
  const [hasBootstrapped, setHasBootstrapped] = useState(false);

  const setLoading = (isLoading: boolean) => {
    setState((prev) => ({ ...prev, isLoading }));
  };

  const setError = (error: string | null) => {
    setState((prev) => ({ ...prev, error }));
  };

  const setLanguageMode = (languageMode: LanguageMode) => {
    setState((prev) => ({ ...prev, languageMode }));
  };

  const bootstrapWorkspace = async (params: {
    sessionId: string;
    ideaId: string;
    languageMode: LanguageMode;
  }) => {
    try {
      setLoading(true);
      setError(null);

      const [session, idea, variants, versions] = await Promise.all([
        ideaService.getSessionById(params.sessionId),
        ideaService.getIdeaById(params.ideaId),
        ideaService.listVariants(params.ideaId),
        ideaService.listVersions(params.ideaId),
      ]);

      const activeVersion =
        versions.items.find((version) => version.is_active) ?? null;

      setState((prev) => ({
        ...prev,
        session,
        idea,
        variants: variants.items,
        versions: versions.items,
        activeVersion,
        selectedVersion: activeVersion,
        latestAnalysis: null,
        latestComparison: null,
        latestSynthesis: null,
        languageMode: params.languageMode,
        error: null,
      }));
    } catch (error) {
      clearWorkspaceFromStorage();
      setError(
        extractApiError(error, "No se pudo restaurar el workspace guardado."),
      );
    } finally {
      setLoading(false);
      setHasBootstrapped(true);
    }
  };

  useEffect(() => {
    const stored = loadWorkspaceFromStorage();

    if (stored.sessionId && stored.ideaId) {
      void bootstrapWorkspace({
        sessionId: stored.sessionId,
        ideaId: stored.ideaId,
        languageMode: stored.languageMode,
      });
      return;
    }

    setState((prev) => ({
      ...prev,
      languageMode: stored.languageMode,
    }));
    setHasBootstrapped(true);
  }, []);

  useEffect(() => {
    if (!hasBootstrapped) {
      return;
    }

    saveWorkspaceToStorage({
      sessionId: state.session?.id ?? null,
      ideaId: state.idea?.id ?? null,
      languageMode: state.languageMode,
    });
  }, [hasBootstrapped, state.session?.id, state.idea?.id, state.languageMode]);

  const createSession = async (payload: CreateSessionPayload) => {
    try {
      setLoading(true);
      setError(null);

      const session = await ideaService.createSession(payload);

      setState((prev) => ({
        ...prev,
        session,
      }));

      return session;
    } catch (error) {
      setError(extractApiError(error, "No se pudo crear la sesión."));
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const createIdea = async (payload: CreateIdeaPayload) => {
    try {
      setLoading(true);
      setError(null);

      const idea = await ideaService.createIdea(payload);

      setState((prev) => ({
        ...prev,
        idea,
        variants: [],
        versions: [],
        activeVersion: null,
        selectedVersion: null,
        latestAnalysis: null,
        latestComparison: null,
        latestSynthesis: null,
      }));

      return idea;
    } catch (error) {
      setError(extractApiError(error, "No se pudo registrar la idea."));
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const generateVariants = async (ideaId: string) => {
    try {
      setLoading(true);
      setError(null);

      const response = await ideaService.generateVariants(ideaId, state.languageMode);

      setState((prev) => ({
        ...prev,
        variants: response.items,
      }));

      return response.items;
    } catch (error) {
      setError(extractApiError(error, "No se pudieron generar las variantes."));
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const selectVariant = async (payload: SelectVariantPayload) => {
    try {
      setLoading(true);
      setError(null);

      const version = await ideaService.selectVariant({
        ...payload,
        language: state.languageMode,
      });

      const [versions, variants] = await Promise.all([
        ideaService.listVersions(payload.idea_id),
        ideaService.listVariants(payload.idea_id),
      ]);

      setState((prev) => ({
        ...prev,
        variants: variants.items,
        activeVersion: version,
        selectedVersion: version,
        versions: versions.items,
        latestAnalysis: null,
        latestComparison: null,
        latestSynthesis: null,
      }));

      return version;
    } catch (error) {
      setError(extractApiError(error, "No se pudo seleccionar la variante."));
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const transformVersion = async (payload: TransformVersionPayload, ideaId: string) => {
    try {
      setLoading(true);
      setError(null);

      const version = await ideaService.transformVersion({
        ...payload,
        language: state.languageMode,
      });

      const versions = await ideaService.listVersions(ideaId);

      setState((prev) => ({
        ...prev,
        activeVersion: version,
        selectedVersion: version,
        versions: versions.items,
        latestAnalysis: null,
        latestComparison: null,
        latestSynthesis: null,
      }));

      return version;
    } catch (error) {
      setError(extractApiError(error, "No se pudo transformar la versión."));
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const activateVersion = async (versionId: string) => {
    try {
      setLoading(true);
      setError(null);

      const version = await ideaService.activateVersion({
        version_id: versionId,
      });

      const versions = await ideaService.listVersions(version.idea_id);

      setState((prev) => ({
        ...prev,
        activeVersion: version,
        selectedVersion: version,
        versions: versions.items,
      }));

      return version;
    } catch (error) {
      setError(extractApiError(error, "No se pudo activar la versión."));
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const analyzePerspective = async (payload: AnalyzePerspectivePayload) => {
    try {
      setLoading(true);
      setError(null);

      const analysis = await ideaService.analyzePerspective({
        ...payload,
        language: state.languageMode,
      });

      setState((prev) => ({
        ...prev,
        latestAnalysis: analysis,
      }));

      return analysis;
    } catch (error) {
      setError(extractApiError(error, "No se pudo generar el análisis."));
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const compareVersions = async (payload: CompareVersionsPayload) => {
    try {
      setLoading(true);
      setError(null);

      const comparison = await ideaService.compareVersions({
        ...payload,
        language: state.languageMode,
      });

      setState((prev) => ({
        ...prev,
        latestComparison: comparison,
      }));

      return comparison;
    } catch (error) {
      setError(extractApiError(error, "No se pudo generar la comparación."));
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const generateSynthesis = async (payload: GenerateSynthesisPayload) => {
    try {
      setLoading(true);
      setError(null);

      const synthesis = await ideaService.generateSynthesis({
        ...payload,
        language: state.languageMode,
      });

      setState((prev) => ({
        ...prev,
        latestSynthesis: synthesis,
      }));

      return synthesis;
    } catch (error) {
      setError(extractApiError(error, "No se pudo generar la síntesis."));
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const clearWorkspace = () => {
    clearWorkspaceFromStorage();
    setState(initialIdeaFlowState);
    setHasBootstrapped(true);
  };

  const selectVersionFromHistory = (versionId: string) => {
    setState((prev) => {
      const version = prev.versions.find((item) => item.id === versionId) ?? null;

      if (!version) {
        return prev;
      }

      return {
        ...prev,
        selectedVersion: version,
      };
    });
  };

  return {
    state,
    actions: {
      createSession,
      createIdea,
      generateVariants,
      selectVariant,
      transformVersion,
      activateVersion,
      analyzePerspective,
      compareVersions,
      generateSynthesis,
      setLanguageMode,
      selectVersionFromHistory,
      clearWorkspace,
      bootstrapWorkspace,
    },
  };
}