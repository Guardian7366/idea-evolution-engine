export type VariantType = 'expansion' | 'focus' | 'creative_twist'

export type TransformationType = 'selection' | 'evolve' | 'refine' | 'mutate'

export type PerspectiveType =
  | 'feasibility'
  | 'innovation'
  | 'user_value'
  | 'risks'

export interface CreateSessionResponse {
  session_id: string
  message: string
}

export interface CreateIdeaRequest {
  session_id: string
  initial_prompt: string
}

export interface CreateIdeaResponse {
  idea_id: string
  session_id: string
  initial_prompt: string
  message: string
}

export interface GenerateVariantsRequest {
  session_id: string
  idea_id: string
  initial_prompt: string
}

export interface IdeaVariantItem {
  variant_id: string
  title: string
  content: string
  variant_type: VariantType
}

export interface GenerateVariantsResponse {
  session_id: string
  idea_id: string
  variants: IdeaVariantItem[]
  message: string
}

export interface ActiveIdeaVersion {
  version_id: string
  idea_id: string
  session_id: string
  title: string
  content: string
  status: 'active'
  version_number: number
  parent_version_id: string | null
  source_variant_id: string | null
  transformation_type: TransformationType
}

export interface SelectVariantRequest {
  session_id: string
  idea_id: string
  variant_id: string
}

export interface SelectVariantResponse {
  session_id: string
  idea_id: string
  selected_variant_id: string
  active_version: ActiveIdeaVersion
  message: string
}

export interface TransformVersionRequest {
  session_id: string
  idea_id: string
  version_id: string
  transformation_type: 'evolve' | 'refine' | 'mutate'
  instruction: string
}

export interface TransformVersionResponse {
  session_id: string
  idea_id: string
  previous_version_id: string
  new_active_version: ActiveIdeaVersion
  message: string
}

export interface CompareVersionsRequest {
  session_id: string
  idea_id: string
  version_id_a: string
  version_id_b: string
}

export interface VersionComparisonResult {
  summary: string
  strengths_version_a: string[]
  strengths_version_b: string[]
  key_differences: string[]
  recommendation: string
}

export interface CompareVersionsResponse {
  session_id: string
  idea_id: string
  version_id_a: string
  version_id_b: string
  comparison: VersionComparisonResult
  message: string
}

export interface ExplorePerspectiveRequest {
  session_id: string
  idea_id: string
  version_id: string
  perspective_type: PerspectiveType
}

export interface PerspectiveAnalysisResult {
  perspective_type: string
  summary: string
  observations: string[]
  suggestion: string
}

export interface ExplorePerspectiveResponse {
  session_id: string
  idea_id: string
  version_id: string
  analysis: PerspectiveAnalysisResult
  message: string
}

export interface GenerateFinalSynthesisRequest {
  session_id: string
  idea_id: string
  version_id: string
}

export interface FinalSynthesisResult {
  title: string
  core_concept: string
  value_proposition: string
  recommended_next_step: string
  notes: string[]
}

export interface GenerateFinalSynthesisResponse {
  session_id: string
  idea_id: string
  version_id: string
  synthesis: FinalSynthesisResult
  message: string
}