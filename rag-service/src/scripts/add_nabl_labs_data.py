"""
ManakAI — ChromaDB data loader
Covers: NABL-accredited testing laboratories for BIS product certification
Problem statement requirement: "Suggest relevant testing laboratories"

Run from rag-service directory:
    python add_nabl_labs_data.py
"""

import chromadb


def add_data():
    client = chromadb.PersistentClient(path="./data/chromadb")
    collection = client.get_collection("bis_standards")

    lab_chunks = [

        # ── OVERVIEW ─────────────────────────────────────────────
        {
            "id": "lab_001",
            "content": """TESTING LABORATORIES FOR BIS CERTIFICATION — How to Find the Right Lab

For BIS product certification (Scheme I, CRS, FMCS), products must be tested at:
1. BIS own laboratories, OR
2. NABL-accredited laboratories recognised by BIS for the specific standard, OR
3. For FMCS: laboratories accredited by ILAC-MRA member bodies abroad

WHAT IS NABL?
National Accreditation Board for Testing and Calibration Laboratories (NABL) is the authorised body under DST (Dept. of Science & Technology) that accredits testing labs in India.
NABL accreditation = lab meets ISO/IEC 17025 quality standards.

HOW TO FIND A NABL LAB FOR YOUR PRODUCT:
Method 1 — NABL website: nabl-india.org → Search labs by discipline, standard or location
Method 2 — BIS website: bis.gov.in → Certification → Recognised Labs → select product category
Method 3 — BIS helpline: 1800-11-4455

WHAT TO TELL THE LAB:
1. Product name and model
2. Applicable Indian Standard (IS number)
3. Purpose: BIS certification / CRS registration / export compliance
4. Urgency (standard or express testing)

LAB SELECTION TIPS:
- Confirm the lab is currently BIS-recognised (not just NABL accredited) for YOUR specific IS standard
- Ask for test report turnaround time (typically 2-6 weeks)
- Get a written quote including all test parameters
- Check if the lab can issue the test report format accepted by BIS""",
            "metadata": {
                "standard_number": "NABL Lab Finder",
                "title": "How to Find NABL Testing Laboratories for BIS Certification",
                "clause": "1.1-1.5",
                "section": "1",
                "page": 1,
                "industry": "testing_labs",
                "product": "all_products",
                "document_type": "BIS Lab Directory",
                "language": "English",
            }
        },

        # ── ELECTRONICS / LED LABS ────────────────────────────────
        {
            "id": "lab_002",
            "content": """TESTING LABORATORIES — Electronics, LED Lamps and Electrical Products

FOR LED LAMPS (IS 16102, IS 16103, IS 16107, IS 16108):

BIS CENTRAL LABORATORIES (Official):
1. BIS Central Laboratory, Mumbai
   Address: Manakalaya, E-9 BKC, Bandra (East), Mumbai 400051
   Phone: 022-26590295
   Tests: Electrical safety, photometric, CRI, luminous flux

2. BIS Regional Office Lab, Delhi
   Address: 8, Kalibari Marg, New Delhi 110001
   Phone: 011-23235490
   Tests: Electrical safety, performance testing for all electronics

NABL/BIS RECOGNISED LABS FOR ELECTRONICS (Major):
3. ERDA (Electrical Research & Development Association), Vadodara
   Accreditation: NABL + BIS recognised
   Scope: LED lamps, luminaires, switchgear, cables, appliances
   Phone: 0265-2638811 | erda.in
   TAT: 3-4 weeks for LED certification

4. CPRI (Central Power Research Institute), Bangalore
   Accreditation: NABL + BIS recognised
   Scope: All electrical equipment, power cables, transformers, meters
   Phone: 080-22207536 | cpri.in
   TAT: 4-6 weeks

5. ERTL (Electronics Regional Test Laboratory), Various cities
   Locations: New Delhi, Mumbai, Bangalore, Kolkata, Hyderabad
   Scope: IT equipment, mobile phones, chargers, CRS products
   Website: ertl.gov.in

6. Bureau Veritas Testing Lab, Gurgaon
   Accreditation: NABL + BIS recognised
   Scope: Electronics, electrical, consumer products
   Phone: 1800-200-3000 | bureauveritas.com/india

FOR SWITCHES AND SOCKETS (IS 3854, IS 1293):
- CPRI Bangalore (comprehensive testing)
- ERDA Vadodara (Scheme I certification support)
- Intertek India, Gurgaon/Mumbai

TYPICAL COSTS FOR LED LAMP TESTING:
- Safety testing (IS 16102): ₹15,000 - ₹30,000 per model
- Performance testing (IS 16103): ₹20,000 - ₹40,000 per model
- Complete BIS certification package: ₹40,000 - ₹80,000""",
            "metadata": {
                "standard_number": "BIS Recognised Labs — Electronics",
                "title": "Testing Labs for LED Lamps, Electronics and Electrical Products",
                "clause": "2.1-2.4",
                "section": "2",
                "page": 4,
                "industry": "testing_labs",
                "product": "electronics_led",
                "document_type": "BIS Lab Directory",
                "language": "English",
            }
        },

        # ── MEDICAL DEVICE LABS ───────────────────────────────────
        {
            "id": "lab_003",
            "content": """TESTING LABORATORIES — Medical Devices and Equipment

FOR MEDICAL DEVICES (IS 13450, Medical Devices Rules 2017):

Note: Medical devices in India are regulated jointly by:
- BIS (for IS standards compliance)
- CDSCO (Central Drugs Standard Control Organisation) for MD licencing

BIS RECOGNISED LABS FOR MEDICAL DEVICES:
1. NABL Central Laboratory, BIS Mumbai
   Scope: Electromedical equipment (IS 13450 series)
   Contact: bis.gov.in → lab services

2. SCTIMST (Sree Chitra Tirunal Institute), Trivandrum
   Accreditation: NABL + DST
   Scope: Biomedical equipment, implants, surgical instruments
   Phone: 0471-2520291 | sctimst.ac.in

3. IIT Bombay Testing Lab
   Scope: Electromedical, biosensors, diagnostic equipment
   Contact: rnd.iitb.ac.in

4. NTTF-MDT, Bangalore
   Scope: Medical device testing, ISO 10993 biocompatibility
   Phone: 080-23723414

5. SGS India, Multiple locations
   Accreditation: NABL + international
   Scope: Medical devices, EMC testing, safety (IEC 60601)
   Website: sgs.com/en-gb/india

FOR VENTILATORS AND CRITICAL CARE EQUIPMENT (IS 13450 Part 2):
- BIS Lab, Mumbai (reference lab)
- SAMEER (Society for Applied Microwave Electronics Engineering & Research), Mumbai
  Phone: 022-26290362 | sameer.gov.in

FOR ECG EQUIPMENT:
- SAMEER Mumbai (electromagnetic compatibility)
- BIS Central Lab (safety compliance IS 13450-2-25)

TYPICAL COSTS FOR MEDICAL DEVICE TESTING:
- ECG equipment full compliance: ₹1,50,000 - ₹3,00,000
- Ventilator safety testing: ₹2,00,000 - ₹5,00,000
- X-ray equipment: ₹3,00,000 - ₹8,00,000
- Turnaround time: 8-16 weeks (due to complexity)""",
            "metadata": {
                "standard_number": "BIS Recognised Labs — Medical",
                "title": "Testing Labs for Medical Devices and Electromedical Equipment",
                "clause": "3.1-3.4",
                "section": "3",
                "page": 8,
                "industry": "testing_labs",
                "product": "medical_devices",
                "document_type": "BIS Lab Directory",
                "language": "English",
            }
        },

        # ── WATER QUALITY LABS ────────────────────────────────────
        {
            "id": "lab_004",
            "content": """TESTING LABORATORIES — Water Quality (Drinking Water, Packaged Water)

FOR DRINKING WATER (IS 10500) AND PACKAGED WATER (IS 14543):

BIS RECOGNISED LABS FOR WATER TESTING:
1. National Reference Trace Element and Mineral Nutrient Laboratory (NRTEMN), AIIMS Delhi
   Scope: Trace metals, minerals in water

2. National Environmental Engineering Research Institute (NEERI), Nagpur
   Accreditation: NABL
   Scope: Comprehensive water quality (chemical, biological, physical)
   Phone: 0712-2249885 | neeri.res.in

3. Central Food Laboratory (CFL), Kolkata
   Scope: Packaged drinking water, mineral water (FSSAI + BIS)
   Phone: 033-22344992

4. BIS Lab, Chennai
   Address: CIT Campus, Taramani, Chennai 600113
   Scope: Food, beverages, water testing
   Phone: 044-22541568

5. Vimta Labs, Hyderabad
   Accreditation: NABL + BIS recognised
   Scope: Water, food, pharma testing
   Website: vimta.com | Phone: 040-27264141

6. SGS India Water Labs (Mumbai, Delhi, Bangalore)
   Scope: Physical, chemical, microbiological water parameters
   TAT: 7-14 working days

PARAMETERS TESTED FOR IS 14543 (Packaged Drinking Water):
Physical: Turbidity, colour, TDS, pH, temperature
Chemical: Fluoride, chloride, sulphate, nitrate, heavy metals (lead, arsenic, cadmium)
Microbiological: Total coliforms, E.coli, Pseudomonas aeruginosa
Additional: Barium, boron, selenium, cyanide

TYPICAL COSTS:
- Complete IS 10500 testing: ₹8,000 - ₹15,000
- Complete IS 14543 testing: ₹12,000 - ₹25,000 per batch
- Microbiological testing only: ₹2,000 - ₹5,000
- Turnaround: 7-21 days (microbiological takes longer)""",
            "metadata": {
                "standard_number": "BIS Recognised Labs — Water",
                "title": "Testing Labs for Drinking Water and Packaged Water Quality",
                "clause": "4.1-4.4",
                "section": "4",
                "page": 12,
                "industry": "testing_labs",
                "product": "water_quality",
                "document_type": "BIS Lab Directory",
                "language": "English",
            }
        },

        # ── CONSTRUCTION LABS ─────────────────────────────────────
        {
            "id": "lab_005",
            "content": """TESTING LABORATORIES — Construction Materials (Cement, Steel, Concrete)

FOR CEMENT (IS 269, IS 8112, IS 455) AND STEEL (IS 1786, IS 2062):

BIS RECOGNISED LABS FOR CONSTRUCTION MATERIALS:
1. National Council for Cement and Building Materials (NCB), Delhi/Ballabgarh
   Accreditation: NABL + BIS recognised
   Scope: All types of cement, concrete, admixtures
   Phone: 0129-2242120 | ncbindia.com
   TAT: 28 days (cement strength requires 28-day curing)

2. SERC (Structural Engineering Research Centre), Chennai
   Accreditation: NABL + CSIR
   Scope: Structural steel, concrete, construction materials
   Phone: 044-22541025 | serc.res.in

3. Central Building Research Institute (CBRI), Roorkee
   Accreditation: NABL
   Scope: Building materials, insulation, construction products
   Phone: 01332-272243 | cbri.res.in

4. NABL Accredited State Labs:
   - Maharashtra: Director of Industrial Safety & Health, Mumbai
   - Gujarat: Gujarat Council of Science & Technology, Gandhinagar
   - Tamil Nadu: Institute for Testing of Materials, Chennai

5. Bureau Veritas Materials Lab, Navi Mumbai
   Scope: Metals, construction materials, NDT
   Phone: 022-27693344

FOR TMT STEEL BARS (IS 1786):
Tests required: Chemical composition, tensile strength, yield strength, elongation, bend test, rebend test
Typical labs: NABL-accredited steel testing labs near steel mills
TAT: 5-10 working days (chemical + mechanical tests)

TYPICAL COSTS:
- Cement full IS 269 testing: ₹15,000 - ₹25,000 per lot
- Steel bars IS 1786 testing: ₹5,000 - ₹12,000 per lot
- Concrete cube testing (IS 456): ₹500 - ₹1,000 per cube
- Note: 28-day strength test adds 4 weeks minimum to timeline""",
            "metadata": {
                "standard_number": "BIS Recognised Labs — Construction",
                "title": "Testing Labs for Cement, Steel and Construction Materials",
                "clause": "5.1-5.4",
                "section": "5",
                "page": 16,
                "industry": "testing_labs",
                "product": "construction_materials",
                "document_type": "BIS Lab Directory",
                "language": "English",
            }
        },

        # ── AUTOMOTIVE LABS ───────────────────────────────────────
        {
            "id": "lab_006",
            "content": """TESTING LABORATORIES — Automotive Products

FOR AUTOMOTIVE PRODUCTS (IS 7079 Brake Systems, IS 17017 EV Charging, IS 14257 Batteries):

BIS RECOGNISED LABS FOR AUTOMOTIVE:
1. ARAI (Automotive Research Association of India), Pune
   Accreditation: NABL + BIS recognised
   Scope: Complete vehicle testing, components, EV systems, batteries
   Phone: 020-30231111 | araiindia.com
   TAT: 4-12 weeks depending on test type

2. NATRiP (National Automotive Testing R&D and Innovation Centre):
   - iCAT (International Centre for Automotive Technology), Manesar
     Phone: 0124-2892000 | icat.in
   - GARC (Global Automotive Research Centre), Chennai
     Phone: 044-67261000 | garc.in
   - NATRAX (National Automotive Test Track), Pithampur (MP)
   Scope: Vehicle certification, components, EV, safety

3. VRDE (Vehicle Research & Development Establishment), Ahmednagar
   Scope: Military and commercial vehicles, components
   Phone: 0241-2480265

4. SAG (Standard and Analytical Group), DRDO — Gurgaon
   Scope: Automotive batteries, fuel systems

FOR EV CHARGING STATIONS (IS 17017):
- ARAI Pune (comprehensive EV testing)
- CPRI Bangalore (electrical safety, EMC)
- TÜV Rheinland India, Gurgaon

FOR AUTOMOTIVE BATTERIES (IS 14257):
- ARAI Pune
- NEERI Nagpur (environmental testing)
- Central Electrochemical Research Institute (CECRI), Karaikudi

TYPICAL COSTS:
- Brake system IS 7079 testing: ₹30,000 - ₹80,000
- EV charging station IS 17017: ₹1,00,000 - ₹3,00,000
- Automotive battery: ₹50,000 - ₹1,50,000
- Helmet IS 4151: ₹5,000 - ₹15,000""",
            "metadata": {
                "standard_number": "BIS Recognised Labs — Automotive",
                "title": "Testing Labs for Automotive, EV and Vehicle Components",
                "clause": "6.1-6.4",
                "section": "6",
                "page": 20,
                "industry": "testing_labs",
                "product": "automotive",
                "document_type": "BIS Lab Directory",
                "language": "English",
            }
        },

        # ── TEXTILE LABS ──────────────────────────────────────────
        {
            "id": "lab_007",
            "content": """TESTING LABORATORIES — Textiles and Apparel

FOR TEXTILES (IS 1346 Cotton Fabrics, IS 9070 Polyester, IS 4249 Woollen):

BIS RECOGNISED LABS FOR TEXTILES:
1. SITRA (South India Textile Research Association), Coimbatore
   Accreditation: NABL + BIS recognised
   Scope: All textile testing — yarn, fabric, garments, technical textiles
   Phone: 0422-2574367 | sitra.in
   TAT: 2-3 weeks

2. ATIRA (Ahmedabad Textile Industry's Research Association), Ahmedabad
   Accreditation: NABL
   Scope: Cotton, synthetic, blended textiles, colour fastness
   Phone: 079-26304161 | atiraindia.com

3. WRA (Wool Research Association), Mumbai/Thane
   Accreditation: NABL
   Scope: Woollen textiles, carpets, technical wool products
   Phone: 022-25404134 | woolresearch.com

4. BTRA (Bombay Textile Research Association), Mumbai
   Scope: Composite textiles, performance fabrics, industrial textiles
   Phone: 022-25402612 | btraindia.com

5. Bureau Veritas Textile Lab, Gurgaon
   Scope: Physical, chemical, colorfastness, consumer safety
   Website: bureauveritas.com/textile-testing

TESTS FOR COTTON FABRIC (IS 1346):
- Thread count (ends/cm × picks/cm)
- Fabric weight (GSM)
- Tensile strength (warp and weft)
- Tear strength
- Dimensional stability after washing
- Colour fastness (if dyed)
- Fibre composition

TYPICAL COSTS:
- Complete IS 1346 cotton fabric testing: ₹3,000 - ₹8,000 per sample
- Colour fastness tests: ₹500 - ₹2,000 per test
- Flammability testing: ₹2,000 - ₹5,000
- Export compliance bundle: ₹10,000 - ₹20,000
- TAT: 7-14 working days""",
            "metadata": {
                "standard_number": "BIS Recognised Labs — Textiles",
                "title": "Testing Labs for Textiles, Fabrics and Apparel",
                "clause": "7.1-7.4",
                "section": "7",
                "page": 24,
                "industry": "testing_labs",
                "product": "textiles",
                "document_type": "BIS Lab Directory",
                "language": "English",
            }
        },

        # ── BIS OWN LABS ──────────────────────────────────────────
        {
            "id": "lab_008",
            "content": """BIS CENTRAL LABORATORIES — Official BIS Testing Facilities

BIS OPERATES 5 CENTRAL LABORATORIES across India:

1. BIS CENTRAL LABORATORY — SAHIBABAD (Uttar Pradesh)
   Address: Plot 4, Site-IV, Sahibabad Industrial Area, Ghaziabad 201010
   Phone: 0120-2770151
   Scope: Electronics, electrical, mechanical, chemical, food
   Primary: North India reference lab

2. BIS LABORATORY — MUMBAI (Western Region)
   Address: Manakalaya, BKC, Bandra (East), Mumbai 400051
   Phone: 022-26590295
   Scope: Electronics, metals, building materials, food, chemicals

3. BIS LABORATORY — KOLKATA (Eastern Region)
   Address: P-7, C.I.T. Scheme VIIM, Kankurgachi, Kolkata 700054
   Phone: 033-23378627
   Scope: Jute, textiles, chemicals, general mechanical testing

4. BIS LABORATORY — CHENNAI (Southern Region)
   Address: C.I.T. Campus, Taramani, Chennai 600113
   Phone: 044-22541568
   Scope: Food, chemicals, leather, general testing

5. BIS LABORATORY — CHANDIGARH (Northern Region)
   Address: SCO 70-71, Sector 34-A, Chandigarh 160022
   Phone: 0172-2614000
   Scope: Wool, textiles, mechanical, general testing

SERVICES OFFERED BY BIS LABS:
- Product testing for BIS certification
- Calibration of instruments (NABL accredited)
- Training courses on testing methods
- Proficiency testing programmes
- Research and development support

HOW TO BOOK BIS LAB:
1. Visit bis.gov.in → Laboratory Services → Online Booking
2. Or contact the nearest BIS branch office
3. Tests scheduled on first-come-first-served basis
4. Payment via NEFT/RTGS or demand draft

BIS LAB ADVANTAGE:
- Test results directly accepted for BIS certification (no question of lab recognition)
- Government rates (typically lower than private labs)
- Official NABL accreditation for most test parameters""",
            "metadata": {
                "standard_number": "BIS Central Laboratories",
                "title": "BIS Own Central Laboratories — Locations, Scope and Booking",
                "clause": "8.1-8.4",
                "section": "8",
                "page": 28,
                "industry": "testing_labs",
                "product": "all_products",
                "document_type": "BIS Lab Directory",
                "language": "English",
            }
        },
    ]

    # ─────────────────────────────────────────────────────────────
    # LOAD INTO CHROMADB
    # ─────────────────────────────────────────────────────────────
    existing = set(collection.get(ids=[c["id"] for c in lab_chunks])["ids"])
    new_chunks = [c for c in lab_chunks if c["id"] not in existing]

    if not new_chunks:
        print("⚠️  All lab chunks already present — nothing to add.")
    else:
        collection.add(
            documents=[c["content"]  for c in new_chunks],
            metadatas=[c["metadata"] for c in new_chunks],
            ids      =[c["id"]       for c in new_chunks],
        )
        print(f"\n✅  Added {len(new_chunks)} NABL lab chunks to ChromaDB")

    total = collection.count()
    print(f"\n📊  Total chunks in ChromaDB now: {total}")
    return new_chunks


if __name__ == "__main__":
    add_data()
    print("\n🎉  Done!  Try these queries now:")
    print("   • 'Which lab can test LED lamps for BIS certification?'")
    print("   • 'Where can I get cement tested for IS 269?'")
    print("   • 'Which labs test medical devices in India?'")
    print("   • 'Testing laboratory for packaged drinking water'")
    print("   • 'Cost of BIS certification testing for LED bulbs'")
    print("   • 'NABL accredited labs for automotive testing'")
    print("   • 'BIS lab in Mumbai — what tests do they do?'")
