# ManakAI Data Pipeline

## Overview

The data pipeline converts BIS documents into a searchable knowledge base. There are **two ways** to load data:

### Option 1: Load Pre-processed CSV (Quick Start) ⚡
**Use when:** You already have a CSV with processed BIS data (like your cement dataset)

### Option 2: Full Pipeline (Complete Processing) 🔄
**Use when:** You have raw PDF documents that need extraction and processing

---

## Option 1: Load CSV Dataset (Recommended for Demo)

### Your Dataset Structure

Your `BIS-Cement-Large-Actual-Dataset.csv` has perfect structure:

```csv
record_id,document_id,standard_number,title,revision,section,clause,
document_type,industry,source_url,page,language,content,lab_name,
osl_code,testing_charge_inr,validity_date,remark
```

### Quick Start

```bash
# 1. Place your CSV in the project
cp /path/to/BIS-Cement-Large-Actual-Dataset.csv ./data/

# 2. Load into ChromaDB
cd rag-service
python src/scripts/load_csv_to_chromadb.py \
  --csv_path ../data/BIS-Cement-Large-Actual-Dataset.csv \
  --batch_size 100 \
  --collection_name bis_standards

# 3. Verify it worked
curl http://localhost:8000/stats
```

### What Happens:

1. **Read CSV** - Loads all records with content
2. **Enhance Text** - Creates rich context for embedding:
   ```
   Standard: IS 269:2015
   Title: Ordinary Portland Cement - Specification
   Section: 7
   Clause: 7 Table-3 i
   
   Content: Fineness
   ```
3. **Generate Embeddings** - Uses Sentence Transformers
4. **Store in ChromaDB** - With full metadata for filtering
5. **Ready for Queries!** - RAG service can now answer questions

### Expected Output

```
🚀 Starting BIS CSV to ChromaDB ingestion
📂 CSV Path: ../data/BIS-Cement-Large-Actual-Dataset.csv
💾 ChromaDB Path: ./data/chromadb
📦 Collection: bis_standards
⚙️  Batch Size: 100
────────────────────────────────────────────────────────
📖 Reading CSV from: ../data/BIS-Cement-Large-Actual-Dataset.csv
✅ Loaded 147 records from CSV
📝 Preparing documents for embedding...
✅ Prepared 147 documents
🔧 Initializing ChromaDB and Embedding Service...
📤 Uploading to ChromaDB in batches of 100...
✅ Ingestion complete!

📊 Collection Statistics:
  - Total documents: 147
  
🧪 Testing retrieval with sample query...
✅ Sample query successful! Found 3 results

📄 Top Result:
  Standard: IS 269:2015
  Clause: 7 Table-3 iv a
  Content: Compressive Strength At 72 hrs ± 1 hr - IS 4031 Part 6
  
🎉 All done! Your ChromaDB is ready for queries.
```

---

## Option 2: Full Pipeline (PDF Processing)

### When to Use
- You have raw BIS PDF documents
- You need OCR for scanned documents
- You want clause-aware chunking
- You need automated metadata extraction

### Architecture

```
PDF Documents
    ↓
[PDF Extractor] - PyMuPDF + Tesseract OCR
    ↓
[Clause-Aware Chunker] - Respects document structure
    ↓
[Metadata Extractor] - Extracts standard#, clause#, etc.
    ↓
[CSV Export] - Saves processed data
    ↓
[ChromaDB Loader] - Loads into vector database
```

### Setup

```bash
cd data-pipeline

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR (for scanned PDFs)
# macOS:
brew install tesseract

# Ubuntu/Debian:
sudo apt-get install tesseract-ocr

# Configure
cp config/pipeline_config.yaml config/my_config.yaml
# Edit my_config.yaml with your settings
```

### Configuration

`config/pipeline_config.yaml`:

