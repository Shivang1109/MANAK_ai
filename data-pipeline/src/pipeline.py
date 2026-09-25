"""
ManakAI Data Pipeline
Main orchestrator for BIS document processing pipeline
"""

import yaml
from pathlib import Path
from typing import List, Dict
from loguru import logger
import json
from datetime import datetime

from extractors.pdf_extractor import PDFExtractor, DocumentCleaner
from chunkers.clause_aware_chunker import ClauseAwareChunker
from metadata.metadata_extractor import MetadataExtractor
from collectors.bis_collector import ManualDocumentRegistry


class DataPipeline:
    """Main data processing pipeline"""
    
    def __init__(self, config_path: str = "config/pipeline_config.yaml"):
        """Initialize pipeline with configuration"""
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        
        # Initialize components
        self.registry = ManualDocumentRegistry()
        self.pdf_extractor = PDFExtractor(self.config)
        self.document_cleaner = DocumentCleaner(self.config)
        self.chunker = ClauseAwareChunker(self.config)
        self.metadata_extractor = MetadataExtractor(self.config)
        
        # Setup logging
        log_config = self.config.get('logging', {})
        logger.add(
            log_config.get('log_file', 'pipeline.log'),
            format=log_config.get('format'),
            level=log_config.get('level', 'INFO')
        )
        
        # Output directory
        self.processed_dir = Path(self.config['directories']['processed'])
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
    def process_all_documents(self) -> Dict:
        """Process all registered documents"""
        logger.info("Starting data pipeline...")
        
        documents = self.registry.get_registered_documents()
        logger.info(f"Found {len(documents)} registered documents")
        
        results = {
            'processed': 0,
            'failed': 0,
            'total_chunks': 0,
            'documents': []
        }
        
        for doc_metadata in documents:
            try:
                chunks = self.process_document(doc_metadata)
                results['processed'] += 1
                results['total_chunks'] += len(chunks)
                results['documents'].append({
                    'document_id': doc_metadata['document_id'],
                    'status': 'success',
                    'chunks': len(chunks)
                })
            except Exception as e:
                logger.error(f"Failed to process {doc_metadata['document_id']}: {e}")
                results['failed'] += 1
                results['documents'].append({
                    'document_id': doc_metadata['document_id'],
                    'status': 'failed',
                    'error': str(e)
                })
        
        # Save pipeline report
        self._save_report(results)
        
        logger.success(
            f"Pipeline complete: {results['processed']} processed, "
            f"{results['failed']} failed, {results['total_chunks']} total chunks"
        )
        
        return results
    
    def process_document(self, doc_metadata: Dict) -> List[Dict]:
        """
        Process a single document through the pipeline
        
        Args:
            doc_metadata: Document metadata from registry
            
        Returns:
            List of processed chunks
        """
        pdf_path = Path(doc_metadata['local_path'])
        logger.info(f"Processing: {doc_metadata['standard_number']}")
        
        # Step 1: Extract text from PDF
        extraction_result = self.pdf_extractor.extract(pdf_path)
        
        # Step 2: Clean text
        for page in extraction_result['pages']:
            page['cleaned_text'] = self.document_cleaner.clean(page['text'])
        
        # Step 3: Extract/enhance metadata
        full_text = '\n\n'.join(page['cleaned_text'] for page in extraction_result['pages'])
        enhanced_metadata = self.metadata_extractor.extract_document_metadata(
            full_text,
            doc_metadata
        )
        
        # Step 4: Chunk document
        chunks = self.chunker.chunk_document(extraction_result['pages'], enhanced_metadata)
        
        # Step 5: Save processed chunks
        self._save_chunks(chunks, enhanced_metadata)
        
        logger.success(f"Processed {len(chunks)} chunks for {enhanced_metadata['standard_number']}")
        
        return chunks
    
    def _save_chunks(self, chunks: List[Dict], doc_metadata: Dict):
        """Save processed chunks to disk"""
        output_file = self.processed_dir / f"{doc_metadata['document_id']}_chunks.json"
        
        output_data = {
            'document_metadata': doc_metadata,
            'processed_date': datetime.now().isoformat(),
            'chunk_count': len(chunks),
            'chunks': chunks
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved chunks: {output_file}")
    
    def _save_report(self, results: Dict):
        """Save pipeline execution report"""
        report_file = self.processed_dir.parent / 'manifests' / f"pipeline_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Pipeline report saved: {report_file}")
    
    def get_all_chunks(self) -> List[Dict]:
        """Load all processed chunks"""
        all_chunks = []
        
        for chunk_file in self.processed_dir.glob("*_chunks.json"):
            with open(chunk_file) as f:
                data = json.load(f)
                all_chunks.extend(data['chunks'])
        
        logger.info(f"Loaded {len(all_chunks)} chunks from {len(list(self.processed_dir.glob('*_chunks.json')))} documents")
        return all_chunks


def main():
    """Run the pipeline"""
    pipeline = DataPipeline()
    
    # Process all registered documents
    results = pipeline.process_all_documents()
    
    print("\n" + "="*50)
    print("PIPELINE RESULTS")
    print("="*50)
    print(f"Documents processed: {results['processed']}")
    print(f"Documents failed: {results['failed']}")
    print(f"Total chunks created: {results['total_chunks']}")
    print("="*50)
    
    # Get all chunks for next step (embedding & ChromaDB)
    all_chunks = pipeline.get_all_chunks()
    print(f"\nReady for embedding: {len(all_chunks)} chunks")


if __name__ == "__main__":
    main()
