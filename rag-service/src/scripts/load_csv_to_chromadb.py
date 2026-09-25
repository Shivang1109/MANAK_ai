"""
Load BIS CSV dataset into ChromaDB

This script loads pre-processed BIS data (like cement standards) from CSV
directly into ChromaDB for immediate use by the RAG system.

Usage:
    python src/scripts/load_csv_to_chromadb.py --csv_path /path/to/dataset.csv
"""

import os
import sys
import csv
import argparse
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from retrieval.chromadb_client import ChromaDBClient
from embeddings.embedding_service import EmbeddingService


def load_csv_dataset(csv_path: str) -> List[Dict[str, Any]]:
    """
    Load BIS dataset from CSV file.
    
    Args:
        csv_path: Path to CSV file
        
    Returns:
        List of records with content and metadata
    """
    records = []
    
    print(f"📖 Reading CSV from: {csv_path}")
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Skip rows with empty content
            if not row.get('content', '').strip():
                continue
            
            records.append(row)
    
    print(f"✅ Loaded {len(records)} records from CSV")
    return records


def prepare_documents(records: List[Dict[str, Any]]) -> tuple[List[str], List[Dict[str, Any]], List[str]]:
    """
    Prepare documents for ChromaDB ingestion.
    
    Args:
        records: List of CSV records
        
    Returns:
        Tuple of (texts, metadatas, ids)
    """
    texts = []
    metadatas = []
    ids = []
    
    print("📝 Preparing documents for embedding...")
    
    for record in tqdm(records):
        # Main content to embed
        content = record.get('content', '').strip()
        
        if not content:
            continue
        
        # Create rich text for embedding (includes context)
        standard_num = record.get('standard_number', '')
        title = record.get('title', '')
        clause = record.get('clause', '')
        section = record.get('section', '')
        
        # Enhanced text for better retrieval
        rich_text = f"""
Standard: {standard_num}
Title: {title}
Section: {section}
Clause: {clause}

Content: {content}
        """.strip()
        
        texts.append(rich_text)
        
        # Metadata (stored with vector for filtering)
        metadata = {
            'document_id': record.get('document_id', ''),
            'standard_number': standard_num,
            'title': title,
            'revision': record.get('revision', ''),
            'section': section,
            'clause': clause,
            'document_type': record.get('document_type', 'Indian Standard'),
            'industry': record.get('industry', ''),
            'source_url': record.get('source_url', ''),
            'page': record.get('page', ''),
            'language': record.get('language', 'English'),
            'content': content,  # Store original content
            'lab_name': record.get('lab_name', ''),
            'osl_code': record.get('osl_code', ''),
            'testing_charge_inr': record.get('testing_charge_inr', ''),
            'validity_date': record.get('validity_date', ''),
            'remark': record.get('remark', '')
        }
        
        # Clean metadata (remove empty values)
        metadata = {k: v for k, v in metadata.items() if v}
        
        metadatas.append(metadata)
        
        # Unique ID
        record_id = record.get('record_id', f"RECORD_{len(ids):06d}")
        ids.append(record_id)
    
    print(f"✅ Prepared {len(texts)} documents")
    return texts, metadatas, ids


def main():
    parser = argparse.ArgumentParser(description='Load BIS CSV dataset into ChromaDB')
    parser.add_argument(
        '--csv_path',
        type=str,
        required=True,
        help='Path to CSV file'
    )
    parser.add_argument(
        '--batch_size',
        type=int,
        default=100,
        help='Batch size for processing (default: 100)'
    )
    parser.add_argument(
        '--collection_name',
        type=str,
        default='bis_standards',
        help='ChromaDB collection name (default: bis_standards)'
    )
    parser.add_argument(
        '--chromadb_path',
        type=str,
        default='./data/chromadb',
        help='ChromaDB persistence path'
    )
    
    args = parser.parse_args()
    
    # Validate CSV file exists
    if not os.path.exists(args.csv_path):
        print(f"❌ Error: CSV file not found: {args.csv_path}")
        sys.exit(1)
    
    print("🚀 Starting BIS CSV to ChromaDB ingestion")
    print(f"📂 CSV Path: {args.csv_path}")
    print(f"💾 ChromaDB Path: {args.chromadb_path}")
    print(f"📦 Collection: {args.collection_name}")
    print(f"⚙️  Batch Size: {args.batch_size}")
    print("-" * 60)
    
    # Step 1: Load CSV
    records = load_csv_dataset(args.csv_path)
    
    if not records:
        print("❌ No valid records found in CSV")
        sys.exit(1)
    
    # Step 2: Prepare documents
    texts, metadatas, ids = prepare_documents(records)
    
    if not texts:
        print("❌ No documents to ingest")
        sys.exit(1)
    
    # Step 3: Initialize services
    print("\n🔧 Initializing ChromaDB and Embedding Service...")
    
    # Create config for ChromaDB client
    chroma_config = {
        'chromadb': {
            'persist_directory': args.chromadb_path,
            'collection_name': args.collection_name
        }
    }
    
    chromadb_client = ChromaDBClient(chroma_config)
    
    # Create config for embedding service
    embed_config = {
        'embeddings': {
            'model': 'sentence-transformers/all-MiniLM-L6-v2',
            'device': 'cpu'
        }
    }
    
    embedding_service = EmbeddingService(embed_config)
    
    # Step 4: Batch processing
    print(f"\n📤 Uploading to ChromaDB in batches of {args.batch_size}...")
    
    total_batches = (len(texts) + args.batch_size - 1) // args.batch_size
    
    for i in tqdm(range(0, len(texts), args.batch_size), total=total_batches):
        batch_texts = texts[i:i + args.batch_size]
        batch_metadatas = metadatas[i:i + args.batch_size]
        batch_ids = ids[i:i + args.batch_size]
        
        # Generate embeddings
        embeddings = embedding_service.encode_documents(batch_texts, show_progress=False)
        
        # Add to ChromaDB
        chromadb_client.add_documents(
            documents=batch_texts,
            metadatas=batch_metadatas,
            ids=batch_ids,
            embeddings=embeddings
        )
    
    # Step 5: Verify
    print("\n✅ Ingestion complete!")
    print("\n📊 Collection Statistics:")
    stats = chromadb_client.get_collection_stats()
    print(f"  - Total chunks: {stats.get('total_chunks', 0)}")
    if stats.get('industries'):
        print(f"  - Industries: {', '.join(stats['industries'])}")
    if stats.get('unique_standards'):
        print(f"  - Unique standards: {stats['unique_standards']}")
    
    print("\n🎉 All done! Your ChromaDB is ready for queries.")
    print(f"\n💡 Collection: {args.collection_name}")
    print(f"   Path: {args.chromadb_path}")
    print(f"   Documents loaded: {len(texts)}")

if __name__ == "__main__":
    main()
