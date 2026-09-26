"""
Add expanded demo data for ManakAI
Covers multiple popular product categories with detailed BIS specifications
"""

import chromadb
from datetime import datetime

def add_expanded_demo_data():
    """Add comprehensive demo data across multiple categories"""
    
    client = chromadb.PersistentClient(path="./data/chromadb")
    collection = client.get_collection("bis_standards")
    
    print("Adding expanded demo data...")
    
    # LED BULBS (Electronics)
    led_chunks = [
        {
            "id": "led_001",
            "content": """IS 16102 (Part 2):2023 - Self-Ballasted LED Lamps for General Lighting Services - Safety Requirements

Section 3: GENERAL REQUIREMENTS
3.1 Voltage Rating
LED lamps shall be designed for operation at 220V ± 10% at 50Hz AC supply. The lamp shall operate safely and efficiently within this voltage range.

3.2 Power Factor
The power factor of LED lamps shall not be less than 0.7 for lamps rated above 25W, and not less than 0.5 for lamps rated at 25W and below.

3.3 Temperature Limits
During normal operation, accessible parts of the lamp shall not exceed 90°C. Internal components may reach higher temperatures but must remain within manufacturer specifications.""",
            "metadata": {
                "standard_number": "IS 16102 (Part 2):2023",
                "title": "Self-Ballasted LED Lamps - Safety Requirements",
                "clause": "3.1-3.3",
                "section": "3",
                "page": 8,
                "industry": "electronics",
                "product": "led_bulbs",
                "document_type": "Indian Standard",
                "chunk_size": 730,
                "is_demo": "true"
            }
        },
        {
            "id": "led_002",
            "content": """IS 16102 (Part 2):2023 - Self-Ballasted LED Lamps - Safety Requirements

Section 4: PHOTOMETRIC REQUIREMENTS
4.1 Luminous Efficacy
The luminous efficacy of LED lamps shall be at least 80 lumens per watt for lamps rated above 15W, and at least 70 lumens per watt for lamps rated at 15W and below.

4.2 Color Rendering Index (CRI)
The general color rendering index (Ra) shall not be less than 80. For applications requiring high color accuracy, Ra ≥ 90 is recommended.

4.3 Correlated Color Temperature (CCT)
LED lamps shall be available in standard CCT ranges: Warm White (2700K-3000K), Cool White (4000K-4500K), and Day Light (5500K-6500K). Tolerance: ±300K.""",
            "metadata": {
                "standard_number": "IS 16102 (Part 2):2023",
                "title": "Self-Ballasted LED Lamps - Safety Requirements",
                "clause": "4.1-4.3",
                "section": "4",
                "page": 12,
                "industry": "electronics",
                "product": "led_bulbs",
                "document_type": "Indian Standard",
                "chunk_size": 778,
                "is_demo": "true"
            }
        },
        {
            "id": "led_003",
            "content": """IS 16102 (Part 2):2023 - Self-Ballasted LED Lamps - Safety Requirements

Section 7: CERTIFICATION AND MARKING REQUIREMENTS
7.1 Mandatory Certification
LED lamps fall under mandatory BIS certification as per Quality Control Order (Electric Lamps and Related Components) 2022. Manufacturers must obtain BIS License (IS Mark) before sale in India.

7.2 Marking Requirements
Each lamp shall be permanently and legibly marked with: (a) IS Mark with license number, (b) Manufacturer name or trademark, (c) Rated voltage and frequency, (d) Rated wattage, (e) Luminous flux in lumens, (f) Color temperature, (g) Batch or manufacturing code.

7.3 Testing Frequency
Licensed manufacturers shall conduct type tests every two years and routine tests as per IS 4852.""",
            "metadata": {
                "standard_number": "IS 16102 (Part 2):2023",
                "title": "Self-Ballasted LED Lamps - Safety Requirements",
                "clause": "7.1-7.3",
                "section": "7",
                "page": 24,
                "industry": "electronics",
                "product": "led_bulbs",
                "document_type": "Indian Standard",
                "chunk_size": 851,
                "is_demo": "true"
            }
        }
    ]
    
    # STEEL BARS (Construction)
    steel_chunks = [
        {
            "id": "steel_001",
            "content": """IS 1786:2008 - High Strength Deformed Steel Bars and Wires for Concrete Reinforcement - Specification

Section 5: CHEMICAL COMPOSITION
5.1 General Requirements
Steel shall be made by any accepted steel making process. The chemical composition shall conform to the limits specified in Table 1.

5.2 Carbon Content
Maximum carbon content shall not exceed 0.30% by mass for all grades (Fe 415, Fe 500, Fe 550, Fe 600).

5.3 Sulphur and Phosphorus
Maximum sulphur content: 0.055% by mass. Maximum phosphorus content: 0.055% by mass. These limits ensure adequate ductility and weldability.

5.4 Carbon Equivalent
Carbon equivalent (CE) shall not exceed 0.54% when calculated using formula: CE = C + Mn/6 + (Cr+Mo+V)/5 + (Ni+Cu)/15.""",
            "metadata": {
                "standard_number": "IS 1786:2008",
                "title": "High Strength Deformed Steel Bars for Concrete Reinforcement",
                "clause": "5.1-5.4",
                "section": "5",
                "page": 6,
                "industry": "construction",
                "product": "steel_bars",
                "document_type": "Indian Standard",
                "chunk_size": 847,
                "is_demo": "true"
            }
        },
        {
            "id": "steel_002",
            "content": """IS 1786:2008 - High Strength Deformed Steel Bars - Specification

Section 6: MECHANICAL PROPERTIES
6.1 Tensile Strength Requirements
Fe 415: Yield strength ≥ 415 N/mm², Ultimate tensile strength ≥ 485 N/mm²
Fe 500: Yield strength ≥ 500 N/mm², Ultimate tensile strength ≥ 545 N/mm²
Fe 550: Yield strength ≥ 550 N/mm², Ultimate tensile strength ≥ 585 N/mm²

6.2 Elongation
Minimum elongation on gauge length 5.65√A (where A is cross-sectional area) shall be 14.5% for all grades.

6.3 Bend Test
Bars shall withstand bending through 180° around a mandrel without cracking. Mandrel diameter: 4d for Fe 415, 5d for Fe 500 and above (where d = nominal bar diameter).""",
            "metadata": {
                "standard_number": "IS 1786:2008",
                "title": "High Strength Deformed Steel Bars for Concrete Reinforcement",
                "clause": "6.1-6.3",
                "section": "6",
                "page": 8,
                "industry": "construction",
                "product": "steel_bars",
                "document_type": "Indian Standard",
                "chunk_size": 794,
                "is_demo": "true"
            }
        }
    ]
    
    # FOOD PACKAGING (Food Safety)
    packaging_chunks = [
        {
            "id": "pack_001",
            "content": """IS 10146:2023 - Code of Practice for Packaging of Food Products

Section 4: MATERIALS FOR FOOD CONTACT
4.1 Primary Packaging Materials
Materials in direct contact with food shall comply with Prevention of Food Adulteration Rules and FSSAI regulations. Only food-grade materials permitted under Schedule IV of FSS (Packaging) Regulations 2018 shall be used.

4.2 Plastic Materials
Plastics shall not contain more than: Lead (Pb) ≤ 1 ppm, Cadmium (Cd) ≤ 0.5 ppm, Mercury (Hg) ≤ 0.5 ppm, Hexavalent Chromium (Cr VI) ≤ 0.1 ppm. Virgin food-grade polymers are preferred. Recycled plastics require specific approval.

4.3 Migration Limits
Overall migration limit: 10 mg/dm² of food contact area or 60 mg/kg of food simulant. Specific migration of additives and monomers shall not exceed limits in Annex A.""",
            "metadata": {
                "standard_number": "IS 10146:2023",
                "title": "Code of Practice for Packaging of Food Products",
                "clause": "4.1-4.3",
                "section": "4",
                "page": 11,
                "industry": "food_packaging",
                "product": "food_packaging",
                "document_type": "Indian Standard",
                "chunk_size": 944,
                "is_demo": "true"
            }
        },
        {
            "id": "pack_002",
            "content": """IS 10146:2023 - Code of Practice for Packaging of Food Products

Section 6: LABELING REQUIREMENTS
6.1 Mandatory Information
All food packages shall display: (a) Product name, (b) List of ingredients in descending order by weight, (c) Nutritional information per 100g/ml, (d) Net quantity, (e) Manufacturer name and address, (f) Manufacturing and expiry dates, (g) FSSAI license number, (h) Storage instructions, (i) Allergen warnings if applicable.

6.2 Material Declaration
Packages shall indicate "Food Grade" marking. For plastics, recycling code and "For food contact only" shall be embossed or printed.

6.3 Tamper-Evidence
Primary packages of processed foods shall have tamper-evident features clearly visible to consumers.""",
            "metadata": {
                "standard_number": "IS 10146:2023",
                "title": "Code of Practice for Packaging of Food Products",
                "clause": "6.1-6.3",
                "section": "6",
                "page": 18,
                "industry": "food_packaging",
                "product": "food_packaging",
                "document_type": "Indian Standard",
                "chunk_size": 855,
                "is_demo": "true"
            }
        }
    ]
    
    # ELECTRICAL SWITCHES (Electronics)
    switch_chunks = [
        {
            "id": "switch_001",
            "content": """IS 3854:2022 - AC Switches for Household and Similar Purposes - Specification

Section 4: ELECTRICAL RATINGS
4.1 Voltage Rating
Switches shall be rated for 230V AC ±10%, 50Hz for single-phase applications. Three-phase switches: 400V AC ±10%, 50Hz.

4.2 Current Rating
Household switches standard ratings: 6A, 10A, 16A, 20A, 25A, 32A. Current capacity shall be marked clearly on the switch body. Switches must carry rated current continuously without exceeding temperature limits.

4.3 Breaking Capacity
Switches shall safely break at least 1500A prospective short circuit current at rated voltage. Minimum electrical endurance: 10,000 operations under rated load.

4.4 Insulation Resistance
Between live parts and earth: ≥ 5 MΩ at 500V DC. Between open contacts: ≥ 5 MΩ at 500V DC.""",
            "metadata": {
                "standard_number": "IS 3854:2022",
                "title": "AC Switches for Household - Specification",
                "clause": "4.1-4.4",
                "section": "4",
                "page": 9,
                "industry": "electrical_electronics",
                "product": "electrical_switches",
                "document_type": "Indian Standard",
                "chunk_size": 847,
                "is_demo": "true"
            }
        },
        {
            "id": "switch_002",
            "content": """IS 3854:2022 - AC Switches for Household - Specification

Section 7: SAFETY REQUIREMENTS
7.1 Electric Shock Protection
Switches shall provide protection against electric shock by basic insulation. Live parts shall not be accessible when installed as per manufacturer instructions. Clearance between live parts and accessible surfaces: minimum 3mm.

7.2 Fire Hazard Prevention
Switch body and cover shall be made of self-extinguishing thermoplastic material with glow-wire test rating minimum 850°C. Material shall meet UL94 V-0 or equivalent flammability rating.

7.3 Mechanical Strength
Switch shall withstand impact test with 0.35 Nm pendulum without cracking or creating hazardous openings. Operating mechanism shall not jam or become inoperative.""",
            "metadata": {
                "standard_number": "IS 3854:2022",
                "title": "AC Switches for Household - Specification",
                "clause": "7.1-7.3",
                "section": "7",
                "page": 16,
                "industry": "electrical_electronics",
                "product": "electrical_switches",
                "document_type": "Indian Standard",
                "chunk_size": 848,
                "is_demo": "true"
            }
        }
    ]
    
    # TEXTILES (Cotton Fabric)
    textile_chunks = [
        {
            "id": "textile_001",
            "content": """IS 1346:2023 - Cotton Fabrics (Grey) - Specification

Section 5: QUALITY REQUIREMENTS
5.1 Thread Count
Minimum thread count shall be as specified for each fabric type: Shirting - 60 ends/cm warp, 48 picks/cm weft. Suiting - 50 ends/cm warp, 40 picks/cm weft. Tolerance: ±5% on stated count.

5.2 Fabric Weight (GSM)
Grey fabric weight tolerance: ±5% of declared GSM (grams per square meter). Standard weights: Lightweight (100-150 GSM), Medium weight (150-200 GSM), Heavyweight (200-300 GSM).

5.3 Yarn Count and Twist
Cotton yarn shall conform to IS 1840. Minimum twist factor: 3.7 for warp, 3.5 for weft. Count strength product (CSP) minimum: 2000 for combed yarn, 1800 for carded yarn.""",
            "metadata": {
                "standard_number": "IS 1346:2023",
                "title": "Cotton Fabrics (Grey) - Specification",
                "clause": "5.1-5.3",
                "section": "5",
                "page": 7,
                "industry": "textiles",
                "product": "cotton_fabric",
                "document_type": "Indian Standard",
                "chunk_size": 813,
                "is_demo": "true"
            }
        },
        {
            "id": "textile_002",
            "content": """IS 1346:2023 - Cotton Fabrics (Grey) - Specification

Section 6: PHYSICAL PROPERTIES AND TESTING
6.1 Tensile Strength
Minimum breaking strength (strip method): Warp direction ≥ 40 kgf, Weft direction ≥ 35 kgf for medium weight fabrics. Test as per IS 1969 (Part 1).

6.2 Tear Strength
Minimum tear strength (single rip method): Warp ≥ 1500 gf, Weft ≥ 1200 gf. Test as per IS 6489.

6.3 Dimensional Stability
Maximum shrinkage after washing: Warp direction ≤ 3%, Weft direction ≤ 3%. For pre-shrunk fabrics: ≤ 1.5% in both directions. Test as per IS 687.

6.4 Defects and Inspection
Fabric shall be free from major defects. Maximum permissible minor defects: 3 per 10 linear meters.""",
            "metadata": {
                "standard_number": "IS 1346:2023",
                "title": "Cotton Fabrics (Grey) - Specification",
                "clause": "6.1-6.4",
                "section": "6",
                "page": 10,
                "industry": "textiles",
                "product": "cotton_fabric",
                "document_type": "Indian Standard",
                "chunk_size": 856,
                "is_demo": "true"
            }
        }
    ]
    
    # Combine all chunks
    all_chunks = led_chunks + steel_chunks + packaging_chunks + switch_chunks + textile_chunks
    
    # Prepare for ChromaDB
    documents = [chunk["content"] for chunk in all_chunks]
    metadatas = [chunk["metadata"] for chunk in all_chunks]
    ids = [chunk["id"] for chunk in all_chunks]
    
    # Add to collection
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"\n✅ Successfully added {len(all_chunks)} demo chunks!")
    print(f"\nBreakdown by category:")
    print(f"  - LED Bulbs: {len(led_chunks)} chunks")
    print(f"  - Steel Bars: {len(steel_chunks)} chunks")
    print(f"  - Food Packaging: {len(packaging_chunks)} chunks")
    print(f"  - Electrical Switches: {len(switch_chunks)} chunks")
    print(f"  - Cotton Textiles: {len(textile_chunks)} chunks")
    
    # Final count
    total = collection.count()
    print(f"\n📊 Total chunks in database: {total}")
    
    return all_chunks

if __name__ == "__main__":
    chunks = add_expanded_demo_data()
    
    print("\n🎉 Demo data expansion complete!")
    print("Try these queries:")
    print("  - What are the voltage requirements for LED bulbs?")
    print("  - What are the mechanical properties of steel bars?")
    print("  - What are food packaging safety requirements?")
    print("  - Electrical switch current ratings")
    print("  - Cotton fabric quality specifications")
