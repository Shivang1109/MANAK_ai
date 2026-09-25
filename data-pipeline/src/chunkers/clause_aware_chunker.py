"""
Clause-Aware Chunking
Splits BIS standards into semantically meaningful chunks while respecting clause boundaries
"""

import re
from typing import List, Dict, Tuple
from loguru import logger


class ClauseAwareChunker:
    """Chunk text while respecting document structure (clauses, sections)"""
    
    def __init__(self, config: Dict):
        self.config = config.get('chunking', {})
        self.max_chunk_size = self.config.get('max_chunk_size', 1000)
        self.overlap_size = self.config.get('overlap_size', 200)
        self.clause_patterns = self.config.get('clause_patterns', [])
        
    def chunk_document(self, pages: List[Dict], document_metadata: Dict) -> List[Dict]:
        """
        Chunk a document into semantically meaningful pieces
        
        Args:
            pages: List of page dicts with 'text' and 'page_number'
            document_metadata: Document-level metadata
            
        Returns:
            List of chunk dicts with text and metadata
        """
        logger.info(f"Chunking document: {document_metadata.get('standard_number')}")
        
        # Combine all pages
        full_text = ""
        page_boundaries = [0]  # Track where each page starts
        
        for page in pages:
            page_text = page.get('cleaned_text') or page.get('text', '')
            full_text += page_text + "\n\n"
            page_boundaries.append(len(full_text))
        
        # Detect structural elements
        structures = self._detect_structure(full_text)
        
        # Create chunks
        chunks = []
        
        if structures:
            # Chunk by detected structure
            chunks = self._chunk_by_structure(full_text, structures, page_boundaries, document_metadata)
        else:
            # Fallback to semantic chunking
            chunks = self._chunk_by_size(full_text, page_boundaries, document_metadata)
        
        logger.success(f"Created {len(chunks)} chunks")
        return chunks
    
    def _detect_structure(self, text: str) -> List[Dict]:
        """Detect clauses, sections, and other structural elements"""
        structures = []
        
        for pattern in self.clause_patterns:
            for match in re.finditer(pattern, text, re.MULTILINE):
                structures.append({
                    'type': 'clause',
                    'position': match.start(),
                    'identifier': match.group(),
                    'text': match.group()
                })
        
        # Sort by position
        structures.sort(key=lambda x: x['position'])
        return structures
    
    def _chunk_by_structure(self, text: str, structures: List[Dict], 
                           page_boundaries: List[int], document_metadata: Dict) -> List[Dict]:
        """Create chunks based on detected structure"""
        chunks = []
        
        for i, structure in enumerate(structures):
            start_pos = structure['position']
            
            # Find end position (start of next structure or end of text)
            if i < len(structures) - 1:
                end_pos = structures[i + 1]['position']
            else:
                end_pos = len(text)
            
            # Extract chunk text
            chunk_text = text[start_pos:end_pos].strip()
            
            # Skip if too small
            if len(chunk_text) < 50:
                continue
            
            # Split if too large
            if len(chunk_text) > self.max_chunk_size * 1.5:
                sub_chunks = self._split_large_chunk(chunk_text, start_pos, page_boundaries, document_metadata, structure)
                chunks.extend(sub_chunks)
            else:
                chunk = self._create_chunk(
                    chunk_text, 
                    start_pos, 
                    page_boundaries, 
                    document_metadata,
                    structure
                )
                chunks.append(chunk)
        
        return chunks
    
    def _chunk_by_size(self, text: str, page_boundaries: List[int], 
                      document_metadata: Dict) -> List[Dict]:
        """Fallback: chunk by size with overlap"""
        chunks = []
        position = 0
        chunk_index = 0
        
        while position < len(text):
            # Find good break point (sentence end)
            end_pos = min(position + self.max_chunk_size, len(text))
            
            if end_pos < len(text):
                # Look for sentence end
                sentence_end = text.rfind('.', position, end_pos)
                if sentence_end > position + self.max_chunk_size * 0.5:
                    end_pos = sentence_end + 1
            
            chunk_text = text[position:end_pos].strip()
            
            if len(chunk_text) > 50:  # Minimum chunk size
                chunk = self._create_chunk(
                    chunk_text,
                    position,
                    page_boundaries,
                    document_metadata,
                    {'type': 'semantic', 'identifier': f'chunk_{chunk_index}'}
                )
                chunks.append(chunk)
                chunk_index += 1
            
            # Move position with overlap
            position = end_pos - self.overlap_size
            if position >= len(text):
                break
        
        return chunks
    
    def _split_large_chunk(self, text: str, start_pos: int, page_boundaries: List[int],
                          document_metadata: Dict, structure: Dict) -> List[Dict]:
        """Split a large chunk into smaller pieces"""
        chunks = []
        position = 0
        sub_index = 0
        
        while position < len(text):
            end_pos = min(position + self.max_chunk_size, len(text))
            
            # Find sentence boundary
            if end_pos < len(text):
                sentence_end = text.rfind('.', position, end_pos)
                if sentence_end > position:
                    end_pos = sentence_end + 1
            
            chunk_text = text[position:end_pos].strip()
            
            if len(chunk_text) > 50:
                sub_structure = structure.copy()
                sub_structure['identifier'] = f"{structure['identifier']}.{sub_index}"
                
                chunk = self._create_chunk(
                    chunk_text,
                    start_pos + position,
                    page_boundaries,
                    document_metadata,
                    sub_structure
                )
                chunks.append(chunk)
                sub_index += 1
            
            position = end_pos
        
        return chunks
    
    def _create_chunk(self, text: str, position: int, page_boundaries: List[int],
                     document_metadata: Dict, structure: Dict = None) -> Dict:
        """Create a chunk with metadata"""
        
        # Determine which page this chunk is on
        page_number = 1
        for i, boundary in enumerate(page_boundaries[1:], 1):
            if position < boundary:
                page_number = i
                break
        
        chunk = {
            'content': text,
            'metadata': {
                'document_id': document_metadata.get('document_id'),
                'standard_number': document_metadata.get('standard_number'),
                'title': document_metadata.get('title'),
                'revision': document_metadata.get('revision'),
                'document_type': document_metadata.get('document_type'),
                'industry': document_metadata.get('industry'),
                'source_url': document_metadata.get('source_url', ''),
                'page': page_number,
                'section': structure.get('identifier', '') if structure else '',
                'clause': structure.get('identifier', '') if structure and structure.get('type') == 'clause' else '',
                'language': 'English',
                'char_count': len(text),
                'chunk_type': structure.get('type', 'semantic') if structure else 'semantic'
            }
        }
        
        return chunk


