from fastapi import HTTPException
import re

def validate_search_query(query: str) -> str:
    """Basic validation for search queries"""
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # Remove potentially problematic characters but keep it simple
    sanitized = query.strip()
    
    # Basic length check
    if len(sanitized) > 500:
        raise HTTPException(status_code=400, detail="Query too long (max 500 characters)")
    
    return sanitized

def validate_limit(limit: int) -> int:
    """Validate query limit parameter"""
    if limit is None:
        return 5
    
    # Allow reasonable limits for demo
    return min(max(limit, 1), 20)  # Between 1 and 20 results
