"""
Embedding Service
Generate embeddings for queries and documents
"""

from sentence_transformers import SentenceTransformer
from typing import List, Union, Dict
from loguru import logger
import torch


class EmbeddingService:
    """Service for generating text embeddings"""
    
    def __init__(self, config: Dict):
        self.config = config.get('embeddings', {})
        
        model_name = self.config.get('model', 'sentence-transformers/all-MiniLM-L6-v2')
        device = self.config.get('device', 'cpu')
        
        logger.info(f"Loading embedding model: {model_name}")
        
        self.model = SentenceTransformer(model_name)
        self.model.to(device)
        
        self.batch_size = self.config.get('batch_size', 32)
        self.normalize = self.config.get('normalize', True)
        
        logger.success(f"Embedding model loaded on {device}")
    
    def encode(self, texts: Union[str, List[str]], show_progress: bool = False) -> Union[List[float], List[List[float]]]:
        """
        Generate embeddings for text(s)
        
        Args:
            texts: Single text string or list of texts
            show_progress: Show progress bar for batch processing
            
        Returns:
            Embedding vector(s)
        """
        is_single = isinstance(texts, str)
        
        if is_single:
            texts = [texts]
        
        # Generate embeddings
        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=show_progress,
            normalize_embeddings=self.normalize,
            convert_to_numpy=True
        )
        
        # Convert to list
        embeddings = embeddings.tolist()
        
        if is_single:
            return embeddings[0]
        
        return embeddings
    
    def encode_query(self, query: str) -> List[float]:
        """
        Encode a search query
        Convenience method that may add query-specific processing in future
        """
        return self.encode(query)
    
    def encode_documents(self, documents: List[str], show_progress: bool = True) -> List[List[float]]:
        """
        Encode multiple documents
        Convenience method for batch document processing
        """
        logger.info(f"Encoding {len(documents)} documents...")
        embeddings = self.encode(documents, show_progress=show_progress)
        logger.success(f"Encoded {len(embeddings)} document embeddings")
        return embeddings


if __name__ == "__main__":
    # Example usage
    import yaml
    
    with open("config/rag_config.yaml") as f:
        config = yaml.safe_load(f)
    
    service = EmbeddingService(config)
    
    # Test query encoding
    query = "What are the requirements for LED bulbs?"
    query_embedding = service.encode_query(query)
    print(f"\nQuery embedding dimension: {len(query_embedding)}")
    print(f"First 5 values: {query_embedding[:5]}")
    
    # Test document encoding
    documents = [
        "LED lamps shall comply with voltage requirements.",
        "The power consumption shall not exceed rated value.",
        "Testing shall be conducted as per IS 10322."
    ]
    doc_embeddings = service.encode_documents(documents, show_progress=False)
    print(f"\nEncoded {len(doc_embeddings)} documents")
