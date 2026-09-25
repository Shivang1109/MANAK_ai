# 🚀 ManakAI - Next Level Action Plan (Post-Internal Selection)

**Status:** ✅ Internal Round CLEARED!  
**Next:** National SIH Finals Preparation  
**Timeline:** 2-4 weeks intensive prep

---

## 🎯 **PHASE 1: STRENGTHEN CORE (Week 1)**

### **Priority 1: Fix Critical Bugs** ⚡ URGENT

#### 1. Registration Issue
**Status:** Some registrations failing  
**Action:**
```bash
# Debug and fix frontend-backend connection
# Ensure consistent port (5173 or 3000)
# Test registration flow 10 times
```

**Owner:** Frontend Lead  
**Deadline:** 2 days

---

#### 2. "Why This Answer?" Enhancement
**Current:** Button exists but needs improvement  
**Action:**
- Add relevance scores to backend response
- Show "92% match" badges in evidence panel
- Add "View in BIS Portal" links if possible

**Files to modify:**
- `backend-api/src/main/java/com/manakai/services/ChatService.java`
- `rag-service/main.py` (add similarity scores to response)
- `frontend/src/components/EvidenceDossier.tsx` (already updated)

**Owner:** Backend + RAG Lead  
**Deadline:** 3 days

---

#### 3. Response Time Optimization
**Current:** 2-3 seconds  
**Target:** <2 seconds consistently

**Actions:**
- Cache frequent queries
- Optimize ChromaDB retrieval (reduce top_k if needed)
- Use connection pooling for database
- Preload embedding model on startup

**Owner:** RAG Lead  
**Deadline:** 4 days

---

### **Priority 2: Improve Data Quality** 📊

#### 4. Add More High-Quality Standards
**Current:** 30 standards, 4,029 chunks  
**Target:** 50 standards, 8,000+ chunks

**Focus Industries:**
- ✅ LED/Lighting (already strong)
- ✅ Medical Equipment (already strong)
- 🔄 **Add:** Consumer Electronics (phones, chargers, adapters)
- 🔄 **Add:** Food Safety (packaged foods, dairy, beverages)
- 🔄 **Add:** Textiles & Apparel (fabrics, garments)

**Why:** Show broader applicability

**Action:**
```bash
# Find 20 more high-priority BIS standards
# Convert to CSV format
# Load into ChromaDB
cd /Users/shivangpathak/SIH-2026/rag-service
python scripts/load_csvs.py
```

**Owner:** Data Team  
**Deadline:** 5 days

---

#### 5. Enrich Metadata
**Current:** Basic metadata  
**Target:** Rich metadata for better citations

**Add to each chunk:**
```json
{
  "standard_number": "IS 16102:2012",
  "title": "LED Lamps - Safety Requirements",
  "section": "5",
  "clause": "5.2",
  "page": 14,
  "industry": "electronics",
  "document_type": "Indian Standard",
  "revision_date": "2012",
  "supersedes": "IS 16102:2008" // if applicable
}
```

**Owner:** Data + RAG Lead  
**Deadline:** 4 days

---

### **Priority 3: Create Golden Test Dataset** 🧪

#### 6. Build 100-Question Evaluation Set
**Current:** Have questions in DEMO_QUESTIONS.md  
**Need:** Structured test suite with expected answers

**Create:** `/rag-service/evaluation/golden_dataset.json`

```json
[
  {
    "id": "Q001",
    "question": "What are LED lamp safety requirements?",
    "expected_standard": "IS 16102:2012",
    "expected_clause": "5.2",
    "expected_keywords": ["safety", "electrical insulation", "voltage"],
    "domain": "electronics",
    "difficulty": "easy"
  },
  // ... 99 more
]
```

**Categories:**
- Easy (50 questions): Single standard, clear answer
- Medium (30 questions): Multiple sources needed
- Hard (20 questions): Ambiguous or edge cases

**Owner:** Full Team (divide by domain)  
**Deadline:** 1 week

---

#### 7. Run Automated Evaluation
**Create:** `/rag-service/evaluation/evaluate.py`

