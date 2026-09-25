# 🎯 SIH 2026 - Quick Reference Card (Print This!)

**Keep this with you during presentation**

---

## ⏱️ **TIMING**

| Section | Duration | Cumulative |
|---------|----------|------------|
| Opening | 1 min | 0:00-1:00 |
| Solution | 2 min | 1:00-3:00 |
| Architecture | 2 min | 3:00-5:00 |
| Live Demo | 4 min | 5:00-9:00 |
| Metrics | 1.5 min | 9:00-10:30 |
| Impact | 1.5 min | 10:30-12:00 |
| Risk Mitigation | 1 min | 12:00-13:00 |
| Roadmap | 1 min | 13:00-14:00 |
| Closing | 30 sec | 14:00-14:30 |

---

## 🔑 **KEY NUMBERS TO REMEMBER**

- **91%** - Retrieval Recall@5
- **94%** - Citation Accuracy  
- **92%** - Grounded Answer Rate
- **89%** - Abstention Accuracy
- **2.3s** - Average Latency
- **4,029** - Chunks loaded
- **30+** - BIS standards covered
- **17** - Industries covered
- **50** - Expert-validated test questions
- **63M** - MSMEs in India (TAM)

---

## 💬 **DEMO QUERIES (IN ORDER)**

### Query 1: Core Use Case
```
What are the safety requirements for LED lamps?
```
**Expected:** IS 16102:2012, Cl. 5.2, 2-3 sec response  
**Click:** "Why this answer?" → Show evidence panel

### Query 2: Different Domain
```
ECG equipment testing standards?
```
**Expected:** IS 13450 Part 2-25, different industry

### Query 3: Safe Abstention
```
Is BIS certification mandatory for flying cars?
```
**Expected:** "I don't have sufficient evidence..."

---

## 🎯 **MUST-SAY PHRASES**

Say these at least once:
- ✅ "Evidence-first BIS intelligence"
- ✅ "No hallucination—confidence-aware abstention"
- ✅ "Every answer backed by exact clause citations"
- ✅ "Explainable—Why this answer? shows evidence"
- ✅ "Feedback loop creates BIS intelligence layer"
- ✅ "We don't promise 100% accuracy—we measure it"

---

## ❓ **TOP 5 LIKELY QUESTIONS**

### 1. "How do you prevent hallucination?"
**Answer:** "Three layers: evidence-first retrieval, confidence scoring, citation traceability. 92% grounded answer rate."

### 2. "What if AI is wrong?"
**Answer:** "94% citation accuracy, confidence scores, 'Why this answer?' verification, clear disclaimers, feedback loop."

### 3. "How is this different from ChatGPT?"
**Answer:** "ChatGPT hallucinates, no citations, generic. We: evidence-backed, IS number + clause + page, BIS-specific corpus."

### 4. "What's your business model?"
**Answer:** "Freemium SaaS (₹499/month), Enterprise (₹50K/year), B2B partnerships (certification bodies, ERP plugins)."

### 5. "How do you scale to 20K standards?"
**Answer:** "Architecture designed for it. ChromaDB handles millions of vectors. 20K standards = 2.5M chunks, <200ms retrieval."

---

## 🚨 **IF DEMO FAILS**

### Backup Plan A:
- Show screenshots of working demo
- Walk through UI explaining features
- Show backend API responses in terminal

### Backup Plan B:
- Show video recording of demo
- Emphasize working code exists
- Offer to show later

### Backup Plan C:
- Walk through architecture diagrams
- Explain how it works conceptually
- Show code on GitHub

**SAY:** "Technical glitch, but system is working—we can show you later or walk through the architecture."

---

## 🎤 **OPENING LINE (MEMORIZE)**

> "Imagine you're a small business owner wanting to manufacture LED bulbs. You need BIS certification. Where do you start? Which standard applies? What tests are needed? Today, getting these answers takes weeks of confusion. With ManakAI, it takes 3 seconds."

---

## 🎤 **CLOSING LINE (MEMORIZE)**

> "ManakAI isn't just a chatbot—it's a BIS intelligence layer. We don't promise 100% AI accuracy; we measure it. We don't hide our process; we show our evidence. We don't replace human experts; we empower them with faster, verified answers. In a world where compliance confusion costs industries time and money, ManakAI brings clarity. Evidence-first, explainable, and continuously improving. Thank you. We're ready for your questions."

---

## 🛡️ **DIFFICULT QUESTION RESPONSES**

### "What if BIS sues you?"
"We cite public documents with proper attribution—that's legal. Position as complement to BIS, not replacement. If they object, pivot to international standards or become their vendor."

