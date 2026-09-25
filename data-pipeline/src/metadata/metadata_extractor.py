"""
Metadata Extraction
Extract rich metadata from BIS documents for better retrieval
"""

import re
from typing import Dict, List, Optional
from loguru import logger


class MetadataExtractor:
    """Extract structured metadata from BIS documents"""
    
    def __init__(self, config: Dict):
        self.config = config.get('metadata', {})
        self.standard_patterns = self.config.get('standard_patterns', [])
        
    def extract_document_metadata(self, text: str, existing_metadata: Dict = None) -> Dict:
        """
        Extract document-level metadata from text
        
        Args:
            text: Full document text
            existing_metadata: Pre-existing metadata to enhance
            
        Returns:
            Enhanced metadata dict
        """
        metadata = existing_metadata.copy() if existing_metadata else {}
        
        # Extract standard number if not provided
        if not metadata.get('standard_number') and self.config.get('extract_standard_number'):
            standard_number = self._extract_standard_number(text)
            if standard_number:
                metadata['standard_number'] = standard_number
        
        # Extract revision year
        if not metadata.get('revision') and self.config.get('extract_revision_year'):
            revision = self._extract_revision_year(text, metadata.get('standard_number'))
            if revision:
                metadata['revision'] = revision
        
        # Extract title
        if not metadata.get('title'):
            title = self._extract_title(text)
            if title:
                metadata['title'] = title
        
        # Extract industry/category
        if not metadata.get('industry') and self.config.get('extract_industry'):
            industry = self._infer_industry(text, metadata.get('title', ''))
            if industry:
                metadata['industry'] = industry
        
        # Document type
        if not metadata.get('document_type') and self.config.get('extract_document_type'):
            doc_type = self._infer_document_type(text, metadata)
            if doc_type:
                metadata['document_type'] = doc_type
        
        return metadata
    
    def _extract_standard_number(self, text: str) -> Optional[str]:
        """Extract IS standard number"""
        # Look in first 500 characters (usually in header)
        header = text[:500]
        
        for pattern in self.standard_patterns:
            match = re.search(pattern, header, re.IGNORECASE)
            if match:
                return match.group().strip()
        
        return None
    
    def _extract_revision_year(self, text: str, standard_number: str = None) -> Optional[str]:
        """Extract revision year from standard number or text"""
        if standard_number:
            # Extract year from IS 12345:2025 format
            year_match = re.search(r':?\s*(\d{4})', standard_number)
            if year_match:
                return year_match.group(1)
        
        # Look for year in header
        header = text[:500]
        year_match = re.search(r'\b(20\d{2})\b', header)
        if year_match:
            return year_match.group(1)
        
        return None
    
    def _extract_title(self, text: str) -> Optional[str]:
        """Extract document title"""
        lines = text[:1000].split('\n')
        
        # Look for title-like patterns
        for line in lines[1:10]:  # Skip first line (might be standard number)
            line = line.strip()
            
            # Title is usually in title case, longer than 10 chars, not a clause number
            if (len(line) > 10 and 
                not re.match(r'^\d+\.', line) and
                not line.startswith('IS ') and
                line[0].isupper()):
                
                # Clean up
                title = re.sub(r'\s+', ' ', line)
                return title
        
        return None
    
    def _infer_industry(self, text: str, title: str) -> Optional[str]:
        """Infer industry category from content"""
        text_lower = (text[:2000] + title).lower()
        
        # Industry keywords
        industry_keywords = {
            'electronics': ['led', 'electronic', 'circuit', 'voltage', 'power supply', 'electrical'],
            'food_packaging': ['food', 'packaging', 'container', 'beverage', 'bottle', 'wrapper'],
            'construction': ['cement', 'concrete', 'steel', 'construction', 'building', 'structural'],
            'textile': ['fabric', 'textile', 'garment', 'cloth', 'fiber'],
            'chemical': ['chemical', 'reagent', 'compound', 'solution', 'acid', 'alkali'],
            'mechanical': ['mechanical', 'machine', 'equipment', 'tool', 'bearing'],
            'automotive': ['vehicle', 'automotive', 'automobile', 'engine', 'transmission']
        }
        
        # Count matches
        industry_scores = {}
        for industry, keywords in industry_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                industry_scores[industry] = score
        
        if industry_scores:
            return max(industry_scores, key=industry_scores.get)
        
        return 'general'
    
    def _infer_document_type(self, text: str, metadata: Dict) -> str:
        """Infer document type"""
        text_lower = text[:1000].lower()
        
        if 'indian standard' in text_lower or metadata.get('standard_number', '').startswith('IS'):
            return 'indian_standard'
        elif 'guideline' in text_lower or 'guidance' in text_lower:
            return 'certification_guideline'
        elif 'manual' in text_lower:
            return 'product_manual'
        elif 'qco' in text_lower or 'quality control' in text_lower:
            return 'qco_information'
        elif 'scheme' in text_lower and 'certification' in text_lower:
            return 'scheme_document'
        else:
            return 'official_guidance'


class ClauseExtractor:
    """Extract clause structure from documents"""
    
    def __init__(self):
        self.clause_pattern = re.compile(r'^(\d+(?:\.\d+)*)\s+(.+)$', re.MULTILINE)
        
    def extract_clauses(self, text: str) -> List[Dict]:
        """Extract all clauses from text"""
        clauses = []
        
        for match in self.clause_pattern.finditer(text):
            clause_number = match.group(1)
            clause_title = match.group(2).strip()
            
            clauses.append({
                'number': clause_number,
                'title': clause_title,
                'position': match.start(),
                'level': len(clause_number.split('.'))
            })
        
        return clauses


if __name__ == "__main__":
    # Example usage
    import yaml
    
    with open("config/pipeline_config.yaml") as f:
        config = yaml.safe_load(f)
    
    extractor = MetadataExtractor(config)
    
    sample_text = """
    IS 12345:2025
    
    LED Lamps - Specification
    
    Indian Standard
    
    1. Scope
    This standard specifies requirements for LED lamps intended for general lighting.
    
    2. References
    IS 10322 Luminaires for general lighting
    
    3. Terminology
    3.1 LED
    Light Emitting Diode - a semiconductor device that emits light.
    """
    
    metadata = extractor.extract_document_metadata(sample_text)
    
    print("Extracted Metadata:")
    print(f"Standard Number: {metadata.get('standard_number')}")
    print(f"Revision: {metadata.get('revision')}")
    print(f"Title: {metadata.get('title')}")
    print(f"Industry: {metadata.get('industry')}")
    print(f"Document Type: {metadata.get('document_type')}")
