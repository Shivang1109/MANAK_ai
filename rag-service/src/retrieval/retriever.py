"""
Retrieval Engine
Handles query processing, retrieval, and re-ranking
"""

from typing import List, Dict, Optional
from loguru import logger
import re


class QueryProcessor:
    """Process and enhance queries before retrieval"""
    
    def __init__(self, config: Dict):
        self.config = config
    
    def process(self, query: str) -> Dict:
        """
        Process a user query
        
        Returns:
            Dict with processed_query, detected_entities, etc.
        """
        # Clean query
        processed_query = query.strip()
        
        # Detect standard numbers
        standard_numbers = self._extract_standard_numbers(query)
        
        # Detect product mentions
        products = self._extract_products(query)
        
        # Detect intent
        intent = self._detect_intent(query)
        
        return {
            'original_query': query,
            'processed_query': processed_query,
            'standard_numbers': standard_numbers,
            'products': products,
            'intent': intent
        }
    
    def _extract_standard_numbers(self, query: str) -> List[str]:
        """Extract IS standard numbers from query"""
        patterns = [
            r'IS\s+\d+(?:\s*:\s*\d{4})?',
            r'IS\s+\d+\s*\(Part\s+\d+\)'
        ]
        
        standards = []
        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            standards.extend(matches)
        
        return list(set(standards))
    
    def _extract_products(self, query: str) -> List[str]:
        """Extract product mentions"""
        # Simple keyword extraction - can be enhanced with NER
        product_keywords = ['led', 'bulb', 'lamp', 'cement', 'steel', 'food', 'water']
        
        query_lower = query.lower()
        detected = [kw for kw in product_keywords if kw in query_lower]
        
        return detected
    
    def _detect_intent(self, query: str) -> str:
        """Detect user intent"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['how to', 'apply', 'get', 'obtain', 'process']):
            if 'certif' in query_lower:
                return 'certification_process'
        
        if any(word in query_lower for word in ['which standard', 'what standard', 'applicable standard']):
            return 'find_standard'
        
        if any(word in query_lower for word in ['requirement', 'must', 'shall', 'need to']):
            return 'requirements'
        
        if any(word in query_lower for word in ['mandatory', 'compulsory', 'required by law']):
            return 'compliance_check'
        
        return 'general_question'


class HybridRetriever:
    """Retrieves relevant chunks using vector similarity and metadata filtering"""
    
    def __init__(self, chromadb_client, embedding_service, config: Dict):
        self.chromadb = chromadb_client
        self.embedder = embedding_service
        self.config = config.get('retrieval', {})
        
        self.top_k = self.config.get('top_k', 10)
        self.min_similarity = self.config.get('min_similarity', 0.5)
    
    def retrieve(self, query_info: Dict, metadata_filter: Optional[Dict] = None) -> List[Dict]:
        """
        Retrieve relevant chunks
        
        Args:
            query_info: Processed query information
            metadata_filter: Optional metadata filters
            
        Returns:
            List of retrieved chunks with scores
        """
        query = query_info['processed_query']
        
        logger.info(f"Retrieving for query: {query}")
        
        # Generate query embedding
        query_embedding = self.embedder.encode_query(query)
        
        # Build metadata filter if provided
        enhanced_filter = metadata_filter.copy() if metadata_filter else None
        
        # Known indexed standards in ChromaDB
        known_standards = [
            'IS 10146:2023', 'IS 10500:2012', 'IS 1166:2024', 'IS 12640:Part 1:2024',
            'IS 1293:2019', 'IS 13450 : Part 2 : Sec 25 (2018)', 'IS 1346:2023',
            'IS 16102 (Part 2):2023', 'IS 16102 : Part 1 (2026)', 'IS 16102 : Part 2 (2017)',
            'IS 16103 : Part 1 (2025)', 'IS 16103 : Part 2 (2012)', 'IS 16106 (2012)',
            'IS 16107 : Part 2 : Sec 1 (2012)', 'IS 1786:2008', 'IS 2185 : Part 1 (2005)',
            'IS 269:2015', 'IS 3025 (Part 34/Sec 1):2023', 'IS 3025 (Part 43/Sec 1):2022',
            'IS 3854:2022', 'IS 456:2000', 'IS 5401 (Part 2):2012', 'IS 694:2010',
            'IS 7079:2008', 'IS 14543 (2024)'
        ]

        # Check if user mentioned a specific standard number
        # Extract the standard code directly following "IS" (e.g., "IS 10500:2012" -> "10500", "IS 1293" -> "1293")
        query_codes = set(re.findall(r'IS\s*(\d{3,5})', query, re.IGNORECASE))

        targeted_chunks = []
        if query_codes and not enhanced_filter:
            matched_stds = [
                k for k in known_standards
                if any(f"IS {code}" in k or f"IS{code}" in k or k.startswith(f"IS {code}") for code in query_codes)
            ]
            if matched_stds:
                logger.info(f"Targeting specific BIS standard(s): {matched_stds}")
                std_filter = {'standard_number': matched_stds[0]} if len(matched_stds) == 1 else {'standard_number': {'$in': matched_stds}}
                try:
                    target_res = self.chromadb.query(
                        query_embedding=query_embedding,
                        n_results=min(15, self.top_k),
                        metadata_filter=std_filter
                    )
                    if target_res and target_res.get('documents'):
                        for i in range(len(target_res['documents'])):
                            dist = target_res['distances'][i]
                            sim = 1 - dist
                            targeted_chunks.append({
                                'chunk_id': target_res['ids'][i],
                                'content': target_res['documents'][i],
                                'metadata': target_res['metadatas'][i],
                                'similarity_score': max(sim, 0.55),
                                'distance': dist
                            })
                except Exception as e:
                    logger.warning(f"Targeted standard query failed: {e}")

        # General Query ChromaDB
        results = self.chromadb.query(
            query_embedding=query_embedding,
            n_results=self.top_k,
            metadata_filter=enhanced_filter
        )
        
        # Fallback to unfiltered query if filtered query returned no documents
        if (not results or not results.get('documents') or len(results['documents']) == 0) and enhanced_filter:
            logger.info("Filtered query returned 0 documents, falling back to semantic search without filter")
            results = self.chromadb.query(
                query_embedding=query_embedding,
                n_results=self.top_k,
                metadata_filter=None
            )
        
        # Convert to structured format
        retrieved_chunks = list(targeted_chunks)
        seen_ids = set(c['chunk_id'] for c in targeted_chunks)

        if results and results.get('documents'):
            for i in range(len(results['documents'])):
                chunk_id = results['ids'][i]
                if chunk_id in seen_ids:
                    continue
                seen_ids.add(chunk_id)

                distance = results['distances'][i]
                similarity = 1 - distance
                
                # Filter by minimum similarity
                if similarity < 0.35:
                    continue
                
                chunk = {
                    'chunk_id': chunk_id,
                    'content': results['documents'][i],
                    'metadata': results['metadatas'][i],
                    'similarity_score': similarity,
                    'distance': distance
                }
                
                retrieved_chunks.append(chunk)
        
        logger.success(f"Retrieved {len(retrieved_chunks)} chunks (above threshold)")
        
        return retrieved_chunks


class ReRanker:
    """Re-rank retrieved chunks for better relevance"""
    
    def __init__(self, config: Dict):
        self.config = config.get('reranking', {})
        self.enabled = self.config.get('enabled', True)
        self.final_k = config.get('retrieval', {}).get('final_k', 5)
    
    def rerank(self, query: str, chunks: List[Dict]) -> List[Dict]:
        """
        Re-rank retrieved chunks
        
        For MVP, uses simple heuristics. Can be enhanced with cross-encoder models.
        """
        if not self.enabled or len(chunks) <= self.final_k:
            return chunks[:self.final_k]
        
        logger.info(f"Re-ranking {len(chunks)} chunks...")
        
        # Score each chunk
        for chunk in chunks:
            chunk['rerank_score'] = self._calculate_score(query, chunk)
        
        # Sort by rerank score
        reranked = sorted(chunks, key=lambda x: x['rerank_score'], reverse=True)
        
        # Return top K
        return reranked[:self.final_k]
    
    def _calculate_score(self, query: str, chunk: Dict) -> float:
        """
        Calculate re-ranking score
        
        Combines:
        - Original similarity score
        - Metadata relevance
        - Content features
        """
        score = float(chunk.get('similarity_score', 0.5))

        # Boost if standard number matches the query
        chunk_std = str(chunk['metadata'].get('standard_number', ''))
        query_is_matches = re.findall(r'IS\s*(\d+)', query, re.IGNORECASE)
        for std_num in query_is_matches:
            if std_num in chunk_std:
                score += 3.0  # Massive boost for matching the requested IS standard
            else:
                score -= 0.5  # Penalize chunks from competing standards when a specific IS is requested

        # Boost if query terms appear in content
        query_terms = set(re.findall(r'\w+', query.lower()))
        content_terms = set(re.findall(r'\w+', chunk['content'].lower()))
        overlap = len(query_terms & content_terms)
        score += overlap * 0.05
        
        # Boost recent standards
        revision = chunk['metadata'].get('revision', '')
        if revision and revision.isdigit():
            year = int(revision)
            if year >= 2020:
                score += 0.1
        
        # Boost if clause is specified (more specific)
        if chunk['metadata'].get('clause'):
            score += 0.05
        
        return score


if __name__ == "__main__":
    # Example usage
    import yaml
    from embeddings.embedding_service import EmbeddingService
    from retrieval.chromadb_client import ChromaDBClient
    
    with open("config/rag_config.yaml") as f:
        config = yaml.safe_load(f)
    
    # Initialize components
    processor = QueryProcessor(config)
    chromadb = ChromaDBClient(config)
    embedder = EmbeddingService(config)
    retriever = HybridRetriever(chromadb, embedder, config)
    reranker = ReRanker(config)
    
    # Test query
    query = "What are the voltage requirements for LED bulbs in IS 12345?"
    
    # Process query
    query_info = processor.process(query)
    print("\nQuery Info:")
    print(f"Intent: {query_info['intent']}")
    print(f"Standards: {query_info['standard_numbers']}")
    print(f"Products: {query_info['products']}")
    
    # Retrieve (if ChromaDB has data)
    try:
        chunks = retriever.retrieve(query_info)
        print(f"\nRetrieved {len(chunks)} chunks")
        
        # Re-rank
        reranked = reranker.rerank(query, chunks)
        print(f"Top {len(reranked)} after re-ranking")
    except Exception as e:
        print(f"\nRetrieval test skipped (no data in ChromaDB): {e}")
