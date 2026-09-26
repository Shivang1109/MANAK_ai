"""
ManakAI RAG Service - FastAPI Application
Main entry point for the RAG engine
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from loguru import logger
import yaml
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables (.env)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Import services
from retrieval.chromadb_client import ChromaDBClient
from embeddings.embedding_service import EmbeddingService
from retrieval.retriever import QueryProcessor, HybridRetriever, ReRanker
from llm.llm_service import LLMService

# Load configuration
config_path = Path(__file__).parent.parent / "config" / "rag_config.yaml"
with open(config_path) as f:
    config = yaml.safe_load(f)

# Initialize FastAPI
app_config = config.get('api', {})
app = FastAPI(
    title=app_config.get('title', 'ManakAI RAG Engine'),
    version=app_config.get('version', '1.0.0'),
    description=app_config.get('description', 'RAG engine for BIS standards')
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services (singleton pattern)
class Services:
    chromadb: ChromaDBClient = None
    embedder: EmbeddingService = None
    query_processor: QueryProcessor = None
    retriever: HybridRetriever = None
    reranker: ReRanker = None
    llm_service: LLMService = None

services = Services()


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting ManakAI RAG Service...")
    
    try:
        # Initialize services
        services.chromadb = ChromaDBClient(config)
        services.embedder = EmbeddingService(config)
        services.query_processor = QueryProcessor(config)
        services.retriever = HybridRetriever(services.chromadb, services.embedder, config)
        services.reranker = ReRanker(config)
        services.llm_service = LLMService(config)
        
        logger.success("All services initialized successfully")
        
        # Get collection stats
        stats = services.chromadb.get_collection_stats()
        logger.info(f"ChromaDB stats: {stats}")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise


# Pydantic models
class QueryRequest(BaseModel):
    query: str = Field(..., description="User query")
    session_id: Optional[str] = Field(None, description="Session ID for context")
    metadata_filter: Optional[Dict] = Field(None, description="Metadata filters")
    conversation_history: Optional[List[Dict]] = Field(None, description="Previous messages")

class SourceInfo(BaseModel):
    standard_number: Optional[str]
    title: Optional[str]
    clause: Optional[str]
    page: Optional[int]
    document_type: Optional[str]
    source_url: Optional[str]
    content_preview: Optional[str]

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceInfo]
    confidence: str
    confidence_score: float
    query_info: Dict
    retrieved_chunks_count: int
    processing_time_ms: int

class HealthResponse(BaseModel):
    status: str
    version: str
    chromadb_status: str
    total_documents: int

class StatsResponse(BaseModel):
    total_chunks: int
    unique_standards: int
    industries: List[str]
    document_types: List[str]
    sample_standards: List[str]


# API Endpoints

@app.get("/", response_model=Dict)
async def root():
    """Root endpoint"""
    return {
        "service": "ManakAI RAG Engine",
        "version": app_config.get('version', '1.0.0'),
        "status": "operational"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        stats = services.chromadb.get_collection_stats()
        
        return HealthResponse(
            status="healthy",
            version=app_config.get('version', '1.0.0'),
            chromadb_status="connected",
            total_documents=stats.get('total_chunks', 0)
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get knowledge base statistics"""
    try:
        stats = services.chromadb.get_collection_stats()
        
        return StatsResponse(
            total_chunks=stats.get('total_chunks', 0),
            unique_standards=stats.get('unique_standards', 0),
            industries=stats.get('industries', []),
            document_types=stats.get('document_types', []),
            sample_standards=stats.get('sample_standards', [])
        )
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/internal/rag/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Main RAG query endpoint
    
    This is called by the Spring Boot backend with user queries
    """
    start_time = datetime.now()
    
    try:
        logger.info(f"Query received: {request.query}")
        
        # Step 1: Process query
        query_info = services.query_processor.process(request.query)
        logger.info(f"Query intent: {query_info['intent']}")
        
        # Step 2: Retrieve relevant chunks
        retrieved_chunks = services.retriever.retrieve(
            query_info,
            metadata_filter=request.metadata_filter
        )
        
        if not retrieved_chunks:
            logger.warning("No relevant chunks retrieved")
            return QueryResponse(
                answer="I don't have sufficient information in the available BIS documents to answer this question accurately. Please verify with official BIS sources.",
                sources=[],
                confidence="low",
                confidence_score=0.0,
                query_info=query_info,
                retrieved_chunks_count=0,
                processing_time_ms=int((datetime.now() - start_time).total_seconds() * 1000)
            )
        
        # Step 3: Re-rank chunks
        reranked_chunks = services.reranker.rerank(request.query, retrieved_chunks)
        logger.info(f"Re-ranked to top {len(reranked_chunks)} chunks")
        
        # Step 4: Generate answer with LLM
        result = services.llm_service.generate_answer(
            query=request.query,
            retrieved_chunks=reranked_chunks,
            conversation_history=request.conversation_history
        )
        
        # Step 5: Build response
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return QueryResponse(
            answer=result['answer'],
            sources=[SourceInfo(**src) for src in result['sources']],
            confidence=result['confidence'],
            confidence_score=result['confidence_score'],
            query_info=query_info,
            retrieved_chunks_count=len(retrieved_chunks),
            processing_time_ms=processing_time
        )
    
    except Exception as e:
        logger.error(f"Query processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@app.get("/search/standards", response_model=List[Dict])
async def search_standards(product: str, industry: Optional[str] = None):
    """
    Search for applicable standards by product
    
    Used for "Find Applicable Standard" feature
    """
    try:
        logger.info(f"Standard search: product={product}, industry={industry}")
        
        # Build search query
        query = f"Which Indian Standard applies to {product}?"
        
        query_info = services.query_processor.process(query)
        
        # Add industry filter if provided and not 'all'
        metadata_filter = {}
        if industry and industry.lower() != 'all':
            metadata_filter['industry'] = industry
        
        # Retrieve
        chunks = services.retriever.retrieve(query_info, metadata_filter if metadata_filter else None)
        
        # Fallback if no chunks with industry filter
        if not chunks and metadata_filter:
            logger.info(f"No chunks found with industry filter '{industry}', falling back to all industries")
            chunks = services.retriever.retrieve(query_info, None)
        
        # Extract unique standards
        standards = {}
        for chunk in chunks:
            std_num = chunk['metadata'].get('standard_number')
            if std_num and std_num not in standards:
                standards[std_num] = {
                    'standard_number': std_num,
                    'title': chunk['metadata'].get('title'),
                    'revision': chunk['metadata'].get('revision'),
                    'relevance': chunk['similarity_score'],
                    'document_type': chunk['metadata'].get('document_type')
                }
        
        # Sort by relevance
        result = sorted(standards.values(), key=lambda x: x['relevance'], reverse=True)
        
        return result
    
    except Exception as e:
        logger.error(f"Standard search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    host = app_config.get('host', '0.0.0.0')
    port = app_config.get('port', 8000)
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
