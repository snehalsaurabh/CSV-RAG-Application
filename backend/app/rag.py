import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import os
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
        """Get dataset statistics"""
        if self.founders_df is None:
            return {"error": "Dataset not loaded"}
        
        # Get keyword frequency
        all_keywords = []
        for keywords_str in self.founders_df['keywords']:
            all_keywords.extend([k.strip() for k in keywords_str.split(',')])
        
        keyword_counts = pd.Series(all_keywords).value_counts().head(10).to_dict()
        
        return {
            "total_founders": len(self.founders_df),
            "roles": self.founders_df['role'].value_counts().to_dict(),
            "stages": self.founders_df['stage'].value_counts().to_dict(),
            "top_keywords": keyword_counts,
            "locations": len(self.founders_df['location'].unique())
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
