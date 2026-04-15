/* Shared type definitions for the frontend application. */

export interface User {
  id: number;
  email: string;
  full_name: string | null;
  role: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Resume {
  id: number;
  user_id: number;
  original_filename: string;
  file_path: string;
  extracted_text: string | null;
  uploaded_at: string;
}

export interface Vacancy {
  id: number;
  title: string;
  company: string;
  description: string;
  requirements: string | null;
  location: string | null;
  employment_type: string | null;
  salary_min: number | null;
  salary_max: number | null;
  url: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Recommendation {
  id: number;
  user_id: number;
  vacancy_id: number;
  overall_score: number;
  keyword_score: number;
  semantic_score: number;
  matched_skills: string[] | null;
  missing_skills: string[] | null;
  explanation: string | null;
  strategy: string | null;
  created_at: string;
  updated_at: string;
  vacancy: Vacancy;
}

export interface GenerateRecommendationsResponse {
  strategy: string;
  generated_count: number;
  results: Recommendation[];
}

export interface StrategyInfo {
  name: string;
  description: string;
}

export interface StrategiesResponse {
  strategies: StrategyInfo[];
}

export interface AuthToken {
  access_token: string;
  token_type: string;
}

export interface ApiError {
  detail: string;
}

export interface UploadResponse {
  id: number;
  user_id: number;
  original_filename: string;
  file_path: string;
  extracted_text: string | null;
  uploaded_at: string;
}
