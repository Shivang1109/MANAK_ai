"""
ChromaDB Client
Manages vector database operations for BIS knowledge base
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
from loguru import logger
from pathlib import Path
import json


class ChromaDBClient:
    """ChromaDB vector database client"""
    
    def __init__(self, config: Dict):
        self.config = config.get('chromadb', {})
        
        persist_dir = Path(self.config.get('persist_directory', '../chromadb_data'))
        persist_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(persist_dir),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        self.collection_name = self.config.get('collection_name', 'bis_standards')
        self.collection = None
        
    def get_or_create_collection(self):
        """Get or create the BIS standards collection"""
        if self.collection is None:
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={
                    "description": "BIS Standards Knowledge Base",
                    "hnsw:space": self.config.get('distance_metric', 'cosine')
                }
            )
            logger.info(f"Collection '{self.collection_name}' ready with {self.collection.count()} documents")
        
        return self.collection
    
    def add_chunks(self, chunks: List[Dict], embeddings: List[List[float]]):
        """
        Add document chunks to ChromaDB
        
        Args:
            chunks: List of chunk dicts with 'content' and 'metadata'
            embeddings: List of embedding vectors
        """
        collection = self.get_or_create_collection()
        
        # Prepare data for ChromaDB
        ids = []
        documents = []
        metadatas = []
        embeddings_list = []
        
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            # Generate unique ID
            doc_id = chunk['metadata'].get('document_id', 'unknown')
            chunk_id = f"{doc_id}_chunk_{i}"
            
            ids.append(chunk_id)
            documents.append(chunk['content'])
            metadatas.append(chunk['metadata'])
            embeddings_list.append(embedding)
        
        # Add to collection
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings_list
        )
        
        logger.success(f"Added {len(chunks)} chunks to ChromaDB")
        
    def query(self, 
             query_embedding: List[float],
             n_results: int = 10,
             metadata_filter: Optional[Dict] = None) -> Dict:
        """
        Query the vector database
        
        Args:
            query_embedding: Query embedding vector
            n_results: Number of results to return
            metadata_filter: Optional metadata filters
            
        Returns:
            Query results with documents, metadatas, and distances
        """
        collection = self.get_or_create_collection()
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=metadata_filter,
            include=['documents', 'metadatas', 'distances']
        )
        
        return {
            'ids': results['ids'][0],
            'documents': results['documents'][0],
            'metadatas': results['metadatas'][0],
            'distances': results['distances'][0]
        }
    
    def get_collection_stats(self) -> Dict:
        """Get collection statistics"""
        collection = self.get_or_create_collection()
        
        count = collection.count()
        
        # Sample to get industries and document types
        if count > 0:
            sample = collection.get(limit=min(100, count), include=['metadatas'])
            
            industries = set()
            doc_types = set()
            standards = set()
            
            for metadata in sample['metadatas']:
                if metadata.get('industry'):
                    industries.add(metadata['industry'])
                if metadata.get('document_type'):
                    doc_types.add(metadata['document_type'])
                if metadata.get('standard_number'):
                    standards.add(metadata['standard_number'])
            
            return {
                'total_chunks': count,
                'unique_standards': len(standards),
                'industries': sorted(industries),
                'document_types': sorted(doc_types),
                'sample_standards': sorted(standards)[:5]
            }
        
        return {'total_chunks': 0}
    
    def reset_collection(self):
        """Reset (delete and recreate) the collection"""
        try:
            self.client.delete_collection(self.collection_name)
            logger.warning(f"Deleted collection: {self.collection_name}")
        except Exception as e:
            logger.info(f"Collection did not exist: {e}")
        
        self.collection = None
        self.get_or_create_collection()
        logger.info(f"Created fresh collection: {self.collection_name}")
    
    def add_documents(self, documents: List[str], metadatas: List[Dict], 
                      ids: List[str], embeddings: List[List[float]]):
        """
        Add documents directly to ChromaDB
        
        Args:
            documents: List of document texts
            metadatas: List of metadata dicts
            ids: List of document IDs
            embeddings: List of embedding vectors
        """
        collection = self.get_or_create_collection()
        
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )
        
        logger.success(f"Added {len(documents)} documents to ChromaDB")


if __name__ == "__main__":
    # Example usage
    import yaml
    
    with open("config/rag_config.yaml") as f:
        config = yaml.safe_load(f)
    
    client = ChromaDBClient(config)
    
    # Get stats
    stats = client.get_collection_stats()
    print("\nChromaDB Collection Stats:")
    print(json.dumps(stats, indent=2))