**Metrics to measure:**
- Retrieval Recall@K (did we find the right standard?)
- Citation Accuracy (is IS number + clause correct?)
- Answer Groundedness (is answer supported by evidence?)
- Latency (response time)
- Abstention Accuracy (did we correctly say "don't know"?)

**Output:** Evaluation report showing 91%+ scores

**Owner:** ML/RAG Lead  
**Deadline:** 1 week (after golden dataset ready)

---

## 🎯 **PHASE 2: ADD DIFFERENTIATING FEATURES (Week 2)**

### **Priority 4: Build Admin Analytics Dashboard** 📊

#### 8. Enhanced Admin Panel
**Current:** Basic admin view  
**Target:** Impressive analytics for judges

**Add These Views:**

**A. Query Analytics:**
- Top 10 most-asked questions
- Query volume by industry
- Average response time trends
- Success rate (thumbs up/down ratio)

**B. Coverage Gaps:**
- Questions with no good answers (low confidence)
- Industries with few queries
- Standards with no queries (unused data)

**C. User Behavior:**
- New users per day
- Returning users rate
- Average queries per user
- Feedback submission rate

**D. System Health:**
- Service uptime
- Error rates
- Database size
- ChromaDB collection stats

**Tech Stack:**
- Use Chart.js or Recharts for visualizations
- Real-time updates via WebSocket (optional, nice-to-have)
- Export reports as PDF

**Owner:** Frontend + Backend Lead  
**Deadline:** 1 week

---

### **Priority 5: Certification Pathway Feature** 🗺️

#### 9. "How to Get Certified" Guide
**New Feature:** After answering a question, show step-by-step certification process

**Example Flow:**
```
User: "Is BIS certification mandatory for LED bulbs?"

Answer: "Yes, IS 16102:2012 applies..."

[NEW] 📋 Certification Pathway:
Step 1: Determine applicable standard (✅ IS 16102:2012)
Step 2: Apply to BIS (Form BIS-01)
Step 3: Get product tested at NABL lab
Step 4: Submit test reports
Step 5: BIS factory inspection
Step 6: License issued (ISI mark)

Estimated Time: 3-6 months
Estimated Cost: ₹50,000 - ₹2,00,000

[Button] Find NABL Labs Near You
[Button] Download Application Forms
```

**Data Source:** Manually create certification workflows for top 10 industries

**Owner:** Research Team + Frontend  
**Deadline:** 1 week

---

### **Priority 6: Comparison Feature** 🔍

#### 10. "Compare Standards" Functionality
**Use Case:** User wants to compare IS 16102 (LED safety) vs IS 16103 (LED performance)

**New UI Component:**
```tsx
// frontend/src/components/CompareStandards.tsx

[Card 1: IS 16102:2012]
Focus: Safety
Key Requirements: Insulation, voltage limits
Mandatory: Yes

[Card 2: IS 16103:2012]
Focus: Performance
Key Requirements: Luminous efficacy, CRI
Mandatory: No (voluntary)

[Side-by-side table showing differences]
```

**Backend Endpoint:** `/api/compare?standards=IS16102,IS16103`

**Owner:** Full Stack Dev  
**Deadline:** 1 week

---

## 🎯 **PHASE 3: POLISH & PROFESSIONALIZE (Week 3)**

### **Priority 7: UI/UX Refinement** 🎨

#### 11. Design Improvements
**Current:** Functional but basic  
**Target:** Polished, professional

**Actions:**
- Add loading skeletons (not just spinners)
- Smooth animations for evidence panel
- Empty states with helpful suggestions
- Error states with recovery actions
- Tooltips for new users
- Tour/walkthrough on first visit
- Dark mode (optional, nice-to-have)

**Tools:**
- Framer Motion for animations
- React Joyride for tour
- Tailwind refinements

**Owner:** Frontend Lead  
**Deadline:** 1 week

---

#### 12. Mobile Responsiveness
**Current:** Works on desktop  
**Target:** Perfect on mobile too

**Test on:**
- iPhone (Safari)
- Android (Chrome)
- Tablet (iPad)

