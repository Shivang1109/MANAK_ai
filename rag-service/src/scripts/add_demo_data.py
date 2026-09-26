"""
Add demo BIS standards data with full content for Monday demo
This creates proper chunks with actual requirements, not just metadata
"""

import chromadb
from datetime import datetime

# Sample BIS standard content with full requirements
DEMO_STANDARDS = [
    {
        "standard_number": "IS 269:2015",
        "title": "Ordinary Portland Cement - Specification",
        "chunks": [
            {
                "clause": "4.1",
                "content": """
IS 269:2015 - Ordinary Portland Cement Specification

Section 4: CHEMICAL REQUIREMENTS

4.1 Chemical Composition
The chemical composition of ordinary Portland cement shall conform to the following requirements:

a) Ratio of percentage of lime to percentages of silica, alumina and iron oxide, when calculated by the formula:
   CaO - 0.7 SO₃ / (SiO₂ + Al₂O₃ + Fe₂O₃)
   shall not be less than 0.66 and not more than 1.02

b) Ratio of percentage of alumina to that of iron oxide shall not be less than 0.66

c) Insoluble residue shall not exceed 4 percent by mass

d) Magnesia (MgO) content shall not exceed 6 percent by mass

e) Total sulphur content calculated as sulphuric anhydride (SO₃) shall not exceed 3 percent by mass

f) Total loss on ignition shall not exceed 5 percent by mass

g) Chloride content as Cl shall not exceed 0.05 percent by mass
""",
                "page": 5
            },
            {
                "clause": "5.1",
                "content": """
IS 269:2015 - Ordinary Portland Cement Specification

Section 5: PHYSICAL REQUIREMENTS

5.1 Fineness
The fineness of cement shall be such that when tested by dry sieving on 90 micron IS Sieve, the residue shall not exceed 10 percent by mass.

When determined by specific surface (Blaine method), it shall not be less than 225 m²/kg.

5.2 Soundness
The soundness of cement when tested by Le Chatelier method shall not be more than 10 mm.

When tested by Autoclave method, the expansion shall not be more than 0.8 percent.

5.3 Setting Time
a) Initial setting time shall not be less than 30 minutes when tested by Vicat apparatus
b) Final setting time shall not be more than 600 minutes (10 hours)

5.4 Compressive Strength
The compressive strength of cement mortar cubes shall not be less than the values given below:

Test Period | Minimum Compressive Strength (MPa)
72 ± 1 hours (3 days) | 23
168 ± 2 hours (7 days) | 33
672 ± 4 hours (28 days) | 43
""",
                "page": 6
            },
            {
                "clause": "7.1",
                "content": """
IS 269:2015 - Ordinary Portland Cement Specification

Section 7: TESTING AND QUALITY CONTROL

7.1 Sampling
Samples for testing shall be drawn in accordance with IS 3535.

7.2 Chemical Tests
Chemical tests shall be conducted as per IS 4032.

7.3 Physical Tests
a) Fineness test - IS 4031 (Part 1)
b) Soundness test - IS 4031 (Part 3) 
c) Setting time - IS 4031 (Part 5)
d) Compressive strength - IS 4031 (Part 6)

7.4 Test Frequency
Minimum one sample shall be tested for every 50 tonnes of cement produced or part thereof.

7.5 Acceptance Criteria
A lot shall be accepted if all test results comply with the requirements specified in Sections 4 and 5.
""",
                "page": 8
            }
        ]
    },
    {
        "standard_number": "IS 10500:2012",
        "title": "Drinking Water - Specification",
        "chunks": [
            {
                "clause": "4.1",
                "content": """
IS 10500:2012 - Drinking Water Specification

Section 4: REQUIREMENTS

4.1 Organoleptic and Physical Requirements

Parameter | Acceptable Limit | Permissible Limit in Absence of Alternative
---------|------------------|----------------------------------------
Colour (Hazen units, Max) | 5 | 25
Odour | Agreeable | Agreeable
Taste | Agreeable | Agreeable  
Turbidity (NTU, Max) | 1 | 5
pH value | 6.5 to 8.5 | No relaxation
Total Hardness (mg/l as CaCO₃, Max) | 200 | 600
Iron (mg/l as Fe, Max) | 0.3 | No relaxation
Total Dissolved Solids (mg/l, Max) | 500 | 2000
Chlorides (mg/l as Cl, Max) | 250 | 1000
Sulphate (mg/l as SO₄, Max) | 200 | 400

4.2 Chemical Requirements
All chemical parameters shall be within the acceptable limits specified in Table 2 of this standard.
""",
                "page": 3
            },
            {
                "clause": "4.3",
                "content": """
IS 10500:2012 - Drinking Water Specification

Section 4: REQUIREMENTS (continued)

4.3 Toxic Substances

The following toxic substances shall not exceed the limits specified:

a) Arsenic (mg/l as As): Max 0.01 (No relaxation)
b) Cadmium (mg/l as Cd): Max 0.003 (No relaxation)
c) Chromium (mg/l as Cr): Max 0.05 (No relaxation)
d) Cyanide (mg/l as CN): Max 0.05 (No relaxation)
e) Lead (mg/l as Pb): Max 0.01 (No relaxation)
f) Mercury (mg/l as Hg): Max 0.001 (No relaxation)
g) Nitrate (mg/l as NO₃): Max 45 (No relaxation)
h) Fluoride (mg/l as F): Max 1.0, Permissible 1.5

4.4 Pesticide Residues
Shall not exceed limits specified in Annex A.

4.5 Radioactive Substances
Alpha emitters: Max 0.1 Bq/l
Beta emitters: Max 1.0 Bq/l
""",
                "page": 4
            },
            {
                "clause": "5.1",
                "content": """
IS 10500:2012 - Drinking Water Specification

Section 5: BACTERIOLOGICAL REQUIREMENTS

5.1 Microbiological Quality
Drinking water shall conform to the following bacteriological requirements:

a) All water intended for drinking should be free from Escherichia coli or thermotolerant coliform bacteria
b) E.coli or thermotolerant coliform must not be detectable in any 100 ml sample
c) Total coliform bacteria should not be detectable in any 100 ml sample
d) For treated water entering distribution system: E.coli = 0 per 100 ml

5.2 Testing Frequency
a) Community water supplies: At least once a month
b) Piped water supplies: Based on population served, minimum once per week
c) At point of delivery: Regular monitoring required

5.3 Disinfection
a) Free residual chlorine: 0.2 to 1.0 mg/l (after 30 min contact)
b) At consumer end: Min 0.2 mg/l
""",
                "page": 5
            }
        ]
    }
]

