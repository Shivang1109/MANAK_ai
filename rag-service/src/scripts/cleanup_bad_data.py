"""
Remove low-quality chunks (< 200 chars) from ChromaDB
Keep only demo data and any other good quality chunks
"""

import chromadb

def cleanup_database():
    """Remove all chunks with content length < 200 characters"""
    
    client = chromadb.PersistentClient(path="./data/chromadb")
    collection = client.get_collection("bis_standards")
    
    print("Analyzing database...")
    
    # Get all data
    all_data = collection.get(include=['documents', 'metadatas'])
    
    total = len(all_data['ids'])
    print(f"Total chunks before cleanup: {total}")
    
    # Find chunks to delete (short ones without demo flag)
    to_delete = []
    kept = []
    
    for i, (doc_id, doc, meta) in enumerate(zip(all_data['ids'], all_data['documents'], all_data['metadatas'])):
        doc_length = len(doc)
        is_demo = meta.get('is_demo', 'false')
        
        # Keep demo data OR chunks with good content (>= 300 chars)
        if is_demo == 'true' or doc_length >= 300:
            kept.append({
                'id': doc_id,
                'length': doc_length,
                'is_demo': is_demo,
                'standard': meta.get('standard_number', 'N/A')
            })
        else:
            to_delete.append(doc_id)
    
    print(f"\nChunks to KEEP: {len(kept)}")
    print(f"Chunks to DELETE: {len(to_delete)}")
    
    if to_delete:
        print(f"\nDeleting {len(to_delete)} low-quality chunks...")
        
        # Delete in batches of 100
        batch_size = 100
        for i in range(0, len(to_delete), batch_size):
            batch = to_delete[i:i+batch_size]
            collection.delete(ids=batch)
            print(f"  Deleted batch {i//batch_size + 1} ({len(batch)} chunks)")
        
        print("\n✅ Cleanup complete!")
    else:
        print("\n✅ No cleanup needed - all chunks are good quality!")
    
    # Final stats
    final_count = collection.count()
    print(f"\nFinal database stats:")
    print(f"Total chunks: {final_count}")
    
    # Show kept chunks breakdown
    demo_chunks = [c for c in kept if c['is_demo'] == 'true']
    good_chunks = [c for c in kept if c['is_demo'] != 'true']
    
    print(f"  - Demo chunks: {len(demo_chunks)}")
    print(f"  - Other good chunks (>=300 chars): {len(good_chunks)}")
    
    if demo_chunks:
        print("\n📋 Demo data chunks:")
        for c in demo_chunks:
            print(f"  • {c['standard']} - {c['length']} chars")
    
    # Test retrieval
    print("\n🔍 Testing retrieval after cleanup...")
    results = collection.query(
        query_texts=["chemical requirements cement"],
        n_results=3
    )
    
    print(f"Top 3 retrieved chunks:")
    for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0]), 1):
        print(f"\n  {i}. {meta.get('standard_number')} - {meta.get('clause')}")
        print(f"     Length: {len(doc)} chars")
        print(f"     Preview: {doc[:150]}...")

if __name__ == "__main__":
    cleanup_database()
