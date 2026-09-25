"""
BIS Document Collector
Collects official BIS standards and certification documents from authorized sources
"""

import requests
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import json
from loguru import logger
from bs4 import BeautifulSoup
import time


class BISDocumentCollector:
    """Collects BIS standards from official sources"""
    
    def __init__(self, config: Dict, output_dir: str = "data/raw"):
        self.config = config
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.manifest = {
            "collection_date": datetime.now().isoformat(),
            "documents": []
        }
        
    def collect_from_urls(self, document_urls: List[Dict[str, str]]) -> List[Path]:
        """
        Collect documents from provided URLs
        
        Args:
            document_urls: List of dicts with 'url', 'standard_number', 'title', etc.
            
        Returns:
            List of paths to downloaded PDFs
        """
        downloaded_files = []
        
        for doc_info in document_urls:
            try:
                file_path = self._download_document(doc_info)
                if file_path:
                    downloaded_files.append(file_path)
                    self._add_to_manifest(doc_info, file_path)
                    
                # Be respectful - rate limit requests
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Failed to download {doc_info.get('url')}: {e}")
                
        self._save_manifest()
        return downloaded_files
    
    def _download_document(self, doc_info: Dict) -> Optional[Path]:
        """Download a single document"""
        url = doc_info['url']
        standard_number = doc_info.get('standard_number', 'unknown')
        
        logger.info(f"Downloading: {standard_number} from {url}")
        
        try:
            response = requests.get(url, timeout=30, allow_redirects=True)
            response.raise_for_status()
            
            # Generate filename
            safe_name = standard_number.replace('/', '_').replace(':', '_')
            filename = f"{safe_name}_{datetime.now().strftime('%Y%m%d')}.pdf"
            file_path = self.output_dir / filename
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(response.content)
                
            logger.success(f"Downloaded: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Download failed for {url}: {e}")
            return None
    
    def _add_to_manifest(self, doc_info: Dict, file_path: Path):
        """Add document to collection manifest"""
        self.manifest["documents"].append({
            "standard_number": doc_info.get('standard_number'),
            "title": doc_info.get('title'),
            "document_type": doc_info.get('document_type'),
            "industry": doc_info.get('industry'),
            "source_url": doc_info.get('url'),
            "local_path": str(file_path),
            "collected_date": datetime.now().isoformat(),
            "file_size": file_path.stat().st_size
        })
    
    def _save_manifest(self):
        """Save collection manifest"""
        manifest_path = self.output_dir.parent / "manifests" / f"collection_{datetime.now().strftime('%Y%m%d')}.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)
            
        logger.info(f"Manifest saved: {manifest_path}")


class ManualDocumentRegistry:
    """
    Registry for manually collected BIS documents
    Since BIS documents may require authentication/subscription,
    this class helps register documents collected by authorized means
    """
    
    def __init__(self, registry_dir: str = "data/manifests"):
        self.registry_dir = Path(registry_dir)
        self.registry_dir.mkdir(parents=True, exist_ok=True)
        
    def register_document(self, 
                         file_path: str,
                         standard_number: str,
                         title: str,
                         revision: str,
                         document_type: str,
                         industry: str,
                         source_url: str = "",
                         notes: str = "") -> Dict:
        """
        Register a manually collected document
        
        This creates a metadata record for documents that were obtained
        through official channels (purchased, licensed, etc.)
        """
        doc_metadata = {
            "document_id": f"{standard_number.replace(':', '_')}_{revision}",
            "standard_number": standard_number,
            "title": title,
            "revision": revision,
            "document_type": document_type,
            "industry": industry,
            "source_url": source_url,
            "local_path": file_path,
            "registered_date": datetime.now().isoformat(),
            "notes": notes,
            "status": "registered"
        }
        
        # Save individual metadata file
        metadata_path = self.registry_dir / f"{doc_metadata['document_id']}.json"
        with open(metadata_path, 'w') as f:
            json.dump(doc_metadata, f, indent=2)
            
        logger.info(f"Registered document: {standard_number}")
        return doc_metadata
    
    def get_registered_documents(self) -> List[Dict]:
        """Get all registered documents"""
        documents = []
        for metadata_file in self.registry_dir.glob("*.json"):
            if metadata_file.name != "master_registry.json":
                with open(metadata_file) as f:
                    documents.append(json.load(f))
        return documents


if __name__ == "__main__":
    # Example usage
    from dotenv import load_dotenv
    load_dotenv()
    
    # For MVP, we'll manually register documents
    registry = ManualDocumentRegistry()
    
    # Example: Register a sample document
    # In practice, you would have obtained these through official BIS channels
    sample_docs = [
        {
            "file_path": "data/raw/IS_12345_2025.pdf",
            "standard_number": "IS 12345:2025",
            "title": "LED Lamps - Specification",
            "revision": "2025",
            "document_type": "indian_standard",
            "industry": "electronics",
            "source_url": "https://www.bis.gov.in/standards/...",
            "notes": "Sample document for MVP development"
        }
    ]
    
    for doc in sample_docs:
        registry.register_document(**doc)
    
    logger.info(f"Registered {len(sample_docs)} documents")
