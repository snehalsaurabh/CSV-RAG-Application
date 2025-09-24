# Founder RAG Chat - Design Note/Technical Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Dataset Creation](#dataset-creation)
3. [Technology Stack](#technology-stack)
4. [Architecture \& Implementation](#architecture--implementation)
5. [Local Development Setup](#local-development-setup)
6. [Deployment Strategy](#deployment-strategy)
7. [Authentication \& Security](#authentication--security)
8. [Edge Cases \& Error Handling](#edge-cases--error-handling)
9. [Production Best Practices](#production-best-practices)
10. [Demo URLs \& Credentials](#demo-urls--credentials)

## Project Overview

**Goal**: Build a small RAG (Retrieval-Augmented Generation) chat system that finds and explains the best matches from a founder dataset using natural language queries.

**Live Demo**:

- Frontend: `https://antler-rag-frontend.vercel.app`
- Backend API: `https://antler-rag-backend.onrender.com`
- API Docs: `https://antler-rag-backend.onrender.com/docs`

**Demo Credentials**:

- Username: `demo`
- Password: `demo`


## Dataset Creation

### Dataset Structure

Created a synthetic dataset of 700+ founder profiles with the following columns:

- `id`: UUID4 unique identifier
- `founder_name`: Full name (realistic combinations)
- `email`: Professional email format (fake but realistic)
- `role`: Founder/Co-founder/Engineer/PM/Investor/Other
- `company`: Company names across various industries
- `location`: City, Country format (global distribution)
- `idea`: 1-2 sentence business idea description
- `about`: 2-4 sentence professional bio
- `keywords`: Comma-separated industry tags (healthtech, AI, marketplace, etc.)
- `stage`: none/pre-seed/seed/series A/growth
- `linkedin`: LinkedIn URL format
- `notes`: Optional additional information


### Sample Dataset Rows

<div style="overflow-x: auto;">

| ID | Founder Name | Email | Role | Company | Location | Idea | About | Keywords | Stage | LinkedIn | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| a1b2c3d4-e5f6-7890-abcd-ef1234567890 | Sarah Chen | sarah.chen@medtech.ai | Founder | MedTech AI | San Francisco, USA | Building AI-powered diagnostic tools for early cancer detection. Leveraging machine learning to analyze medical imaging data. | Former Google engineer with 8 years in ML. Led health tech initiatives at Stanford Medicine. Published researcher in computer vision applications for healthcare. | healthtech, AI, machine learning, diagnostics | seed | [LinkedIn](https://linkedin.com/in/sarahchen) | Featured in Forbes 30 Under 30 |
| b2c3d4e5-f6g7-8901-bcde-f23456789012 | Raj Patel | raj.patel@fintech.in | Co-founder | FinanceFlow | Mumbai, India | Creating digital banking solutions for underbanked populations in India. Mobile-first approach with local language support. | Ex-Goldman Sachs analyst turned fintech entrepreneur. IIT Delhi graduate with expertise in financial systems and emerging markets. | fintech, banking, mobile, emerging markets | pre-seed | [LinkedIn](https://linkedin.com/in/rajpatel) | Y Combinator alum |
| 2e065d46-09c1-45a4-807b-03daab2b69cc | Jerry Sullivan | jsullivan@smith-nunez.com | PM | Smith-Nunez | Martinique | Innovative robotics solution for enterprise clients | Ex-Adobe product manager with expertise in UX research, tokenomics design. Product manager at Smith-Nunez driving robotics product strategy. Previously featured in TechCrunch and Wired. | robotics, IoT, cloud, biotech | pre-seed | [LinkedIn](https://linkedin.com/in/jerry-sullivan-670) | Interested in partnerships |
| 118e1b1d-ecc0-4a57-91f8-b4f1cb0f865c | Aaron Cortez | acortez@avilaplc.ai | Co-founder | Avila PLC | Aruba | AI-enhanced agriculture service for modern businesses | Berkeley PhD with expertise in deep learning, data engineering, cybersecurity. Currently building Avila PLC to revolutionize the agriculture industry. Previously featured in TechCrunch and Wired. | agriculture, adtech, cleantech, developer tools | none | [LinkedIn](https://linkedin.com/in/aaron-cortez-361) | Looking for technical co-founder |
| 6b0cbe94-881d-4a8c-b8bc-2a5d8a896c39 | Michael Jones | michael@rodriguezbuchan.co | Founder | Rodriguez, Buchanan and Turner | Benin | Carbon credit trading fintech platform | Stanford MBA graduate with expertise in operations management, supply chain optimization, quantitative analysis. Currently building Rodriguez, Buchanan and Turner to revolutionize the fintech industry. Previously led team of 50+ engineers. | fintech, fashion, beauty, gaming, AI | series A | [LinkedIn](https://linkedin.com/in/michael-jones-852) | - |
| 98a5729a-df38-468c-a301-ec5b59558fa7 | Douglas Mcintosh | dmcintosh@foster-guerrero.io | Investor | Foster-Guerrero | Lebanon | Innovative retail solution for enterprise clients | Former Bain & Company consultant with expertise in computer vision, bioinformatics, enterprise partnerships. Angel investor and advisor specializing in retail startups. Previously scaled from 0 to 100 employees. | retail, biotech | none | [LinkedIn](https://linkedin.com/in/douglas-mcintosh-766) | - |
| f83ef178-4c59-4676-8d1e-cfa780ed49e2 | Christopher Robinson | christopher@myerssalinasand.co | Other | Myers, Salinas and Gardner | North Macedonia | Computer vision solution for quality control in manufacturing | Former Google engineer with expertise in UX research, sales strategy. Working in the AI space with focus on innovation and growth. | AI, AR, analytics, healthtech, VR | growth | [LinkedIn](https://linkedin.com/in/christopher-robinson-976) | - |
| ec465e60-7849-4d64-b0b9-d130fc907736 | Brianna Byrd | bbyrd@wongbernardands.io | Investor | Wong, Bernard and Smith | Tunisia | Consumer-focused IoT platform with mobile-first approach | PhD in Computer Science with expertise in operations management, data visualization. Angel investor and advisor specializing in IoT startups. Previously achieved $1M ARR. | IoT, biotech, adtech, cloud | series A | [LinkedIn](https://linkedin.com/in/brianna-byrd-898) | - |
| 5b52b410-b078-4826-8830-6f0139015e67 | Kristen Martinez | kristen@armstronggroup.io | Founder | Armstrong Group | Mauritania | AI-enhanced biotech service for modern businesses | Oxford MBA graduate with expertise in cloud architecture, full-stack development. Currently building Armstrong Group to revolutionize the biotech industry. | biotech, cloud, cybersecurity | seed | [LinkedIn](https://linkedin.com/in/kristen-martinez-998) | Expanding to European markets |

</div>

### Dataset Generation Process

1. **Programmatic Creation**: Used Python scripts with faker library for realistic data generation
2. **Industry Distribution**: Balanced across healthtech, fintech, edtech, climate, AI, marketplace sectors
3. **Geographic Diversity**: Global representation with focus on major startup ecosystems
4. **Stage Distribution**: Realistic funding stage distribution matching market patterns
5. **Quality Assurance**: Manual review of sample entries for realism and consistency

## Technology Stack

### Backend (Python/FastAPI)

```python
# Core Dependencies
fastapi>=0.104.0          # Modern async web framework
uvicorn[standard]>=0.24.0 # ASGI server with performance optimizations
python-jose[cryptography]>=3.3.0  # JWT token handling
passlib[bcrypt]>=1.7.4    # Secure password hashing
python-multipart>=0.0.6   # Form data parsing

# ML & RAG Components
sentence-transformers>=2.2.0  # Text embeddings (all-MiniLM-L6-v2)
faiss-cpu>=1.7.4             # Vector similarity search
pandas>=2.1.0                # Data manipulation
numpy>=1.24.0                # Numerical operations
google-generativeai>=0.7.0   # Gemini AI for explanations

# Utilities
python-dotenv>=1.0.0      # Environment variable management
```


### Frontend (React/TypeScript)

```json
{
  "dependencies": {
    "react": "^19.1.1",           // Latest React with concurrent features
    "react-dom": "^19.1.1",      // DOM rendering
    "react-router-dom": "^6.26.2", // Client-side routing
    "axios": "^1.7.7"            // HTTP client with interceptors
  },
  "devDependencies": {
    "vite": "^7.1.7",            // Fast build tool
    "typescript": "~5.8.3",      // Type safety
    "@vitejs/plugin-react": "^5.0.3" // React integration
  }
}
```


### Infrastructure

- **Backend Hosting**: Render.com (Standard tier - 2GB RAM)
- **Frontend Hosting**: Vercel (Edge deployment)
- **Database**: In-memory (demonstration purposes)
- **Vector Search**: FAISS in-memory index
- **AI Service**: Google Gemini 1.5 Flash


## Architecture \& Implementation

### RAG System Design

#### 1. Embedding Generation

```python
# Using sentence-transformers for semantic embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Comprehensive text creation for embedding (from rag.py)
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

# Generate embeddings with progress tracking
embeddings = model.encode(texts, show_progress_bar=True)
```


#### 2. Vector Indexing with FAISS

```python
# Create FAISS index for cosine similarity search
dimension = self.embeddings.shape[1]  # 384 dimensions for all-MiniLM-L6-v2
index = faiss.IndexFlatIP(dimension)  # Inner product index

# Normalize embeddings for cosine similarity calculation
faiss.normalize_L2(self.embeddings)
index.add(self.embeddings.astype('float32'))
```


#### 3. Search Pipeline

```python
def search_founders(self, query: str, limit: int = 5) -> List[dict]:
    """Search for founders using vector similarity with comprehensive results"""
    try:
        if self.model is None or self.index is None:
            return []
        
        # 1. Generate and normalize query embedding
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        # 2. Vector similarity search using FAISS
        scores, indices = self.index.search(query_embedding.astype('float32'), limit)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.founders_df):
                founder = self.founders_df.iloc[idx]
                
                # 3. Generate AI-powered explanations
                snippet = self.generate_match_explanation_gemini(query, founder)
                matched_fields = self.identify_matched_fields(query, founder)
                
                # 4. Structure results with full provenance
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
```


#### 4. Explanation Generation

```python
def generate_match_explanation_gemini(self, query: str, founder) -> str:
    """Generate match explanations using Google Gemini AI with fallback"""
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
        
        Generate a concise 1-2 sentence explanation of why this founder 
        matches the query. Focus on the most relevant matching aspects. 
        Start with "Matched on" and cite specific fields.
        
        Example: "Matched on keywords: healthtech, AI and role: Founder 
        with experience in building diagnostic platforms for early disease detection."
        """
        
        response = self.gemini_model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return self.generate_match_explanation_fallback(query, founder)
```

#### 5. Field-Level Match Identification

```python
def identify_matched_fields(self, query: str, founder) -> List[str]:
    """Identify which specific fields contributed to the match for citation"""
    matched = []
    query_lower = query.lower()
    
    # Check keyword matches
    keywords = [k.strip().lower() for k in founder['keywords'].split(',')]
    if any(keyword in query_lower for keyword in keywords):
        matched.append("keywords")
    
    # Check role, location, company, stage matches
    if founder['role'].lower() in query_lower:
        matched.append("role")
    if founder['company'].lower() in query_lower:
        matched.append("company")
    if any(loc.lower() in query_lower for loc in founder['location'].split(', ')):
        matched.append("location")
    if founder['stage'].lower() in query_lower:
        matched.append("stage")
    
    # Check semantic matches in text fields
    about_words = set(founder['about'].lower().split())
    idea_words = set(founder['idea'].lower().split())
    query_words = set(query_lower.split())
    
    if about_words.intersection(query_words):
        matched.append("about")
    if idea_words.intersection(query_words):
        matched.append("idea")
    
    # Return matched fields or default to keywords/about
    return matched if matched else ["keywords", "about"]
```

### Authentication System

#### JWT Implementation (Production-Ready)

```python
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timezone, timedelta

# Secure password hashing with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hardcoded demo users (FOR DEMONSTRATION ONLY) - use secure DB in production
USERS_DB = {
    "demo": "$2b$12$xyZc9jWa0iMifjL9BrZ31.ZpHfc.ysr3KP6LpAC3DX8nbfmdc63he",  # demo
    "admin": "$2b$12$.QcUVLxReQlfviq0X3hCOOLjCfFubuaf6AIUh1cQXOzQqzDCNf8k2",  # demo
    "reviewer": "$2b$12$UNstFuAza1Epla3EvC0HhuCB4vqn13tEp38EfDbC4ffPZDpzIm0lC"  # demo
}

def create_access_token(data: dict):
    """Create JWT token with timezone-aware expiration"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token with comprehensive validation"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Proper expiration checking
        exp = payload.get("exp")
        if exp is None:
            raise HTTPException(status_code=401, detail="Token missing expiration")
        
        if datetime.now(timezone.utc).timestamp() > exp:
            raise HTTPException(status_code=401, detail="Token expired")
            
        return username
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password using bcrypt with error handling"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False
```

**Note**: For this demonstration, we use hardcoded bcrypt hashes. In production, passwords would be properly hashed during user registration.

### Frontend Architecture

#### React Structure

```typescript
// Type-safe API integration
interface FounderResult {
  id: string;
  founder_name: string;
  role: string;
  company: string;
  location: string;
  snippet: string;
  similarity_score: number;
  matched_fields: string[];
  row_id: number;
}

// Context-based authentication
const AuthContext = createContext<{
  user: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}>()
```


#### Search UI Features

- **Real-time search** with 600ms debouncing
- **Results caching** to avoid duplicate API calls
- **Pagination** with intersection observer for infinite scroll
- **Progressive disclosure** with "Show More" for detailed views
- **Field-level citations** showing which data fields contributed to matches


## Local Development Setup

### Prerequisites

```bash
# Python 3.8+
python --version

# Node.js 18+
node --version
npm --version
```


### Backend Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd AntlerIndia/backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Environment variables
cp .env.example .env
# Edit .env file:
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production-12345
GOOGLE_API_KEY=your-gemini-api-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 5. Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```


### Frontend Setup

```bash
# 1. Navigate to frontend directory
cd AntlerIndia/frontend

# 2. Install dependencies
npm install

# 3. Environment setup
cp .env.example .env.local
# Edit .env.local:
VITE_API_BASE_URL=http://localhost:8000

# 4. Run development server
npm run dev
```


### Dataset Placement

```bash
# Ensure dataset is in correct location
AntlerIndia/
├── backend/
│   ├── data/
│   │   └── founders_dataset.csv  # Place your CSV here
│   └── app/
└── frontend/
```


## Deployment Strategy

### Production Deployment

#### Backend (Render.com)

```bash
# Deployment Configuration
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Root Directory: backend
Instance Type: Standard ($25/month for 2GB RAM)

# Environment Variables in Render Dashboard
SECRET_KEY=production-secret-key-256-bits
GOOGLE_API_KEY=gemini-api-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```


#### Frontend (Vercel)

```bash
# Build Configuration
Framework: Vite
Build Command: npm run build
Output Directory: dist
Root Directory: frontend

# Environment Variables in Vercel
VITE_API_BASE_URL=https://antler-rag-backend.onrender.com
```


#### CORS Configuration

```python
# Production CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://antler-rag-frontend.vercel.app",
        "http://localhost:5173"  # Local development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
```


## Authentication \& Security

### Current Implementation (Demo)

- **Hardcoded users**: For demonstration purposes only
- **Bcrypt hashes**: Pre-computed for demo accounts
- **JWT tokens**: 30-minute expiration with proper validation
- **HTTPS enforcement**: All production traffic over TLS


### Production Security Measures

The following will be applied when moving to production:

#### Password Security

```python
# Proper user registration flow
def register_user(username: str, password: str):
    # Validate password strength
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    
    # Hash password with bcrypt
    hashed = pwd_context.hash(password)
    
    # Store in secure database
    db.users.insert({
        "username": username,
        "password_hash": hashed,
        "created_at": datetime.utcnow()
    })
```


#### Environment Security

```python
# Production environment variable validation
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY or len(SECRET_KEY) < 32:
    raise ValueError("SECRET_KEY must be at least 32 characters")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is required")
```


#### Database Security

```python
# Production database with encryption
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Encrypted connection with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    echo=False  # Never log SQL in production
)
```


### OAuth Integration (Recommended)

```python
# GitHub OAuth example
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name='github',
    client_id=os.getenv('GITHUB_CLIENT_ID'),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    server_metadata_url='https://api.github.com/.well-known/oauth_config',
    client_kwargs={'scope': 'user:email'}
)
```


## Edge Cases \& Error Handling

### Search Edge Cases

- **Empty queries**: Return helpful prompt suggestions
- **Very short queries**: Minimum 3 character requirement
- **Special characters**: Sanitized but preserved for search context
- **Rate limiting**: 10 requests per minute per IP
- **Large result sets**: Pagination with maximum 50 results per query


### System Resilience

- **API timeouts**: 30-second timeout with retry logic
- **Memory management**: Batch processing for large embeddings
- **Gemini API failures**: Fallback to rule-based explanations
- **FAISS index corruption**: Automatic re-indexing on startup failure
- **Database connectivity**: Connection pooling with retry mechanism


### Error Response Format

```json
{
  "error": "search_failed",
  "message": "Unable to process search query",
  "details": {
    "query": "original user query",
    "timestamp": "2025-09-24T20:30:00Z",
    "request_id": "uuid-for-tracking"
  }
}
```


### Monitoring \& Logging

```python
import logging
from datetime import datetime

# Structured logging for production
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def log_search_event(query: str, results_count: int, response_time: float):
    logger.info({
        "event": "search_completed",
        "query": query[:100],  # Truncate for privacy
        "results_count": results_count,
        "response_time_ms": response_time * 1000,
        "timestamp": datetime.utcnow().isoformat()
    })
```

## Production Best Practices

The following best practices will be implemented when moving to production:

### Infrastructure Scaling

```yaml
# Recommended production architecture
Load Balancer: Cloudflare/AWS ALB
  ├── Frontend: Vercel Edge Network
  ├── API Gateway: AWS API Gateway
  └── Backend Cluster: 
      ├── App Servers: 3x instances (auto-scaling)
      ├── Database: PostgreSQL (managed)
      ├── Cache: Redis cluster
      └── Search: Elasticsearch/Vector DB
```


### Database Design

```sql
-- Production database schema
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE founders (
    id UUID PRIMARY KEY,
    founder_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    role VARCHAR(50),
    company VARCHAR(255),
    location VARCHAR(255),
    idea TEXT,
    about TEXT,
    keywords TEXT,
    stage VARCHAR(50),
    linkedin VARCHAR(255),
    notes TEXT,
    embedding VECTOR(384),  -- For pgvector
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_founders_embedding ON founders 
USING ivfflat (embedding vector_cosine_ops);
```


### Security Headers

```python
from fastapi.middleware.security import SecurityHeadersMiddleware

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    lambda request, call_next: call_next(request).then(
        lambda response: response.headers.update({
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'"
        })
    )
)
```


### Performance Optimization

```python
# Production caching strategy
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis

# Redis caching for search results
@cache(expire=300)  # 5-minute cache
async def search_founders_cached(query: str, limit: int):
    return await search_founders(query, limit)

# Connection pooling for database
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600
)
```


### Monitoring \& Observability

```python
# Application Performance Monitoring
from prometheus_client import Counter, Histogram, start_http_server

search_requests = Counter('search_requests_total', 'Total search requests')
search_duration = Histogram('search_duration_seconds', 'Search request duration')

@search_duration.time()
async def search_with_metrics(query: str):
    search_requests.inc()
    return await search_founders(query)

# Health checks for orchestration
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": await check_database_health(),
        "ai_service": await check_gemini_health(),
        "search_index": rag_service.is_ready()
    }
```


## Demo URLs \& Credentials

### Live Application

- **Frontend**: [Website](https://csv-rag-application-git-main-snehalsaurabhs-projects.vercel.app)
- **API Documentation**: [Docs](https://csv-rag-application-1.onrender.com/docs)
- **GitHub Repository**: [https://github.com/snehalsaurabh/CSV-RAG-Application](https://github.com/snehalsaurabh/CSV-RAG-Application)


### Demo Credentials

All demo accounts use the same password for simplicity:


| Username | Password | Role |
| :-- | :-- | :-- |
| demo | demo | Standard User |
| admin | demo | Administrator |
| reviewer | demo | Reviewer |

### Example Queries

- "healthtech founder in India with AI background"
- "fintech startup in pre-seed stage"
- "climate tech entrepreneur in San Francisco"
- "marketplace founder with Series A funding limit: 3"


### Security Notice

⚠️ **Important**: The demo passwords are intentionally simple and exposed for evaluation purposes. In production, these would be:

1. Generated with proper entropy (12+ characters)
2. Never hardcoded in source code
3. Stored only as bcrypt hashes
4. Managed through secure user registration flows
5. Protected with additional security measures (2FA, account lockout, etc.)

***

**Built with**: FastAPI, React, TypeScript, Sentence Transformers, FAISS, Gemini AI
**Deployment**: Render.com (Backend) + Vercel (Frontend)
**Completion Time**: ~8 hours of focused development
**AI Assistance**: Used GitHub Copilot for boilerplate code generation and debugging