if __name__ == "__main__":
    # Example usage
    import yaml
    
    with open("config/pipeline_config.yaml") as f:
        config = yaml.safe_load(f)
    
    chunker = ClauseAwareChunker(config)
    
    # Example document
    sample_pages = [
        {
            'page_number': 1,
            'text': """
            IS 12345:2025
            LED Lamps - Specification
            
            1. Scope
            This standard covers LED lamps for general lighting purposes.
            
            2. References
            IS 10322 Luminaires for general lighting.
            
            3. Terminology
            3.1 LED: Light Emitting Diode
            3.2 Luminous Flux: The quantity of light emitted
            
            4. Requirements
            4.1 General
            LED lamps shall comply with the requirements specified.
            
            4.2 Electrical Requirements
            4.2.1 Voltage: The rated voltage shall be specified.
            4.2.2 Power Consumption: Not exceeding rated value.
            """
        }
    ]
    
    doc_metadata = {
        'document_id': 'IS_12345_2025',
        'standard_number': 'IS 12345:2025',
        'title': 'LED Lamps - Specification',
        'revision': '2025',
        'document_type': 'indian_standard',
        'industry': 'electronics'
    }
    
    chunks = chunker.chunk_document(sample_pages, doc_metadata)
    
    print(f"\nCreated {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"\n--- Chunk {i} ---")
        print(f"Clause: {chunk['metadata']['clause']}")
        print(f"Page: {chunk['metadata']['page']}")
        print(f"Length: {chunk['metadata']['char_count']} chars")
        print(f"Content preview: {chunk['content'][:100]}...")
