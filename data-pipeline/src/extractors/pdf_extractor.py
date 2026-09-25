"""
PDF Text Extraction
Handles both digital and scanned PDFs using PyMuPDF and Tesseract OCR
"""

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from loguru import logger
import io
import re


class PDFExtractor:
    """Extract text from PDF documents"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.ocr_enabled = config.get('extraction', {}).get('ocr_enabled', True)
        self.ocr_language = config.get('extraction', {}).get('ocr_language', 'eng')
        
    def extract(self, pdf_path: Path) -> Dict:
        """
        Extract text and metadata from PDF
        
        Returns:
            Dict with pages, metadata, and extraction info
        """
        logger.info(f"Extracting: {pdf_path}")
        
        try:
            doc = fitz.open(pdf_path)
            
            extraction_result = {
                "file_path": str(pdf_path),
                "total_pages": len(doc),
                "metadata": self._extract_metadata(doc),
                "pages": [],
                "extraction_method": []
            }
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Try digital text extraction first
                text = page.get_text()
                method = "digital"
                
                # If text is sparse, use OCR
                if self.ocr_enabled and self._is_text_sparse(text):
                    logger.info(f"Page {page_num + 1}: Using OCR")
                    text = self._extract_with_ocr(page)
                    method = "ocr"
                
                extraction_result["pages"].append({
                    "page_number": page_num + 1,
                    "text": text,
                    "char_count": len(text),
                    "extraction_method": method
                })
                
                extraction_result["extraction_method"].append(method)
            
            doc.close()
            
            # Summary
            digital_pages = extraction_result["extraction_method"].count("digital")
            ocr_pages = extraction_result["extraction_method"].count("ocr")
            
            logger.success(
                f"Extracted {extraction_result['total_pages']} pages "
                f"({digital_pages} digital, {ocr_pages} OCR)"
            )
            
            return extraction_result
            
        except Exception as e:
            logger.error(f"Extraction failed for {pdf_path}: {e}")
            raise
    
    def _extract_metadata(self, doc: fitz.Document) -> Dict:
        """Extract PDF metadata"""
        metadata = doc.metadata or {}
        return {
            "title": metadata.get("title", ""),
            "author": metadata.get("author", ""),
            "subject": metadata.get("subject", ""),
            "creator": metadata.get("creator", ""),
            "producer": metadata.get("producer", ""),
            "creation_date": metadata.get("creationDate", ""),
            "modification_date": metadata.get("modDate", "")
        }
    
    def _is_text_sparse(self, text: str, threshold: int = 100) -> bool:
        """Check if extracted text is too sparse (likely scanned)"""
        return len(text.strip()) < threshold
    
    def _extract_with_ocr(self, page: fitz.Page) -> str:
        """Extract text using OCR"""
        try:
            # Render page to image
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x resolution
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            
            # Run OCR
            text = pytesseract.image_to_string(img, lang=self.ocr_language)
            
            return text
            
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return ""


class DocumentCleaner:
    """Clean and normalize extracted text"""
    
    def __init__(self, config: Dict):
        self.config = config.get('cleaning', {})
        
    def clean(self, text: str) -> str:
        """Clean extracted text"""
        
        if self.config.get('normalize_whitespace', True):
            text = self._normalize_whitespace(text)
        
        if self.config.get('fix_hyphenation', True):
            text = self._fix_hyphenation(text)
        
        if self.config.get('merge_broken_lines', True):
            text = self._merge_broken_lines(text)
        
        return text
    
    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace"""
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        # Replace multiple newlines with double newline
        text = re.sub(r'\n\n+', '\n\n', text)
        return text.strip()
    
    def _fix_hyphenation(self, text: str) -> str:
        """Fix broken words at line ends"""
        # Remove hyphens at line breaks
        text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
        return text
    
    def _merge_broken_lines(self, text: str) -> str:
        """Merge lines that were incorrectly broken"""
        # Merge lines that don't end with sentence-ending punctuation
        lines = text.split('\n')
        merged_lines = []
        current_line = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_line:
                    merged_lines.append(current_line)
                    current_line = ""
                continue
            
            if current_line:
                # Check if previous line ends with sentence-ending punctuation
                if current_line[-1] in '.!?:':
                    merged_lines.append(current_line)
                    current_line = line
                else:
                    current_line += " " + line
            else:
                current_line = line
        
        if current_line:
            merged_lines.append(current_line)
        
        return '\n\n'.join(merged_lines)


if __name__ == "__main__":
    # Example usage
    import yaml
    
    with open("config/pipeline_config.yaml") as f:
        config = yaml.safe_load(f)
    
    extractor = PDFExtractor(config)
    cleaner = DocumentCleaner(config)
    
    # Example: Extract from a sample PDF
    sample_pdf = Path("data/raw/IS_12345_2025.pdf")
    
    if sample_pdf.exists():
        result = extractor.extract(sample_pdf)
        
        # Clean each page
        for page in result["pages"]:
            page["cleaned_text"] = cleaner.clean(page["text"])
        
        logger.info(f"Processed {result['total_pages']} pages")
    else:
        logger.warning(f"Sample PDF not found: {sample_pdf}")
