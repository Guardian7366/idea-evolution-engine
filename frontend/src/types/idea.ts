export type LanguageMode = "auto" | "es" | "en";

export interface SessionResponse {
  id: string;
  title: string | null;
  status: string;
  created_at: string;
  updated_at: string;
  closed_at: string | null;
}

export interface IdeaResponse {
  id: string;
  session_id: string;
  content: string;
  title: string | null;
  created_at: string;
  updated_at: string;
}

export interface VariantResponse {
  id: string;
  idea_id: string;
  title: string;
  description: string;
  order_index: number;
  is_selected: boolean;
  selected_at: string | null;
  created_at: string;
}

export interface VariantListResponse {
  items: VariantResponse[];
}

export interface VersionResponse {
  id: string;
  idea_id: string;
  content: string;
  version_number: number;
  transformation_type: string;
  source_variant_id: string | null;
  parent_version_id: string | null;
  user_instruction: string | null;
  is_active: boolean;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface VersionListResponse {
  items: VersionResponse[];
}

export interface PerspectiveResponse {
  id: string;
  version_id: string;
  analysis_type: string;
  content: string;
  created_at: string;
}

export interface ComparisonResponse {
  id: string;
  idea_id: string;
  left_version_id: string;
  right_version_id: string;
  comparison_text: string | null;
  created_at: string;
}

export interface SynthesisResponse {
  id: string;
  idea_id: string;
  version_id: string;
  summary: string;
  value_proposition: string;
  target_audience: string;
  structured_description: string;
  next_steps: string;
  created_at: string;
}

export interface CreateSessionPayload {
  title?: string | null;
}

export interface CreateIdeaPayload {
  session_id: string;
  content: string;
  title?: string | null;
}

export interface SelectVariantPayload {
  idea_id: string;
  variant_id: string;
  language?: LanguageMode;
}

export interface TransformVersionPayload {
  version_id: string;
  transformation_type: string;
  instruction?: string | null;
  language?: LanguageMode;
}

export interface AnalyzePerspectivePayload {
  version_id: string;
  perspective: string;
  language?: LanguageMode;
}

export interface GenerateSynthesisPayload {
  idea_id: string;
  version_id: string;
  language?: LanguageMode;
}

export interface CompareVersionsPayload {
  idea_id: string;
  left_version_id: string;
  right_version_id: string;
  language?: LanguageMode;
}

export interface ActivateVersionPayload {
  version_id: string;
}