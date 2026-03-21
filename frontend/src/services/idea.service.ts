import { apiClient } from './api'
import type {
  CompareVersionsRequest,
  CompareVersionsResponse,
  CreateIdeaRequest,
  CreateIdeaResponse,
  CreateSessionResponse,
  ExplorePerspectiveRequest,
  ExplorePerspectiveResponse,
  GenerateFinalSynthesisRequest,
  GenerateFinalSynthesisResponse,
  GenerateVariantsRequest,
  GenerateVariantsResponse,
  SelectVariantRequest,
  SelectVariantResponse,
  TransformVersionRequest,
  TransformVersionResponse,
} from '../types/idea'

// Session creation endpoint.
export async function createSession(): Promise<CreateSessionResponse> {
  const response = await apiClient.post<CreateSessionResponse>('/sessions')
  return response.data
}

// Idea creation endpoint.
export async function createIdea(
  payload: CreateIdeaRequest,
): Promise<CreateIdeaResponse> {
  const response = await apiClient.post<CreateIdeaResponse>('/ideas', payload)
  return response.data
}

// Initial variants generation endpoint.
export async function generateVariants(
  payload: GenerateVariantsRequest,
): Promise<GenerateVariantsResponse> {
  const response = await apiClient.post<GenerateVariantsResponse>(
    '/ideas/generate-variants',
    payload,
  )
  return response.data
}

// Variant selection endpoint that creates the first active version.
export async function selectVariant(
  payload: SelectVariantRequest,
): Promise<SelectVariantResponse> {
  const response = await apiClient.post<SelectVariantResponse>(
    '/ideas/select-variant',
    payload,
  )
  return response.data
}

// Version transformation endpoint.
export async function transformVersion(
  payload: TransformVersionRequest,
): Promise<TransformVersionResponse> {
  const response = await apiClient.post<TransformVersionResponse>(
    '/ideas/transform-version',
    payload,
  )
  return response.data
}

// Analytical comparison between two versions.
export async function compareVersions(
  payload: CompareVersionsRequest,
): Promise<CompareVersionsResponse> {
  const response = await apiClient.post<CompareVersionsResponse>(
    '/ideas/compare-versions',
    payload,
  )
  return response.data
}

// Analytical perspective exploration over one version.
export async function explorePerspective(
  payload: ExplorePerspectiveRequest,
): Promise<ExplorePerspectiveResponse> {
  const response = await apiClient.post<ExplorePerspectiveResponse>(
    '/ideas/explore-perspective',
    payload,
  )
  return response.data
}

// Final synthesis generation for the active version.
export async function generateFinalSynthesis(
  payload: GenerateFinalSynthesisRequest,
): Promise<GenerateFinalSynthesisResponse> {
  const response = await apiClient.post<GenerateFinalSynthesisResponse>(
    '/ideas/generate-final-synthesis',
    payload,
  )
  return response.data
}