```yaml
data_sources:
  bis_portal:
    base_url: "https://www.bis.gov.in"
    output_dir: "./data/raw_pdfs"

extraction:
  ocr_enabled: true
  ocr_language: "eng"
  quality_threshold: 0.7

chunking:
  method: "clause_aware"
  max_chunk_size: 1000
  chunk_overlap: 100
  respect_structure: true

metadata:
  extract_standard_number: true
  extract_revision: true
  extract_clauses: true
  extract_sections: true
  industry_categorization: true

output:
  format: "csv"
  path: "./data/processed/bis_documents.csv"
```

### Run Pipeline

```bash
# Step 1: Collect PDFs (if needed)
python src/collectors/bis_collector.py --standards "IS 269" "IS 455"

# Step 2: Run full pipeline
python src/pipeline.py --config config/my_config.yaml

# Step 3: Load into ChromaDB
cd ../rag-service
python src/scripts/load_csv_to_chromadb.py \
  --csv_path ../data-pipeline/data/processed/bis_documents.csv
```

### Pipeline Output

The pipeline creates:

1. **Extracted Text** - `data/extracted/`
2. **Chunked Content** - `data/chunked/`
3. **Final CSV** - `data/processed/bis_documents.csv`
4. **Logs** - `logs/pipeline.log`

---

## Data Format Explanation

### CSV Columns (Your Format)

| Column | Description | Example |
|--------|-------------|---------|
| `record_id` | Unique record identifier | CEMENT_00001 |
| `document_id` | Document identifier | IS_269_2015 |
| `standard_number` | BIS standard number | IS 269:2015 |
| `title` | Document title | Ordinary Portland Cement - Specification |
| `revision` | Revision information | Sixth Revision |
| `section` | Section number | 6.1 |
| `clause` | Clause number | 6.1 Table-2 i |
| `document_type` | Type of document | Indian Standard |
| `industry` | Industry category | cement |
| `source_url` | Original document URL | https://lims.bis.gov.in/... |
| `page` | Page number | 18 |
| `language` | Content language | English |
| `content` | **Main text content** | Ratio of percentage of lime... |
| `lab_name` | Testing lab name | National Test House Mumbai |
| `osl_code` | Lab code | 7107604 |
| `testing_charge_inr` | Test cost in INR | 500 |
| `validity_date` | Validity date | 31 Dec, 2026 |
| `remark` | Additional notes | |

### What Gets Embedded

The `content` field + context:
```
Standard: IS 269:2015
Title: Ordinary Portland Cement - Specification
Section: 6.1
Clause: 6.1 Table-2 i

Content: Ratio of percentage of lime to percentages of silica, alumina and iron oxide
```

### What Gets Stored as Metadata

Everything else! This allows filtering like:
- "Find all requirements for IS 269:2015"
- "Show only Table-3 clauses"
- "Filter by cement industry"
- "Show tests under ₹1000"

---

## Database Structure

### ChromaDB (Vector Database)

```
Collection: bis_standards
├── Vectors (embeddings)
│   └── 384-dimensional (all-MiniLM-L6-v2)
│
└── Metadata (per document)
    ├── standard_number: "IS 269:2015"
    ├── clause: "7 Table-3 iv a"
    ├── content: "Compressive Strength..."
    ├── industry: "cement"
    ├── lab_name: "NTH Mumbai"
    └── ... (all CSV columns)
```

### PostgreSQL (Optional - Document Registry)

If you want to track which documents are loaded:

```sql
-- Optional: Track loaded documents
CREATE TABLE loaded_documents (
    id SERIAL PRIMARY KEY,
    document_id VARCHAR(100) UNIQUE,
    standard_number VARCHAR(50),
    title TEXT,
    records_count INTEGER,
    loaded_at TIMESTAMP DEFAULT NOW()
);

-- After loading CSV, insert:
INSERT INTO loaded_documents (document_id, standard_number, title, records_count)
VALUES ('IS_269_2015', 'IS 269:2015', 'Ordinary Portland Cement', 81);
```

---

## Testing Your Data

### 1. Check ChromaDB Stats

```bash
curl http://localhost:8000/stats
```

**Expected Response:**
```json
{
  "collection_name": "bis_standards",
  "count": 147,
  "embedding_dimension": 384
}
```

### 2. Test Sample Queries