def add_demo_data():
    """Add comprehensive demo data to ChromaDB"""
    
    # Connect to ChromaDB
    client = chromadb.PersistentClient(path="./data/chromadb")
    collection = client.get_or_create_collection("bis_standards")
    
    print("Adding demo BIS standards with full content...\n")
    
    for standard in DEMO_STANDARDS:
        std_num = standard["standard_number"]
        title = standard["title"]
        
        print(f"Processing: {std_num} - {title}")
        
        for i, chunk in enumerate(standard["chunks"]):
            # Create unique ID
            chunk_id = f"demo_{std_num.replace(':', '_').replace(' ', '')}_{i}"
            
            # Prepare metadata
            metadata = {
                "standard_number": std_num,
                "title": title,
                "clause": chunk["clause"],
                "page": chunk["page"],
                "document_type": "Indian Standard",
                "industry": "cement" if "cement" in title.lower() else "drinking_water",
                "source": "Demo Data",
                "chunk_size": len(chunk["content"]),
                "is_demo": "true"
            }
            
            # Add to collection
            collection.add(
                ids=[chunk_id],
                documents=[chunk["content"]],
                metadatas=[metadata]
            )
            
            print(f"  ✓ Added chunk {i+1}: Clause {chunk['clause']} ({len(chunk['content'])} chars)")
        
        print()
    
    # Verify
    total = collection.count()
    print(f"\n✅ Demo data added successfully!")
    print(f"Total chunks in database: {total}")
    
    # Test query
    print("\n🔍 Testing retrieval...")
    results = collection.query(
        query_texts=["cement chemical requirements"],
        n_results=2
    )
    
    print(f"Found {len(results['documents'][0])} relevant chunks")
    for i, doc in enumerate(results['documents'][0], 1):
        print(f"\nChunk {i} preview (first 200 chars):")
        print(doc[:200] + "...")

if __name__ == "__main__":
    add_demo_data()
