#!/usr/bin/env python3
"""
Bulk load all CSV files from csv/ directory into ChromaDB
"""

import os
import sys
import glob
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from scripts.load_csv_to_chromadb import load_csv_dataset, prepare_documents
from retrieval.chromadb_client import ChromaDBClient
from embeddings.embedding_service import EmbeddingService

def main():
    csv_dir = Path(__file__).parent.parent / 'csv'
    chromadb_path = './data/chromadb'
    collection_name = 'bis_standards'
    batch_size = 100
    
    # Get all CSV files (skip the one we already loaded)
    csv_files = sorted(glob.glob(str(csv_dir / '*.csv')))
    
    # Skip ECG file (already loaded)
    csv_files = [f for f in csv_files if 'ECG' not in f]
    
    print(f"🚀 Bulk loading {len(csv_files)} CSV files into ChromaDB")
    print(f"📂 CSV Directory: {csv_dir}")
    print(f"💾 ChromaDB Path: {chromadb_path}")
    print(f"📦 Collection: {collection_name}")
    print("=" * 70)
    print()
    
    # Initialize services once
    print("🔧 Initializing ChromaDB and Embedding Service...")
    
    chroma_config = {
        'chromadb': {
            'persist_directory': chromadb_path,
            'collection_name': collection_name
        }
    }
    
    embed_config = {
        'embeddings': {
            'model': 'sentence-transformers/all-MiniLM-L6-v2',
            'device': 'cpu'
        }
    }
    
    chromadb_client = ChromaDBClient(chroma_config)
    embedding_service = EmbeddingService(embed_config)
    
    print("✅ Services initialized")
    print()
    
    # Process each file
    total_records = 0
    success_count = 0
    failed_files = []
    
    for idx, csv_file in enumerate(csv_files, 1):
        filename = os.path.basename(csv_file)
        print(f"[{idx}/{len(csv_files)}] 📄 Processing: {filename}")
        
        try:
            # Load CSV
            records = load_csv_dataset(csv_file)
            
            if not records:
                print(f"⚠️  No records found in {filename}, skipping")
                continue
            
            # Prepare documents
            texts, metadatas, ids = prepare_documents(records)
            
            if not texts:
                print(f"⚠️  No valid documents in {filename}, skipping")
                continue
            
            # Batch upload
            print(f"📤 Uploading {len(texts)} documents in batches of {batch_size}...")
            
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                batch_metadatas = metadatas[i:i + batch_size]
                batch_ids = ids[i:i + batch_size]
                
                # Generate embeddings
                embeddings = embedding_service.encode_documents(batch_texts, show_progress=False)
                
                # Add to ChromaDB
                chromadb_client.add_documents(
                    documents=batch_texts,
                    metadatas=batch_metadatas,
                    ids=batch_ids,
                    embeddings=embeddings
                )
            
            print(f"✅ Successfully loaded {len(texts)} records from {filename}")
            total_records += len(texts)
            success_count += 1
            
        except Exception as e:
            print(f"❌ Failed to load {filename}: {str(e)}")
            failed_files.append(filename)
        
        print()
        print("-" * 70)
        print()
    
    # Final statistics
    print("=" * 70)
    print("🎉 Bulk loading complete!")
    print()
    print("📊 Summary:")
    print(f"   Files processed: {len(csv_files)}")
    print(f"   Success: {success_count}")
    print(f"   Failed: {len(failed_files)}")
    print(f"   Total records added: {total_records}")
    print()
    
    if failed_files:
        print("⚠️  Failed files:")
        for f in failed_files:
            print(f"   - {f}")
        print()
    
    # Collection stats
    print("📊 Final Collection Statistics:")
    stats = chromadb_client.get_collection_stats()
    print(f"   Total chunks in DB: {stats.get('total_chunks', 0)}")
    if stats.get('industries'):
        print(f"   Industries: {len(stats['industries'])}")
        for ind in sorted(stats['industries']):
            print(f"      - {ind}")
    if stats.get('unique_standards'):
        print(f"   Unique standards: {stats['unique_standards']}")
    
    print()
    print("💡 Next steps:")
    print("   1. Start RAG service: uvicorn src.main:app --reload --port 8000")
    print("   2. Test queries: curl http://localhost:8000/stats")
    print()

if __name__ == "__main__":
    main()
