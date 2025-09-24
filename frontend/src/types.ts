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


