import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import os
import re
from typing import List, Tuple
from dotenv import load_dotenv

load_dotenv()

class RAGService:
    def __init__(self):
        self.model = None
        self.index = None
        self.founders_df = None
        self.embeddings = None
        self.gemini_model = None
        self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Initialize Gemini API"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                print("✅ Gemini API initialized with gemini-1.5-flash")
            except Exception as e:
                print(f"❌ Gemini API initialization failed: {e}")
                self.gemini_model = None
        else:
            print("❌ No Gemini API key found")
    
    def load_dataset(self) -> bool:
        """Load the founders dataset"""
        try:
            # Try different path possibilities
            paths = [
                "../data/founders_dataset.csv",
                "data/founders_dataset.csv", 
                "./data/founders_dataset.csv"
            ]
            
            for path in paths:
                try:
                    self.founders_df = pd.read_csv(path)
                    print(f"✅ Loaded {len(self.founders_df)} founder records from {path}")
                    return True
                except FileNotFoundError:
                    continue
            
            print("❌ Could not find founders_dataset.csv in any expected location")
            return False
            
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            return False
    
    def initialize_embeddings(self) -> bool:
        """Initialize embeddings and FAISS index"""
        try:
            if self.founders_df is None:
                print("❌ Dataset not loaded")
                return False
            
            # Load sentence transformer model
            print("🔄 Loading sentence transformer model...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Create comprehensive text for embedding
            texts = []
            for _, row in self.founders_df.iterrows():
                text = (f"Founder: {row['founder_name']} | "
                       f"Role: {row['role']} | "
                       f"Company: {row['company']} | "
                       f"Location: {row['location']} | "
                       f"Stage: {row['stage']} | "
                       f"Keywords: {row['keywords']} | "
                       f"Idea: {row['idea']} | "
                       f"About: {row['about']}")
                texts.append(text)
            
            # Generate embeddings
            print("🔄 Generating embeddings...")
            self.embeddings = self.model.encode(texts, show_progress_bar=True)
            
            # Create FAISS index
            print("🔄 Creating FAISS index...")
            dimension = self.embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(self.embeddings)
            self.index.add(self.embeddings.astype('float32'))
            
            print(f"✅ RAG system initialized with {len(self.embeddings)} embeddings")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing RAG system: {e}")
            return False
    
    def search_founders(self, query: str, limit: int = 5) -> List[dict]:
        """Search for founders using vector similarity"""
        try:
            if self.model is None or self.index is None:
                return []
            
            # Generate query embedding
            query_embedding = self.model.encode([query])
            faiss.normalize_L2(query_embedding)
            
            # Search FAISS index
            scores, indices = self.index.search(query_embedding.astype('float32'), limit)
            
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.founders_df):
                    founder = self.founders_df.iloc[idx]
                    
                    # Generate explanation using Gemini
                    snippet = self.generate_match_explanation_gemini(query, founder)
                    matched_fields = self.identify_matched_fields(query, founder)
                    
                    result = {
                        "id": founder['id'],
                        "founder_name": founder['founder_name'],
                        "role": founder['role'],
                        "company": founder['company'],
                        "location": founder['location'],
                        "snippet": snippet,
                        "similarity_score": float(score),
                        "matched_fields": matched_fields,
                        "row_id": int(idx)
                    }
                    results.append(result)
            
            return results
            
        except Exception as e:
            print(f"❌ Error in search: {e}")
            return []
    
    def generate_match_explanation_gemini(self, query: str, founder) -> str:
        """Generate match explanation using Gemini"""
        try:
            if self.gemini_model is None:
                return self.generate_match_explanation_fallback(query, founder)
            
            prompt = f"""
            Query: "{query}"
            
            Founder Profile:
            - Name: {founder['founder_name']}
            - Role: {founder['role']}
            - Company: {founder['company']}
            - Location: {founder['location']}
            - Keywords: {founder['keywords']}
            - About: {founder['about']}
            - Idea: {founder['idea']}
            - Stage: {founder['stage']}
            
            Generate a concise 1-2 sentence explanation of why this founder matches the query. 
            Focus on the most relevant matching aspects. Start with "Matched on" and cite specific fields.
            
            Example: "Matched on keywords: healthtech, AI and role: Founder with experience in building diagnostic platforms for early disease detection."
            """
            
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"❌ Gemini API error: {e}")
            return self.generate_match_explanation_fallback(query, founder)
    
    def generate_match_explanation_fallback(self, query: str, founder) -> str:
        """Fallback explanation generation without Gemini"""
        explanations = []
        query_lower = query.lower()
        
        # Check different fields for matches
        keywords = [k.strip() for k in founder['keywords'].split(',')]
        if any(keyword.lower() in query_lower for keyword in keywords):
            matching_keywords = [k for k in keywords if k.lower() in query_lower]
            explanations.append(f"keywords: {', '.join(matching_keywords[:2])}")
        
        if founder['role'].lower() in query_lower:
            explanations.append(f"role: {founder['role']}")
        
        if founder['location'].lower() in query_lower or any(loc.lower() in query_lower for loc in founder['location'].split(', ')):
            explanations.append(f"location: {founder['location']}")
        
        if founder['stage'].lower() in query_lower:
            explanations.append(f"stage: {founder['stage']}")
        
        # Default explanation
        if not explanations:
            primary_keyword = keywords[0] if keywords else "technology"
            explanations.append(f"expertise in {primary_keyword}, role: {founder['role']}")
        
        return f"Matched on " + " and ".join(explanations[:2]) + f" (row id: {founder.name})"
    
    def identify_matched_fields(self, query: str, founder) -> List[str]:
        """Identify which fields contributed to the match"""
        matched = []
        query_lower = query.lower()
        
        keywords = [k.strip().lower() for k in founder['keywords'].split(',')]
        if any(keyword in query_lower for keyword in keywords):
            matched.append("keywords")
        
        if founder['role'].lower() in query_lower:
            matched.append("role")
        
        if founder['company'].lower() in query_lower:
            matched.append("company")
        
        if any(loc.lower() in query_lower for loc in founder['location'].split(', ')):
            matched.append("location")
        
        if founder['stage'].lower() in query_lower:
            matched.append("stage")
        
        # Check about and idea for word matches
        about_words = set(founder['about'].lower().split())
        idea_words = set(founder['idea'].lower().split())
        query_words = set(query_lower.split())
        
        if about_words.intersection(query_words):
            matched.append("about")
        
        if idea_words.intersection(query_words):
            matched.append("idea")
        
        return matched if matched else ["keywords", "about"]
    
    def get_founder_by_id(self, founder_id: str) -> dict:
        """Get founder details by ID"""
        if self.founders_df is None:
            return None
        
        founder_row = self.founders_df[self.founders_df['id'] == founder_id]
        if len(founder_row) == 0:
            return None
        
        # Convert row to dict and handle NaN values
        founder_dict = founder_row.iloc[0].to_dict()
        for key, value in founder_dict.items():
            if pd.isna(value):  # Check if value is NaN
                founder_dict[key] = None
        
        return founder_dict
    
    def get_stats(self) -> dict:
        """Get comprehensive dataset statistics showcasing diversity"""
        if self.founders_df is None:
            return {"error": "Dataset not loaded"}
        
        # Basic stats
        total_founders = len(self.founders_df)
        unique_locations = self.founders_df['location'].nunique()
        unique_companies = self.founders_df['company'].nunique()
        
        # Keywords analysis - more detailed
        all_keywords = []
        for keywords_str in self.founders_df['keywords']:
            if pd.notna(keywords_str):
                all_keywords.extend([k.strip() for k in keywords_str.split(',')])
        
        keyword_counts = pd.Series(all_keywords).value_counts()
        top_keywords = keyword_counts.head(15).to_dict()
        total_unique_keywords = len(keyword_counts)
        
        # Extract backgrounds/previous experience
        backgrounds = []
        skills = []
        achievements = []
        
        for about_text in self.founders_df['about']:
            if pd.notna(about_text):
                # Extract company backgrounds
                if 'Former' in about_text or 'Ex-' in about_text:
                    # Find patterns like "Former Google", "Ex-McKinsey", etc.
                    bg_patterns = re.findall(r'(?:Former|Ex-)[\s]?([A-Za-z&\s]+?)(?:\s(?:engineer|consultant|manager|executive|researcher|analyst|PM|designer|developer|lead|associate))', about_text)
                    backgrounds.extend([bg.strip() for bg in bg_patterns])
                
                # Extract skills (look for "expertise in")
                if 'expertise in' in about_text:
                    skill_text = about_text.split('expertise in')[1].split('.')[0]
                    extracted_skills = [s.strip() for s in skill_text.split(',')]
                    skills.extend(extracted_skills)
                
                # Extract achievements
                if 'Previously' in about_text:
                    achievement_text = about_text.split('Previously')[1].split('.')[0]
                    achievements.append(achievement_text.strip())
        
        # Clean and count backgrounds
        background_counts = {}
        for bg in backgrounds:
            clean_bg = bg.strip()
            if len(clean_bg) > 2 and len(clean_bg) < 30:  # Filter reasonable company names
                background_counts[clean_bg] = background_counts.get(clean_bg, 0) + 1
        
        # Get top backgrounds
        top_backgrounds = dict(sorted(background_counts.items(), key=lambda x: x[1], reverse=True)[:12])
        
        # Skills analysis
        skill_counts = {}
        for skill in skills:
            clean_skill = skill.strip()
            if len(clean_skill) > 3 and len(clean_skill) < 40:
                skill_counts[clean_skill] = skill_counts.get(clean_skill, 0) + 1
        
        top_skills = dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:15])
        
        # Geographic diversity - extract countries/regions
        location_counts = self.founders_df['location'].value_counts().head(20).to_dict()
        
        # Company stage distribution
        stage_counts = self.founders_df['stage'].value_counts().to_dict()
        
        # Role distribution  
        role_counts = self.founders_df['role'].value_counts().to_dict()
        
        # Industry focus (group related keywords)
        industry_mapping = {
            'Technology': ['AI', 'machine learning', 'blockchain', 'cybersecurity', 'IoT', 'AR', 'VR', 'robotics'],
            'Business & Finance': ['fintech', 'SaaS', 'marketplace', 'analytics', 'automation'],
            'Health & Life Sciences': ['healthtech', 'biotech', 'fitness'],
            'Consumer & Retail': ['e-commerce', 'retail', 'fashion', 'beauty', 'gaming'],
            'Infrastructure & Tools': ['cloud', 'developer tools', 'productivity', 'logistics'],
            'Sustainability & Energy': ['cleantech', 'energy', 'agriculture'],
            'Media & Content': ['adtech', 'social', 'mobile'],
            'Real Estate & Property': ['proptech'],
            'Education': ['edtech'],
            'Food & Hospitality': ['foodtech', 'travel']
        }
        
        industry_stats = {}
        for industry, keywords in industry_mapping.items():
            count = sum(keyword_counts.get(keyword, 0) for keyword in keywords)
            if count > 0:
                industry_stats[industry] = count
        
        # Email domain analysis for company diversity
        domains = []
        for email in self.founders_df['email']:
            if pd.notna(email) and '@' in email:
                domain = email.split('@')[1].split('.')[0]
                domains.append(domain)
        
        domain_diversity = len(set(domains))
        
        return {
            # Core metrics
            "total_founders": int(total_founders),
            "unique_companies": int(unique_companies),
            "unique_locations": int(unique_locations),
            "domain_diversity": int(domain_diversity),
            
            # Role & Stage breakdown
            "roles": {str(k): int(v) for k, v in role_counts.items()},
            "stages": {str(k): int(v) for k, v in stage_counts.items()},
            
            # Skills & Background diversity
            "top_backgrounds": {str(k): int(v) for k, v in top_backgrounds.items()},
            "total_unique_backgrounds": int(len(background_counts)),
            "top_skills": {str(k): int(v) for k, v in top_skills.items()},
            "total_unique_skills": int(len(skill_counts)),
            
            # Industry & Technology focus
            "industry_distribution": {str(k): int(v) for k, v in industry_stats.items()},
            "top_keywords": {str(k): int(v) for k, v in top_keywords.items()},
            "total_unique_keywords": int(total_unique_keywords),
            
            # Geographic diversity
            "top_locations": {str(k): int(v) for k, v in location_counts.items()},
            "geographic_coverage": int(unique_locations),
            
            # Achievement diversity
            "sample_achievements": [str(achievement) for achievement in achievements[:10]] if achievements else [],
            "total_documented_achievements": int(len(achievements)),
            
            # Diversity metrics
            "diversity_score": {
                "role_diversity": int(len(role_counts)),
                "stage_diversity": int(len(stage_counts)), 
                "keyword_diversity": int(total_unique_keywords),
                "location_diversity": int(unique_locations),
                "background_diversity": int(len(background_counts)),
                "skill_diversity": int(len(skill_counts))
            }
        }
    
    def is_ready(self) -> bool:
        """Check if RAG system is ready"""
        return (self.founders_df is not None and 
                self.model is not None and 
                self.index is not None)
    
    def is_gemini_available(self) -> bool:
        """Check if Gemini is available"""
        return self.gemini_model is not None

# Global RAG service instance
rag_service = RAGService()
