"""
Populate ChromaDB
Load processed chunks into ChromaDB vector database
"""

import sys
from pathlib import Path
import json
import yaml
from loguru import logger
from tqdm import tqdm

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from retrieval.chromadb_client import ChromaDBClient
from embeddings.embedding_service import EmbeddingService


def load_processed_chunks(data_dir: str = "../../data-pipeline/data/processed") -> list:
    """Load all processed chunks from data pipeline"""
    data_path = Path(data_dir)
    
    if not data_path.exists():
        logger.error(f"Data directory not found: {data_path}")
        return []
    
    all_chunks = []
    
    for chunk_file in data_path.glob("*_chunks.json"):
        logger.info(f"Loading: {chunk_file.name}")
        
        with open(chunk_file) as f:
            data = json.load(f)
            chunks = data.get('chunks', [])
            all_chunks.extend(chunks)
    
    logger.success(f"Loaded {len(all_chunks)} chunks from {len(list(data_path.glob('*_chunks.json')))} files")
    return all_chunks


def populate_chromadb(chunks: list, config: dict, reset: bool = False):
    """
    Populate ChromaDB with chunks
    
    Args:
        chunks: List of chunk dicts
        config: Configuration dict
        reset: If True, reset collection before populating
    """
    logger.info("Initializing services...")
    
    # Initialize services
    chromadb_client = ChromaDBClient(config)
    embedding_service = EmbeddingService(config)
    
    # Reset if requested
    if reset:
        logger.warning("Resetting ChromaDB collection...")
        chromadb_client.reset_collection()
    
    # Check if already populated
    stats = chromadb_client.get_collection_stats()
    if stats.get('total_chunks', 0) > 0:
        logger.warning(f"Collection already has {stats['total_chunks']} chunks")
        response = input("Continue and add more? (y/n): ")
        if response.lower() != 'y':
            logger.info("Aborted")
            return
    
    # Generate embeddings
    logger.info(f"Generating embeddings for {len(chunks)} chunks...")
    
    texts = [chunk['content'] for chunk in chunks]
    embeddings = embedding_service.encode_documents(texts, show_progress=True)
    
    logger.success(f"Generated {len(embeddings)} embeddings")
    
    # Add to ChromaDB in batches
    batch_size = 100
    for i in tqdm(range(0, len(chunks), batch_size), desc="Adding to ChromaDB"):
        batch_chunks = chunks[i:i+batch_size]
        batch_embeddings = embeddings[i:i+batch_size]
        
        chromadb_client.add_chunks(batch_chunks, batch_embeddings)
    
    # Final stats
    final_stats = chromadb_client.get_collection_stats()
    
    logger.success(f"""
ChromaDB Population Complete!

Statistics:
- Total chunks: {final_stats['total_chunks']}
- Unique standards: {final_stats['unique_standards']}
- Industries: {', '.join(final_stats['industries'])}
- Document types: {', '.join(final_stats['document_types'])}

Sample standards:
{chr(10).join(f'  - {std}' for std in final_stats['sample_standards'])}
""")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Populate ChromaDB with processed BIS documents")
    parser.add_argument('--reset', action='store_true', help='Reset collection before populating')
    parser.add_argument('--config', default='../config/rag_config.yaml', help='Config file path')
    parser.add_argument('--data-dir', default='../../data-pipeline/data/processed', help='Processed data directory')
    
    args = parser.parse_args()
    
    # Load config
    config_path = Path(args.config)
    if not config_path.exists():
        logger.error(f"Config file not found: {config_path}")
        return
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Load chunks
    chunks = load_processed_chunks(args.data_dir)
    
    if not chunks:
        logger.error("No chunks found to process")
        return
    
    # Populate
    populate_chromadb(chunks, config, reset=args.reset)


if __name__ == "__main__":
    main()
