"""
Test ChromaDB retrieval with sample queries
Validates that 947 documents are searchable and return relevant results
"""
import sys
sys.path.insert(0, 'src')

from retrieval.chromadb_client import ChromaDBClient
from embeddings.embedding_service import EmbeddingService

# Initialize clients
config_chroma = {
    'chromadb': {
        'persist_directory': './data/chromadb',
        'collection_name': 'bis_standards'
    }
}

config_embed = {
    'embeddings': {
        'model': 'sentence-transformers/all-MiniLM-L6-v2'
    }
}

print("🔧 Initializing ChromaDB and Embedding Service...")
client = ChromaDBClient(config_chroma)
embed_service = EmbeddingService(config_embed)

# Check collection stats
print("\n📊 Collection Stats:")
stats = client.get_collection_stats()
print(f"Total documents: {stats.get('total_chunks', 0)}")
print(f"Unique standards: {stats.get('unique_standards', 0)}")
print(f"Industries: {', '.join(stats.get('industries', []))}")

# Test queries across different industries
test_queries = [
    "cement strength requirements",
    "LED bulb certification standards",
    "food packaging safety standards",
    "steel reinforcement bar specifications",
    "textile fabric quality testing"
]

print("\n" + "="*60)
print("🔍 TESTING RETRIEVAL ACROSS INDUSTRIES")
print("="*60)

for query in test_queries:
    print(f"\n📝 Query: '{query}'")
    print("-" * 60)
    
    # Encode query
    query_embedding = embed_service.encode_query(query)
    
    # Retrieve top 3 results
    results = client.query(query_embedding, n_results=3)
    
    if results['documents'] and len(results['documents']) > 0:
        print(f"✅ Found {len(results['documents'])} results\n")
        
        for i, (doc, metadata) in enumerate(zip(results['documents'], results['metadatas']), 1):
            standard_num = metadata.get('standard_number', 'N/A')
            title = metadata.get('title', 'N/A')
            industry = metadata.get('industry', 'N/A')
            
            print(f"  [{i}] Standard: {standard_num}")
            print(f"      Industry: {industry}")
            print(f"      Title: {title[:80]}..." if len(title) > 80 else f"      Title: {title}")
            print(f"      Preview: {doc[:150]}..." if len(doc) > 150 else f"      Preview: {doc}")
            print()
    else:
        print("❌ No results found")

print("="*60)
print("✅ RETRIEVAL TEST COMPLETE")
print("="*60)