### "You're just wrapping ChatGPT!"
"Our moat: Curated BIS corpus (3 months to build), evidence validation layer (proprietary confidence scoring), network effects (feedback loop), brand trust (first mover)."

### "6% error rate is dangerous!"
"Baseline is 30% with manual search. We're improving (88%→94%). We flag low confidence. We enable verification. We're transparent about limits."

---

## 💡 **BODY LANGUAGE REMINDERS**

- ✅ Eye contact with questioner, then scan others
- ✅ Pause 1 sec before answering
- ✅ Open posture (no crossed arms)
- ✅ Natural hand gestures
- ✅ Smile confidently
- ❌ Don't interrupt
- ❌ Don't say "um" repeatedly
- ❌ Don't ramble (30-60 sec answers)

---

## 📱 **EMERGENCY CONTACTS**

**Demo URLs:**
- Frontend: http://localhost:5173
- Backend: http://localhost:8080
- RAG Docs: http://localhost:8000/docs

**Demo Login:**
- Username: `demo`
- Password: `demo123`

**Quick Restart:**
```bash
lsof -ti:8000,8080,5173 | xargs kill -9
# Then start services again
```

---

## ✅ **PRE-PRESENTATION CHECKLIST**

**T-10 minutes:**
- [ ] All services running
- [ ] Demo login works
- [ ] 3 demo queries tested
- [ ] Browser on demo URL
- [ ] Slides ready
- [ ] Water bottle filled

**T-1 minute:**
- [ ] Deep breath (4-7-8)
- [ ] Review key numbers
- [ ] Smile
- [ ] Confidence: "I built this. I know this."

---

## 🎯 **JUDGE PERSONAS & HOW TO ADDRESS**

### Technical Judge (CTO/Engineer)
- Go deep on architecture
- Use metrics heavily
- Show code if asked
- Be technical and precise

### Business Judge (CEO/VC)
- Focus on market, TAM, GTM
- Talk business model clearly
- Show unit economics
- Emphasize scalability

### Government Judge (BIS Official)
- Emphasize collaboration with BIS
- Show respect for official process
- Focus on feedback loop benefit
- Highlight compliance responsibility

### Academic Judge (Professor)
- Discuss research methodology
- Explain evaluation metrics
- Show systematic approach
- Acknowledge limitations honestly

---

## 🔥 **CONFIDENCE BOOSTERS**

**Before you go on stage, remember:**

1. ✅ You BUILT a working system (not slides)
2. ✅ You TESTED it (94% citation accuracy)
3. ✅ You RESEARCHED it (15 user interviews)
4. ✅ You DOCUMENTED it (26 files)
5. ✅ You KNOW this inside-out

**You've earned the right to be here. Now SHOW them why you deserve to win.**

---

## 🎬 **STAGE PRESENCE**

### Walking to Stage:
- Walk confidently (not rushed)
- Make eye contact with judges
- Smile naturally
- Stand centered

### During Presentation:
- Plant feet (don't pace nervously)
- Use hand gestures to emphasize
- Modulate voice (not monotone)
- Pause for effect after key points

### During Demo:
- Turn to screen while explaining
- Point to elements on screen
- Turn back to judges between steps
- Narrate what you're doing

### During Q&A:
- Stand/sit comfortably
- Look at questioner while listening
- Nod to show you understand
- Answer looking at all judges, not just questioner

---

## 📊 **METRICS SLIDE (MEMORIZE)**

```
📊 MEASURED PERFORMANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Retrieval Recall@5:     91%
✓ Citation Accuracy:      94%
✓ Grounded Answer Rate:   92%
✓ Abstention Accuracy:    89%
✓ Average Latency:        2.3s
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tested on: 50 expert-validated questions
Domains: Electronics, Medical, Water, 
         Construction, Automotive
```

---

## 🎁 **BONUS: IF GOING REALLY WELL**

### Show Advanced Feature:
- Admin analytics dashboard
- Query pattern visualizations
- Feedback analytics

### Mention Future Vision:
- "Imagine this: BIS uses our analytics to improve their documentation"
- "Imagine this: Every manufacturer in India uses ManakAI for compliance"
- "Imagine this: India becomes known for easiest compliance globally"

---

## ⚡ **FINAL REMINDERS**

1. **You're prepared** - You know more than they do about this system
2. **You're authentic** - Be yourself, not a robot
3. **You're passionate** - Let them see you care about this problem
4. **You're competent** - You built something real
5. **You're honest** - Admit limits, don't oversell

---

**🔥 GO WIN THIS! 🏆**

**You've got:**
- ✅ Working product
- ✅ Strong pitch
- ✅ Solid answers
- ✅ Confident team

**Now just EXECUTE and BELIEVE!**

---

**🎤 Break a leg! 🎤**
