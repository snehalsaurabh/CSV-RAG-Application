export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface SearchQuery {
  query: string
  limit?: number
}

export interface FounderResult {
  id: string
  founder_name: string
  role: string
  company: string
  location: string
  snippet: string
  similarity_score: number
  matched_fields: string[]
  row_id: number
}

export interface FounderDetails {
  id: string
  founder_name: string
  email: string
  role: string
  company: string
  location: string
  idea: string
  about: string
  keywords: string
  stage: string
  linkedin: string
  notes: string
}

export interface StatsData {
  total_founders: number
  roles: Record<string, number>
  stages: Record<string, number>
  top_keywords: Record<string, number>
  locations: number
}

export interface DiversityScore {
  role_diversity: number
  stage_diversity: number
  keyword_diversity: number
  location_diversity: number
  background_diversity: number
  skill_diversity: number
}

export interface StatsResponse {
  total_founders: number
  unique_companies: number
  unique_locations: number
  domain_diversity: number
  roles: Record<string, number>
  stages: Record<string, number>
  top_backgrounds: Record<string, number>
  total_unique_backgrounds: number
  top_skills: Record<string, number>
  total_unique_skills: number
  industry_distribution: Record<string, number>
  top_keywords: Record<string, number>
  total_unique_keywords: number
  top_locations: Record<string, number>
  geographic_coverage: number
  sample_achievements: string[]
  total_documented_achievements: number
  diversity_score: DiversityScore
}

