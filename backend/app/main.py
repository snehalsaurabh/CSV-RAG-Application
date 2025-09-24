from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

from .models import *
from .auth import get_current_user, authenticate_user, create_access_token
from .rag import rag_service
from .validation import validate_search_query, validate_limit

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Founder RAG Chat API with Gemini...")
    
    print("📊 Loading dataset...")
    if not rag_service.load_dataset():
        print("❌ Failed to load dataset")
        yield
        return
    
    print("🧠 Initializing RAG system...")
    if not rag_service.initialize_embeddings():
        print("❌ Failed to initialize RAG system")
        yield
        return
    
    print("✅ API ready! Visit /docs for documentation")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down...")

# Initialize FastAPI
app = FastAPI(
    title="Founder RAG Chat API",
    description="AI-powered founder matching and discovery system with Gemini AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware - Secure but demo-friendly
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://csv-rag-application-mvu4064jz-snehalsaurabhs-projects.vercel.app",
        "https://csv-rag-application-git-main-snehalsaurabhs-projects.vercel.app",
        "https://csv-rag-application-snehalsaurabhs-projects.vercel.app",
        "https://csv-rag-application.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "Founder RAG Chat API with Gemini AI",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    return HealthResponse(
        status="healthy",
        dataset_loaded=rag_service.founders_df is not None,
        rag_initialized=rag_service.is_ready(),
        total_founders=len(rag_service.founders_df) if rag_service.founders_df is not None else 0,
        gemini_available=rag_service.is_gemini_available()
    )

# Authentication endpoints
@app.post("/auth/login", response_model=Token, tags=["Authentication"])
async def login(user_data: UserLogin):
    # Basic input validation
    if not user_data.username or not user_data.password:
        raise HTTPException(status_code=400, detail="Username and password required")
    
    username = authenticate_user(user_data.username.lower().strip(), user_data.password)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": username})
    return Token(access_token=access_token, token_type="bearer")

# Search endpoints with validation but NO rate limiting
@app.post("/search", response_model=List[FounderResult], tags=["Search"])
async def search_founders(
    query: SearchQuery, 
    current_user: str = Depends(get_current_user)
):
    # Validate query
    validated_query = validate_search_query(query.query)
    validated_limit = validate_limit(query.limit)
    
    if not rag_service.is_ready():
        raise HTTPException(status_code=503, detail="RAG system not ready")
    
    results = rag_service.search_founders(validated_query, validated_limit)
    
    founder_results = []
    for result in results:
        founder_results.append(FounderResult(**result))
    
    return founder_results

@app.get("/founder/{founder_id}", response_model=FounderDetails, tags=["Founders"])
async def get_founder_details(
    founder_id: str, 
    current_user: str = Depends(get_current_user)
):
    # Basic validation
    if not founder_id or not founder_id.strip():
        raise HTTPException(status_code=400, detail="Founder ID required")
    
    founder_data = rag_service.get_founder_by_id(founder_id.strip())
    
    if founder_data is None:
        raise HTTPException(status_code=404, detail="Founder not found")
    
    return FounderDetails(**founder_data)

@app.get("/stats", tags=["Analytics"])
async def get_statistics(current_user: str = Depends(get_current_user)):
    return rag_service.get_stats()

# Demo endpoint for testing without auth
@app.post("/demo/search", response_model=List[FounderResult], tags=["Demo"])
async def demo_search(query: SearchQuery):
    """Demo endpoint for testing - no auth required"""
    validated_query = validate_search_query(query.query)
    
    if not rag_service.is_ready():
        raise HTTPException(status_code=503, detail="RAG system not ready")
    
    # Limit demo results to 3
    results = rag_service.search_founders(validated_query, min(query.limit or 3, 3))
    
    founder_results = []
    for result in results:
        founder_results.append(FounderResult(**result))
    
    return founder_results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