```bash
# Test 1: Compressive strength
curl -X POST http://localhost:8000/internal/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the compressive strength requirements for cement?",
    "top_k": 5
  }'

# Test 2: Specific standard
curl -X POST http://localhost:8000/internal/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "IS 269:2015 fineness requirements",
    "top_k": 3
  }'

# Test 3: Testing costs
curl -X POST http://localhost:8000/internal/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the cost of compressive strength testing?",
    "top_k": 5
  }'
```

### 3. Verify Metadata Filtering

The RAG engine can filter by metadata:

```python
# In your retriever.py, you can filter like:
results = chromadb_client.query(
    query_texts=[query],
    n_results=10,
    where={
        "standard_number": "IS 269:2015",
        "industry": "cement"
    }
)
```

---

## Data Quality Tips

### For Your CSV Dataset

✅ **Good:**
- Standard numbers are consistent (IS 269:2015)
- Clause numbers are specific (7 Table-3 iv a)
- Content is concise but complete
- Metadata is rich (lab names, costs, validity)

⚠️ **Watch Out:**
- Some `page` fields are empty - that's okay
- Some `testing_charge_inr` are 0 - handled gracefully
- Empty `remark` fields - normal

### Recommended Data Checks

```python
# Check for required fields
import pandas as pd

df = pd.read_csv('BIS-Cement-Large-Actual-Dataset.csv')

print("Data Quality Report:")
print(f"Total records: {len(df)}")
print(f"Records with content: {df['content'].notna().sum()}")
print(f"Unique standards: {df['standard_number'].nunique()}")
print(f"Industries: {df['industry'].unique()}")
print(f"Languages: {df['language'].unique()}")
print(f"\nMissing data:")
print(df.isnull().sum())
```

---

## Adding More Data

### Option A: Add More CSV Files

```bash
# Load additional datasets
python src/scripts/load_csv_to_chromadb.py \
  --csv_path ../data/BIS-Steel-Dataset.csv \
  --collection_name bis_standards

python src/scripts/load_csv_to_chromadb.py \
  --csv_path ../data/BIS-Electronics-Dataset.csv \
  --collection_name bis_standards
```

All data goes into the same collection!

### Option B: Process More PDFs

```bash
cd data-pipeline

# Add PDFs to data/raw_pdfs/
cp /path/to/new-standards/*.pdf data/raw_pdfs/

# Run pipeline
python src/pipeline.py

# Load results
cd ../rag-service
python src/scripts/load_csv_to_chromadb.py \
  --csv_path ../data-pipeline/data/processed/bis_documents.csv
```

---

## Troubleshooting

### ChromaDB Not Persisting

```bash
# Check persistence path
ls -la rag-service/data/chromadb/

# If empty, ChromaDB wasn't configured for persistence
# Fix: Ensure chromadb_path is set correctly
```

### Embeddings Taking Too Long

```bash
# Use GPU if available (in .env)
DEVICE=cuda  # or 'mps' for Mac M1/M2

# Or reduce batch size
python load_csv_to_chromadb.py --batch_size 50
```

### Out of Memory

```bash
# Process in smaller batches
python load_csv_to_chromadb.py --batch_size 25
```

---

## Summary

### Your Current Dataset (Cement)
- **147 records** from BIS cement standards
- Covers IS 269, IS 8041, IS 455, IS 8042
- Includes testing requirements, labs, and costs

### Loading Process
1. **CSV → Python Script** (2 minutes)
2. **Embeddings Generated** (5-10 minutes for 147 records)
3. **Stored in ChromaDB** (instant)
4. **Ready for Queries!**

### What You Can Query Now
- ✅ "What are cement fineness requirements?"
- ✅ "IS 269:2015 compressive strength specifications"
- ✅ "Where can I test cement in Mumbai?"
- ✅ "What is the cost of expansion testing?"
- ✅ "Rapid hardening cement vs ordinary Portland cement"

---

**Next:** Start the RAG service and try some queries!

```bash
cd rag-service
uvicorn src.main:app --reload --port 8000
```
