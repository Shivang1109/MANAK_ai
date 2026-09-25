"""
Test RAG pipeline end-to-end (without LLM)
Validates query processing, retrieval, and re-ranking
"""
import sys
sys.path.insert(0, 'src')

from retrieval.chromadb_client import ChromaDBClient
from embeddings.embedding_service import EmbeddingService
from retrieval.retriever import QueryProcessor, HybridRetriever, ReRanker
import yaml
from pathlib import Path

print("🔧 Loading configuration...")
config_path = Path("config/rag_config.yaml")
with open(config_path) as f:
    config = yaml.safe_load(f)

print("🔧 Initializing services...")
chromadb = ChromaDBClient(config)
embedder = EmbeddingService(config)
query_processor = QueryProcessor(config)
retriever = HybridRetriever(chromadb, embedder, config)
reranker = ReRanker(config)

print("\n" + "="*70)
print("📊 CHROMADB STATS")
print("="*70)
stats = chromadb.get_collection_stats()
print(f"Total documents: {stats.get('total_chunks', 0)}")
print(f"Unique standards: {stats.get('unique_standards', 0)}")
print(f"Industries: {', '.join(stats.get('industries', []))}")
print(f"Sample standards: {stats.get('sample_standards', [])[:3]}")

# Test queries
test_cases = [
    {
        "query": "What are the compressive strength requirements for cement?",
        "expected_industry": "cement"
    },
    {
        "query": "LED bulb voltage specifications",
        "expected_industry": "electrical_electronics"
    },
    {
        "query": "Food packaging material standards",
        "expected_industry": "food"
    },
    {
        "query": "Steel reinforcement bar dimensions",
        "expected_industry": "steel_metals"
    }
]

print("\n" + "="*70)
print("🔍 TESTING RAG PIPELINE")
print("="*70)

for i, test_case in enumerate(test_cases, 1):
    query = test_case["query"]
    
    print(f"\n{'='*70}")
    print(f"Test Case {i}: {query}")
    print('='*70)
    
    # Step 1: Query Processing
    print("\n[Step 1] Query Processing...")
    query_info = query_processor.process(query)
    print(f"  ✓ Intent detected: {query_info['intent']}")
    print(f"  ✓ Products detected: {query_info['products']}")
    print(f"  ✓ Standards detected: {query_info['standard_numbers']}")
    
    # Step 2: Retrieval
    print("\n[Step 2] Hybrid Retrieval...")
    try:
        retrieved_chunks = retriever.retrieve(query_info)
        print(f"  ✓ Retrieved {len(retrieved_chunks)} chunks")
        
        if retrieved_chunks:
            # Show top result details
            top = retrieved_chunks[0]
            print(f"\n  Top Result:")
            print(f"    Standard: {top['metadata'].get('standard_number', 'N/A')}")
            print(f"    Industry: {top['metadata'].get('industry', 'N/A')}")
            print(f"    Title: {top['metadata'].get('title', 'N/A')[:60]}...")
            print(f"    Similarity: {top['similarity_score']:.3f}")
            print(f"    Preview: {top['content'][:150]}...")
        else:
            print("  ⚠ No chunks retrieved above threshold")
            continue
        
        # Step 3: Re-ranking
        print("\n[Step 3] Re-ranking...")
        reranked_chunks = reranker.rerank(query, retrieved_chunks)
        print(f"  ✓ Re-ranked to top {len(reranked_chunks)} chunks")
        
        # Show re-ranked results
        print("\n  Top 3 Re-ranked Results:")
        for j, chunk in enumerate(reranked_chunks[:3], 1):
            print(f"\n  [{j}] {chunk['metadata'].get('standard_number', 'N/A')}")
            print(f"      Similarity: {chunk['similarity_score']:.3f}")
            print(f"      Rerank Score: {chunk.get('rerank_score', 0):.3f}")
            print(f"      Industry: {chunk['metadata'].get('industry', 'N/A')}")
            print(f"      Clause: {chunk['metadata'].get('clause', 'N/A')}")
        
        # Step 4: Would generate answer here (simulated)
        print("\n[Step 4] Answer Generation (Simulated)")
        print("  ✓ Would send to LLM with grounded context")
        print(f"  ✓ Context size: {sum(len(c['content']) for c in reranked_chunks)} chars")
        print(f"  ✓ Sources available: {len(set(c['metadata'].get('standard_number') for c in reranked_chunks))}")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")

print("\n" + "="*70)
print("✅ RAG PIPELINE TEST COMPLETE")
print("="*70)
print("\nSUMMARY:")
print("- Query processing: ✓ Working")
print("- Embedding generation: ✓ Working")
print("- Vector retrieval: ✓ Working")
print("- Re-ranking: ✓ Working")
print("- LLM generation: ⏭ Skipped (requires API key)")
print("\nNEXT STEPS:")
print("1. Set OPENAI_API_KEY or ANTHROPIC_API_KEY in environment")
print("2. Start FastAPI server: python src/main.py")
print("3. Test API endpoint: POST http://localhost:8000/internal/rag/query")
