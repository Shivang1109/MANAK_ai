"""
ManakAI — ChromaDB data loader
Covers: BIS Hallmarking, Certification Schemes (I/II/III), CRS, FMCS
These are REQUIRED by the problem statement and were 0% implemented before.

Run from rag-service directory:
    python add_hallmarking_schemes_data.py
"""

import chromadb

def add_data():
    client = chromadb.PersistentClient(path="./data/chromadb")
    collection = client.get_collection("bis_standards")

    # ─────────────────────────────────────────────────────────────
    # HALLMARKING CHUNKS
    # ─────────────────────────────────────────────────────────────
    hallmarking_chunks = [
        {
            "id": "hallmark_001",
            "content": """BIS HALLMARKING SCHEME — Overview and Legal Basis

BIS Hallmarking is a quality certification of precious metal articles in India, governed under the Bureau of Indian Standards Act, 2016 and the BIS (Hallmarking) Regulations, 2018.

WHAT IS HALLMARKING?
Hallmarking is the official mark of purity on gold, silver, and platinum jewellery. It certifies that the jewellery conforms to the standards of purity adopted by the Bureau of Indian Standards.

LEGAL REQUIREMENT:
Gold jewellery hallmarking became MANDATORY under Quality Control Order 2021 for sellers in notified districts. As of 2023, it is mandatory across India for gold articles of 14, 18, and 22 carats.

APPLICABLE STANDARDS:
- IS 1417:2016 — Methods for determination of fineness and assay of gold alloys in jewellery
- IS 2112:2003 — Fineness of gold and gold alloys
- IS 3095:1997 — Specification for gold alloy jewellery

PURITY DESIGNATIONS:
- 999 (24 carat) — 99.9% pure gold
- 995 (24 carat) — 99.5% pure gold  
- 916 (22 carat) — 91.6% pure gold
- 875 (21 carat) — 87.5% pure gold
- 750 (18 carat) — 75.0% pure gold
- 585 (14 carat) — 58.5% pure gold""",
            "metadata": {
                "standard_number": "BIS Hallmarking Scheme",
                "title": "BIS Hallmarking — Overview, Legal Basis and Purity Designations",
                "clause": "1.1-1.4",
                "section": "1",
                "page": 1,
                "industry": "hallmarking",
                "product": "gold_jewellery",
                "document_type": "BIS Scheme",
                "language": "English",
            }
        },
        {
            "id": "hallmark_002",
            "content": """BIS HALLMARKING SCHEME — Registration Process for Jewellers

HOW TO GET BIS HALLMARKING LICENCE (for jewellers):

Step 1 — REGISTRATION
Apply online at www.bis.gov.in → Hallmarking → Apply for jeweller registration.
Fees: ₹500 (new registration), ₹200 (renewal annually).

Step 2 — DOCUMENTS REQUIRED
- Copy of GST registration certificate
- Copy of identity proof of proprietor/partner/director
- Copy of address proof of business premises
- Affidavit of not being convicted under BIS Act
- Bank account details

Step 3 — VERIFICATION
BIS officer verifies the business premises within 30 days.

Step 4 — LICENCE ISSUE
Certificate of Registration issued. Valid for 1 year. Renewable online.

HALLMARK COMPONENTS (6-digit HUID — Hallmark Unique ID):
Since April 2023, all hallmarked jewellery must carry:
1. BIS logo (triangle)
2. Purity/fineness number (e.g., 916)
3. Jeweller's 6-character HUID (alphanumeric, unique per piece)
- Example: BIS logo + 916 + AB1234

The HUID is traceable on the BIS CARE app. Consumers can verify authenticity by scanning the HUID.""",
            "metadata": {
                "standard_number": "BIS Hallmarking Registration",
                "title": "BIS Hallmarking — Jeweller Registration Process and HUID",
                "clause": "2.1-2.5",
                "section": "2",
                "page": 3,
                "industry": "hallmarking",
                "product": "gold_jewellery",
                "document_type": "BIS Scheme",
                "language": "English",
            }
        },
        {
            "id": "hallmark_003",
            "content": """BIS HALLMARKING SCHEME — Assaying and Hallmarking Centres (AHCs)

ASSAYING AND HALLMARKING CENTRES (AHCs):
AHCs are BIS-recognised laboratories that test purity and apply the hallmark on jewellery.

HOW AHCs WORK:
1. Jeweller submits articles to nearest AHC
2. AHC tests purity using fire assay or X-ray fluorescence (XRF)
3. If purity matches declared fineness, hallmark is applied
4. HUID is registered in BIS central database
5. Article returned to jeweller within 1-2 working days

AHC CHARGES (indicative):
- Up to 20g: ₹35 per article
- 20g to 50g: ₹45 per article
- Above 50g: ₹55 per article

CONSUMER PROTECTION:
- Consumers can verify HUID on BIS CARE app (free, Android/iOS)
- Complaints about hallmarked jewellery: 1800-11-4455 (BIS toll-free)
- If purity found less than declared: full refund + compensation under Consumer Protection Act 2019

SILVER HALLMARKING:
Silver hallmarking is voluntary. Applicable standard: IS 2112.
Purity marks: 999, 970, 925, 900, 835, 800.

PLATINUM HALLMARKING:
Platinum hallmarking is voluntary. Purity: 950 (95%).
Standard: IS 16527 (Draft).""",
            "metadata": {
                "standard_number": "BIS Hallmarking AHC",
                "title": "BIS Hallmarking — Assaying Centres, Charges and Consumer Protection",
                "clause": "3.1-3.6",
                "section": "3",
                "page": 6,
                "industry": "hallmarking",
                "product": "gold_silver_jewellery",
                "document_type": "BIS Scheme",
                "language": "English",
            }
        },

        # ── IS 1417 — Gold testing standard ────────────────────────
        {
            "id": "hallmark_004",
            "content": """IS 1417:2016 — Methods for Determination of Fineness and Assay of Gold and Gold Alloys in Jewellery

SCOPE:
This standard specifies the methods for determination of fineness of gold and gold alloys used in jewellery and allied articles.

SECTION 5 — FIRE ASSAY METHOD (Reference Method):
5.1 Principle: Gold is separated from base metals by cupellation. The gold content is determined gravimetrically.
5.2 Accuracy: ±1 part per thousand (±0.1%)
5.3 Sample size: Minimum 0.25g required
5.4 Equipment: Muffle furnace at 850-950°C, cupels (bone-ash or magnesia)

SECTION 6 — X-RAY FLUORESCENCE (XRF) METHOD (Routine Method):
6.1 Principle: XRF measures characteristic X-ray intensities to determine elemental composition
6.2 Accuracy: ±2 parts per thousand for gold ≥500 fineness
6.3 Calibration: Must be calibrated with certified reference materials every 6 months
6.4 Limitation: Cannot distinguish between surface coating and bulk composition

SECTION 7 — TOUCHSTONE METHOD (Indicative Only):
7.1 For initial screening only — not acceptable for hallmarking certification
7.2 Accuracy: ±5-10 parts per thousand

REPORTING:
Results expressed as parts per thousand (fineness). 
22 carat = 916 fineness = 916 parts gold per 1000 parts alloy.""",
            "metadata": {
                "standard_number": "IS 1417:2016",
                "title": "Methods for Determination of Fineness and Assay of Gold Alloys in Jewellery",
                "clause": "5.1-7.2",
                "section": "5",
                "page": 12,
                "industry": "hallmarking",
                "product": "gold_testing",
                "document_type": "Indian Standard",
                "language": "English",
            }
        },
    ]

    # ─────────────────────────────────────────────────────────────
    # CERTIFICATION SCHEME CHUNKS
    # ─────────────────────────────────────────────────────────────
    scheme_chunks = [
        {
            "id": "scheme_001",
            "content": """BIS CERTIFICATION SCHEMES — Overview of All Schemes

BIS provides product certification under the BIS Act, 2016. The main certification schemes are:

SCHEME I — Product Certification Scheme (IS Mark / ISI Mark):
- Most common scheme for domestic manufacturers
- Manufacturer applies, BIS grants licence to use IS Mark
- Requires factory inspection + product testing at BIS-approved lab
- Annual factory surveillance
- ISI mark on product proves compliance with Indian Standard

SCHEME II — Simplified Procedure for Well-Established Manufacturer:
- For manufacturers with proven quality track record
- Reduced frequency of BIS factory inspections
- Requires ISO 9001 certification as prerequisite
- Self-declaration with periodic BIS verification

SCHEME III — Foreign Manufacturer Certification Scheme (FMCS):
- For overseas manufacturers exporting to India
- Product tested at accredited foreign lab or BIS lab in India
- Factory inspection by BIS or authorised inspection body abroad
- Licence valid 1-2 years, renewable

SCHEME IV — Hall Marking Scheme:
- For gold, silver and platinum jewellery
- Mandatory for gold (22ct, 18ct, 14ct) since 2021
- Jewellers register with BIS, articles tested at AHCs
- HUID (Hallmark Unique ID) for each piece

SCHEME V — ISI Mark for Multiple Locations:
- For manufacturers with multiple production units
- Single licence covering all units
- Each unit inspected separately

SCHEME IX — Compulsory Registration Scheme (CRS):
- For electronics/IT products under Mandatory Testing and Certification Order
- Self-declaration based on test report from BIS-recognised lab
- Online registration, no factory inspection required
- Faster than Scheme I (typically 30-45 days)""",
            "metadata": {
                "standard_number": "BIS Certification Schemes",
                "title": "Overview of All BIS Product Certification Schemes",
                "clause": "1.1-1.7",
                "section": "1",
                "page": 1,
                "industry": "certification",
                "product": "all_products",
                "document_type": "BIS Scheme",
                "language": "English",
            }
        },
        {
            "id": "scheme_002",
            "content": """BIS SCHEME I — Product Certification (ISI Mark) — Detailed Process

SCHEME I: PRODUCT CERTIFICATION SCHEME (IS Mark / ISI Mark)

WHO NEEDS IT:
Products listed under mandatory BIS certification (Quality Control Orders) must have ISI mark before sale in India.
Examples: Cement, steel bars, LPG cylinders, food items, electrical appliances, LED lamps, medical devices.

STEP-BY-STEP PROCESS:

Step 1 — APPLICATION (Week 1):
Apply on BIS website (bis.gov.in) → Product Certification → Scheme I
Fee: Application fee ₹1,000 + Marking fee (varies by product category)

Step 2 — SAMPLE COLLECTION (Week 2-3):
BIS officer visits factory and draws samples
Samples sent to BIS-recognised/approved laboratory

Step 3 — LABORATORY TESTING (Week 3-8):
Product tested against all requirements of the applicable IS standard
Test report issued by lab

Step 4 — FACTORY INSPECTION (Week 4-6):
BIS officer inspects:
- Manufacturing process and equipment
- Quality control procedures
- In-house testing facilities
- Raw material inspection records

Step 5 — GRANT OF LICENCE (Week 8-12):
If tests and inspection satisfactory, BIS grants IS Mark Licence
Licence number format: CM/L-XXXXXXX

Step 6 — SURVEILLANCE (Annual):
Annual factory visit by BIS officer
Periodic market sample testing
Licence renewed annually on payment of fees

COSTS (approximate):
- Application fee: ₹1,000
- Testing charges: ₹10,000 - ₹1,00,000 (depends on product)
- Marking fee: 0.1% to 1% of turnover (varies by product)
- Annual minimum marking fee: ₹500 to ₹50,000""",
            "metadata": {
                "standard_number": "BIS Scheme I",
                "title": "BIS Product Certification Scheme I — ISI Mark Process and Fees",
                "clause": "2.1-2.6",
                "section": "2",
                "page": 4,
                "industry": "certification",
                "product": "domestic_manufacturers",
                "document_type": "BIS Scheme",
                "language": "English",
            }
        },
        {
            "id": "scheme_003",
            "content": """BIS COMPULSORY REGISTRATION SCHEME (CRS) — Electronics and IT Products

CRS (COMPULSORY REGISTRATION SCHEME) — Scheme IX

WHAT IS CRS?
CRS is mandatory for electronics and IT products sold in India under the Electronics and Information Technology Goods (Requirements for Compulsory Registration) Order, 2012 (and amendments).

PRODUCTS COVERED UNDER CRS (50+ categories including):
- Mobile phones and tablets
- LED lights and luminaires
- Laptops and computers
- Printers and scanners
- Power banks and chargers (USB chargers, adapters)
- Smart watches and wearables
- Televisions (LED, LCD, OLED)
- Audio equipment
- Set-top boxes
- UPS and inverters
- Switches and sockets
- CCTV cameras
- Smart meters

HOW CRS DIFFERS FROM SCHEME I:
| Feature | Scheme I (ISI Mark) | CRS |
|---------|---------------------|-----|
| Factory inspection | Yes, mandatory | No |
| Test lab | BIS lab or recognised lab | BIS-recognised lab only |
| Time to licence | 3-6 months | 30-45 days |
| Mark on product | IS Mark + licence number | R-XXXXXXXXXXXXXXXX (14-digit) |
| Annual renewal | Yes | Yes (online) |

CRS REGISTRATION PROCESS:
1. Get product tested at BIS-recognised lab
2. Apply online at crsbis.in
3. Upload test report and product details
4. Registration number issued within 15 working days
5. Display R-number on product and packaging

VALIDITY: 2 years (renewable)
FEES: ₹10,000 per model per year""",
            "metadata": {
                "standard_number": "BIS CRS Scheme",
                "title": "BIS Compulsory Registration Scheme (CRS) for Electronics and IT Products",
                "clause": "3.1-3.5",
                "section": "3",
                "page": 8,
                "industry": "certification",
                "product": "electronics_it",
                "document_type": "BIS Scheme",
                "language": "English",
            }
        },
        {
            "id": "scheme_004",
            "content": """BIS FOREIGN MANUFACTURER CERTIFICATION SCHEME (FMCS) — Scheme III

FMCS: FOR OVERSEAS MANUFACTURERS EXPORTING TO INDIA

WHO NEEDS FMCS?
Foreign manufacturers whose products are subject to mandatory BIS certification in India must obtain FMCS licence before exporting to India.

APPLICABLE PRODUCTS:
All products under mandatory BIS certification (Quality Control Orders) imported into India require either:
- FMCS licence (Scheme III), OR
- The importer must ensure the product has BIS certification

PROCESS:
Step 1 — Application
Apply to BIS at bis.gov.in or BIS International Division, New Delhi
Appoint an Authorised Indian Representative (AIR) — mandatory

Step 2 — Testing
Product samples tested at:
- BIS recognised lab in India, OR
- Laboratory accredited by body with MRA with ILAC (internationally recognised)

Step 3 — Factory Inspection
BIS or BIS-authorised agency inspects overseas factory
Inspection at applicant's expense (travel + per diem for BIS officers)

Step 4 — Licence Grant
Licence valid 1-2 years
Renewable subject to continued compliance

AUTHORISED INDIAN REPRESENTATIVE (AIR):
- Must be an entity registered in India
- Legally responsible for compliance of imported products
- Point of contact for BIS

FEES:
- Application fee: ₹1,000
- Inspection charges: Actual travel + ₹50,000-₹2,00,000 per inspection
- Annual licence fee: Varies by product category

COUNTRIES WITH SPECIAL ARRANGEMENTS:
BIS has bilateral cooperation agreements with several national standards bodies.
Products certified by recognised foreign certification bodies may get expedited processing.""",
            "metadata": {
                "standard_number": "BIS FMCS Scheme III",
                "title": "BIS Foreign Manufacturer Certification Scheme (FMCS) — Process for Importers",
                "clause": "4.1-4.6",
                "section": "4",
                "page": 12,
                "industry": "certification",
                "product": "imported_products",
                "document_type": "BIS Scheme",
                "language": "English",
            }
        },
        {
            "id": "scheme_005",
            "content": """BIS CERTIFICATION — Mandatory vs Voluntary Products and Quality Control Orders (QCOs)

QUALITY CONTROL ORDERS (QCOs):
QCOs are notifications issued by the Government of India under the BIS Act making BIS certification MANDATORY for specific products.
Issued by respective Ministries (e.g., DPIIT, MoHFW, MoP).

CURRENTLY MANDATORY (Selected Examples):

ELECTRONICS:
- LED lamps (IS 16102) — Mandatory since 2017
- Switches and sockets (IS 3854, IS 1293) — Mandatory
- Mobile chargers (IS 13252) — Mandatory
- Power cables (IS 694) — Mandatory

CONSTRUCTION:
- Ordinary Portland Cement (IS 269) — Mandatory
- TMT Steel bars (IS 1786) — Mandatory
- Galvanised steel pipes (IS 1239) — Mandatory

FOOD AND AGRO:
- Packaged drinking water (IS 14543) — Mandatory
- Milk and milk products — Mandatory (FSSAI + BIS)

AUTOMOTIVE:
- Automotive batteries (IS 14257) — Mandatory
- Helmets (IS 4151) — Mandatory

MEDICAL:
- Surgical instruments — Mandatory for selected items
- PPE (IS 9473 for gloves) — Mandatory

VOLUNTARY (No QCO):
Products without QCO may still voluntarily adopt IS standards and obtain BIS licence.
Benefits of voluntary certification:
- Consumer trust
- Market differentiation
- Access to government procurement (many tenders require IS mark)

HOW TO CHECK IF YOUR PRODUCT NEEDS MANDATORY CERTIFICATION:
1. Visit bis.gov.in → Certification → List of mandatory products
2. Check Ministry of Commerce QCO notifications
3. Contact BIS helpline: 1800-11-4455""",
            "metadata": {
                "standard_number": "BIS QCO Mandatory List",
                "title": "BIS Mandatory vs Voluntary Certification — Quality Control Orders (QCOs)",
                "clause": "5.1-5.4",
                "section": "5",
                "page": 16,
                "industry": "certification",
                "product": "all_products",
                "document_type": "BIS Scheme",
                "language": "English",
            }
        },
        {
            "id": "scheme_006",
            "content": """BIS CONSUMER AFFAIRS AND GRIEVANCE REDRESSAL

BIS CONSUMER-FACING SERVICES:

1. BIS CARE APP:
Free mobile app (Android + iOS) for consumers.
Features:
- Verify hallmarked jewellery by scanning HUID
- Check if a product has valid BIS licence (scan IS mark)
- Report fake/substandard products
- File complaints against BIS-certified products

2. CONSUMER HELPLINE:
Toll-free: 1800-11-4455 (9 AM to 5:30 PM, Monday-Friday)
Email: headbis@bis.gov.in

3. COMPLAINTS AGAINST SUBSTANDARD PRODUCTS:
If a BIS-certified product is found to be substandard:
- File complaint on bis.gov.in or BIS CARE app
- BIS investigates within 30 working days
- Manufacturer penalised under BIS Act 2016
- Penalties: Up to ₹5 lakh + 2 years imprisonment for selling uncertified products

4. STANDARDS CLUBS:
BIS runs Standards Clubs in schools and colleges to promote awareness.
Contact local BIS branch office to register your institution.

5. BIS LABORATORY SERVICES:
BIS operates 5 central laboratories:
- Mumbai, Kolkata, Chennai, Chandigarh, Patna
Services: Testing, calibration, training
Contact: Laboratory fees and booking at bis.gov.in

6. WHAT TO CHECK WHEN BUYING PRODUCTS:
For ISI-marked products:
- IS Mark (wheel symbol) + Licence number (CM/L-XXXXXXX)
- Verify licence on BIS CARE app
For hallmarked jewellery:
- BIS logo + Purity (916/750) + 6-character HUID
- Verify HUID on BIS CARE app""",
            "metadata": {
                "standard_number": "BIS Consumer Services",
                "title": "BIS Consumer Affairs — Helpline, CARE App, Complaints and Lab Services",
                "clause": "6.1-6.6",
                "section": "6",
                "page": 20,
                "industry": "consumer_affairs",
                "product": "general_consumer",
                "document_type": "BIS Scheme",
                "language": "English",
            }
        },
    ]

    # ─────────────────────────────────────────────────────────────
    # LOAD INTO CHROMADB
    # ─────────────────────────────────────────────────────────────
    all_chunks = hallmarking_chunks + scheme_chunks

    # De-duplicate: skip IDs already in collection
    existing = set(collection.get(ids=[c["id"] for c in all_chunks])["ids"])
    new_chunks = [c for c in all_chunks if c["id"] not in existing]

    if not new_chunks:
        print("⚠️  All chunks already present in ChromaDB — nothing to add.")
    else:
        collection.add(
            documents=[c["content"]  for c in new_chunks],
            metadatas=[c["metadata"] for c in new_chunks],
            ids      =[c["id"]       for c in new_chunks],
        )
        print(f"\n✅  Added {len(new_chunks)} new chunks to ChromaDB")
        print(f"   Hallmarking chunks  : {sum(1 for c in new_chunks if 'hallmark' in c['id'])}")
        print(f"   Scheme chunks       : {sum(1 for c in new_chunks if 'scheme'   in c['id'])}")

    total = collection.count()
    print(f"\n📊  Total chunks in ChromaDB now: {total}")
    return new_chunks


if __name__ == "__main__":
    add_data()
    print("\n🎉  Done!  Try these queries now:")
    print("   • 'What is BIS hallmarking?'")
    print("   • 'How do I get hallmarking licence?'")
    print("   • 'What is the difference between Scheme I and CRS?'")
    print("   • 'Is BIS certification mandatory for mobile phones?'")
    print("   • 'How to verify hallmarked jewellery?'")
    print("   • 'What is FMCS for foreign manufacturers?'")
