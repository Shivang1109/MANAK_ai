#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'src'))

from retrieval.chromadb_client import ChromaDBClient

# Initialize client
config = {
    'chromadb': {
        'persist_directory': './data/chromadb',
        'collection_name': 'bis_standards'
    }
}

client = ChromaDBClient(config)

# Initialize collection
collection = client.get_or_create_collection()

# Get all unique industries  
all_data = collection.get()

industries = set()
for metadata in all_data['metadatas']:
    if 'industry' in metadata:
        industries.add(metadata['industry'])

print("All industries in ChromaDB:")
for ind in sorted(industries):
    print(f"  - {ind}")

print(f"\nTotal unique industries: {len(industries)}")

# Check for Automotive specifically
automotive_count = sum(1 for m in all_data['metadatas'] if m.get('industry') == 'Automotive')
print(f"\nAutomotive records: {automotive_count}")

# Check a sample automotive record
for i, metadata in enumerate(all_data['metadatas']):
    if metadata.get('industry') == 'Automotive':
        print(f"\nSample Automotive record #{i+1}:")
        print(f"  Standard: {metadata.get('standard_number')}")
        print(f"  Clause: {metadata.get('clause')}")
        print(f"  Content: {metadata.get('content', '')[:100]}...")
        break