**Ensure:**
- Evidence panel works on small screens
- Chat input easy to type on mobile
- Citations readable on 5-inch screen

**Owner:** Frontend Lead  
**Deadline:** 3 days

---

### **Priority 8: Documentation & Explainers** 📚

#### 13. User Guide / Help Section
**Add:** `/help` route with FAQs

**Content:**
- How to ask good questions
- Understanding confidence scores
- How to verify citations
- What to do if answer is wrong
- Privacy & data usage
- Limitations & disclaimers

**Owner:** Content Writer + Frontend  
**Deadline:** 3 days

---

#### 14. Video Demo (For Backup)
**Create:** 2-minute video showing:
1. Problem statement (15 sec)
2. Live demo of 3 queries (90 sec)
3. Admin analytics (15 sec)

**Tool:** Loom or QuickTime screen recording

**Purpose:** Backup if live demo fails during presentation

**Owner:** Presentation Lead  
**Deadline:** 4 days

---

### **Priority 9: Security & Compliance** 🔒

#### 15. Security Hardening
**Actions:**
- ✅ HTTPS in production (Let's Encrypt)
- ✅ SQL injection prevention (use parameterized queries)
- ✅ XSS prevention (sanitize inputs)
- ✅ Rate limiting (prevent abuse)
- ✅ Password hashing (already using bcrypt?)
- ✅ JWT expiration handling
- ✅ CORS properly configured
- ✅ Environment variables secured (.env not in git)

**Run:** Security checklist audit

**Owner:** Backend Lead  
**Deadline:** 2 days

---

#### 16. Legal Disclaimers
**Add to every page footer:**
> "ManakAI provides informational assistance only and is not affiliated with the Bureau of Indian Standards (BIS). Always verify information with official BIS documents before making compliance decisions. Not a substitute for professional legal or regulatory advice."

**Add:** Terms of Service, Privacy Policy (basic templates)

**Owner:** Legal/Content Writer  
**Deadline:** 2 days

---

## 🎯 **PHASE 4: DEMO PREPARATION (Week 4)**

### **Priority 10: Perfect Demo Execution** 🎬

#### 17. Create 5-Minute Demo Script (Refined)
**Structure:**
1. **Hook (15 sec):** Problem statement
2. **Query 1 (60 sec):** LED safety (show citations)
3. **Query 2 (30 sec):** ECG testing (different domain)
4. **Query 3 (30 sec):** Flying cars (safe abstention)
5. **Feature (30 sec):** Click "Why this answer?"
6. **Analytics (30 sec):** Show admin dashboard
7. **Metrics (30 sec):** Show evaluation scores
8. **Closing (15 sec):** Impact statement

**Total:** 4 minutes (buffer for questions)

**Practice:** 20 times until muscle memory

**Owner:** Full Team  
**Deadline:** Continuous practice

---

#### 18. Prepare 3 Backup Plans
**Plan A:** Live demo on stage (primary)  
**Plan B:** Pre-recorded video (if WiFi fails)  
**Plan C:** Slides + terminal commands (if laptop fails)

**Test:** All 3 plans work flawlessly

**Owner:** Tech Lead  
**Deadline:** 1 day before finals

---

#### 19. Mock Presentations
**Schedule:** 5 mock sessions with mentors/friends as judges

**Each session:**
- Full 10-minute presentation
- 5-minute Q&A
- Feedback & iteration

**Rotate roles:** Different team members present each time

**Owner:** Team Lead  
**Deadline:** Last week before finals

---

### **Priority 11: Deployment to Cloud** ☁️

#### 20. Production Deployment
**Current:** Running on localhost  
**Target:** Publicly accessible URL

**Deploy to:** AWS / Azure / Heroku / DigitalOcean

**Architecture:**
- Frontend: Vercel / Netlify (or S3 + CloudFront)
- Backend: EC2 / App Service
- Database: RDS / managed PostgreSQL
- RAG Service: EC2 with GPU (optional) or Lambda

**URL:** `https://manakai.demo` or similar

**Why:** Judges can access from anywhere, shows production-readiness

**SSL:** Let's Encrypt (free HTTPS)

**Owner:** DevOps / Full Team  
**Deadline:** 1 week before finals

---

#### 21. Monitoring & Uptime
**Add:**
- Uptime monitoring (UptimeRobot - free)
- Error tracking (Sentry - free tier)
- Analytics (Google Analytics or Plausible)
- Health check endpoints
- Alert system (email if service down)

**Owner:** Backend Lead  
**Deadline:** 3 days

---

## 🎯 **PHASE 5: FINAL TOUCHES (Days Before Finals)**

### **Priority 12: Presentation Polish** 🎤

#### 22. Slide Deck Refinement
**Review PPT:**
- ✅ Every slide has clear message
- ✅ No text walls (use visuals)
- ✅ Consistent design
- ✅ Animations enhance, not distract
- ✅ Metrics are prominent
- ✅ Screenshots are high-quality

**Get feedback:** Show to 3 non-technical people - if they understand, it's good

**Owner:** Presentation Lead  
**Deadline:** 3 days before finals

---

#### 23. Judge Q&A Prep Session
**Review:** JUDGE_QUESTIONS_ANSWERS.md (already created)

**Add 10 more questions based on:**
- Current events in AI/compliance
- New features you added
- Specifics of your implementation

**Practice:** Each team member answers 5 questions out loud

**Owner:** Full Team  
**Deadline:** 2 days before finals

---

#### 24. Team Coordination
**Assign clear roles:**
- **Person 1:** Main presenter (memorizes pitch)
- **Person 2:** Demo driver (keyboard control)
- **Person 3:** Technical Q&A (answers architecture questions)
- **Person 4:** Business Q&A (answers market/business model)
- **Person 5:** Backup (ready to jump in anywhere)
- **Person 6:** Time keeper (signals time remaining)

**Practice:** Each person knows their role cold

**Owner:** Team Lead  
**Deadline:** 3 days before finals

---

## 🎯 **BONUS: NICE-TO-HAVE (If Time Permits)**

### Optional Features:

#### 25. Multilingual Support (Hindi)
- Translate UI to Hindi
- Accept queries in Hindi
- Return answers in Hindi

**Priority:** LOW (only if everything else done)  
**Time:** 3-4 days

---

#### 26. Voice Input
- Microphone button
- Speech-to-text for queries
- Text-to-speech for answers

**Priority:** LOW (flashy but not critical)  
**Time:** 2-3 days

---

#### 27. Export Feature
- Export Q&A as PDF report
- Save conversations
- Email transcript

**Priority:** MEDIUM  
**Time:** 1-2 days

---

## 📋 **MASTER CHECKLIST**

### Week 1: Core Strengthening ✅
- [ ] Fix registration bugs
- [ ] Enhance "Why this answer?" with scores
- [ ] Optimize response time (<2 sec)
- [ ] Add 20 more standards (reach 50 total)
- [ ] Enrich metadata (full citation info)
- [ ] Create 100-question golden dataset
- [ ] Run automated evaluation (show 91%+ metrics)

### Week 2: Feature Addition ⭐
- [ ] Build analytics dashboard (impressive charts)
- [ ] Add certification pathway guide
- [ ] Create comparison feature
- [ ] Test all features thoroughly

### Week 3: Polish & Deploy 🎨
- [ ] UI/UX refinements (animations, loading states)
- [ ] Mobile responsiveness
- [ ] User guide / help section
- [ ] Record backup video demo
- [ ] Security audit & hardening
- [ ] Add legal disclaimers
- [ ] Deploy to cloud (publicly accessible URL)
- [ ] Set up monitoring

### Week 4: Demo Perfection 🎬
- [ ] Finalize 5-minute demo script
- [ ] Prepare 3 backup plans
- [ ] Conduct 5 mock presentations
- [ ] Refine slide deck
- [ ] Practice Q&A (25+ questions)
- [ ] Assign team roles clearly
- [ ] Final system test (everything works)

### Day Before Finals 🎯
- [ ] Full dress rehearsal (with timing)
- [ ] Test live demo 10 times
- [ ] Verify cloud deployment working
- [ ] Print quick reference cards
- [ ] Sleep 8 hours!

---

## 📊 **SUCCESS METRICS (To Show Judges)**

By finals, you should have:

### **Quantitative:**
- ✅ **50+ standards** loaded (was 30)
- ✅ **8,000+ chunks** (was 4,029)
- ✅ **100-question test set** with results
- ✅ **91%+ retrieval recall**
- ✅ **94%+ citation accuracy**
- ✅ **<2 sec response time**
- ✅ **Zero critical bugs**

### **Qualitative:**
- ✅ **Publicly accessible** demo URL
- ✅ **Professional UI** (polished, not janky)
- ✅ **Impressive analytics** dashboard
- ✅ **Unique features** (certification pathway, comparison)
- ✅ **Confident team** (practiced 20+ times)

---

## 💰 **BUDGET ESTIMATE (If Needed)**

### Cloud Hosting (1 month):
- Frontend (Vercel): Free tier ✅
- Backend (EC2 t3.medium): ₹3,000/month
- Database (RDS t3.micro): ₹2,000/month
- RAG Service (EC2 t3.large): ₹5,000/month
- Domain (optional): ₹500/year
- **Total: ~₹10,000/month**

### Tools & Services (Free Tiers):
- Sentry (error tracking): Free
- UptimeRobot (monitoring): Free
- GitHub (code hosting): Free
- Figma (design): Free

**Total Investment: ₹10-15K for finals prep**

---

## 🎯 **PRIORITY RANKING**

### **MUST DO (Critical for winning):**
1. ✅ Fix bugs (registration, performance)
2. ✅ Create golden test dataset + evaluation
3. ✅ Build analytics dashboard
4. ✅ Deploy to cloud (public URL)
5. ✅ Practice demo 20+ times
6. ✅ Prepare for Q&A (25+ questions)

### **SHOULD DO (Strong differentiators):**
7. Add certification pathway feature
8. Enhance UI/UX polish
9. Mobile responsiveness
10. Security hardening
11. Add 20 more standards

### **NICE TO HAVE (If time permits):**
12. Comparison feature
13. Video backup demo
14. Multilingual support
15. Voice input

---

## 🚀 **MOTIVATION**

You've already WON the internal round! 🎉

That means:
- ✅ Your idea is SOLID
- ✅ Your execution is GOOD
- ✅ Your team is CAPABLE

Now you just need to:
- 🔧 Fix the rough edges
- 💎 Polish what's working
- 📊 Add impressive features
- 🎤 Present with confidence

**You're 70% there. Now go to 100%!**

---

## 📞 **NEXT IMMEDIATE STEPS (Today)**

1. **Team Meeting (2 hours):**
   - Review this action plan
   - Assign owners for each priority
   - Create project board (Trello/Notion)
   - Set daily standups (15 min each morning)

2. **Technical Audit (1 hour):**
   - List all known bugs
   - Prioritize by severity
   - Create GitHub issues

3. **Start Week 1 Tasks:**
   - Begin fixing registration bug
   - Start creating golden dataset
   - Research 20 more BIS standards to add

---

## 🎯 **YOUR COMPETITIVE EDGE**

Remember, other finalists will have:
- ✅ Good ideas
- ✅ Working prototypes
- ✅ Decent presentations

**You'll WIN because you have:**
- ✅ **Measurable performance** (94% accuracy, not just claims)
- ✅ **Production-ready system** (deployed, not just localhost)
- ✅ **Evidence-first approach** (unique positioning)
- ✅ **Impressive features** (analytics, certification guide)
- ✅ **Honest about limitations** (builds trust)
- ✅ **Prepared for hard questions** (25+ answers ready)

---

## 🏆 **FINAL MESSAGE**

You got selected for a reason. Your project has merit.

Now it's execution time.

**Work hard for the next 3 weeks, and you'll look back proud regardless of outcome.**

**But honestly? With this plan, you're going to CRUSH IT.** 🔥

---

**LET'S GO WIN SIH 2026! 🚀🏆**

---

**Questions? Blockers? Need help?**
I'm here. Let's make ManakAI a national winner! 💪
