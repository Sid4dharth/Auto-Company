# Word Precision Audit: Deep Research Skill

**Date:** 2025-11-04
**Purpose:** Systematic review of every word in SKILL.md for precision, intention, and clarity

---

## Audit Methodology

**Criteria for precision:**
1. **No hedge words** ("reasonably", "generally", "basically", "essentially")
2. **No weak verbs** ("can", "may", "might", "should" → use "must", "will", "do")
3. **No vague adjectives** ("good", "nice", "reasonable" → use specific criteria)
4. **No passive voice** where active is stronger
5. **No colloquialisms** in formal directives
6. **No double negatives** ("no need to" → "proceed without")
7. **No redundancy** (say once, clearly)
8. **No ambiguous pronouns** without clear referents

---

## Issues Found (14 total)

### HIGH PRIORITY (8 issues)

#### Issue #1: "reasonable assumptions" (Lines 54, 58)
**Current:**
```markdown
Proceed with reasonable assumptions.
Make reasonable assumptions based on query context.
```

**Problem:** "reasonable" is subjective, vague, creates uncertainty about what's acceptable

**Fix:**
```markdown
Infer assumptions from query context.
Derive assumptions from query signals.
```

**Intention carried:** "reasonable" → permission-seeking, cautious | "infer/derive" → direct action, confident

---

#### Issue #2: "genuinely incomprehensible" (Line 61)
**Current:**
```markdown
Query is genuinely incomprehensible
```

**Problem:** "genuinely" is hedge word, weakens the criterion

**Fix:**
```markdown
Query is incomprehensible
```

**Intention carried:** "genuinely" → doubting, qualifying | removed → clear, definitive

---

#### Issue #3: "User can redirect if needed" (Line 64)
**Current:**
```markdown
PROCEED with standard mode. User can redirect if needed.
```

**Problem:** "can" is weak permission, "if needed" is uncertain, both undermine autonomy

**Fix:**
```markdown
PROCEED with standard mode. User will redirect if incorrect.
```

**Intention carried:** "can...if needed" → uncertain, permission-seeking | "will...if incorrect" → confident, definitive

---

#### Issue #4: "NO need to wait" - double negative (Line 85)
**Current:**
```markdown
NO need to wait for approval - proceed directly to execution
```

**Problem:** Double negative ("NO need") is weaker than direct command, "proceed directly to execution" is wordy

**Fix:**
```markdown
Proceed without waiting for approval
```

**Intention carried:** "NO need to" → permissive, passive | "Proceed without" → imperative, active

---

#### Issue #5: Contraction "Don't" (Line 113)
**Current:**
```markdown
Don't inline everything - use references
```

**Problem:** Contraction in formal directive, less authoritative

**Fix:**
```markdown
Do not inline everything - reference external files
```

**Intention carried:** "Don't" → casual | "Do not" → formal, authoritative

---

#### Issue #6: "ask to proceed" - weak request (Line 229)
**Current:**
```markdown
<5 sources after exhaustive search → Report limitation, ask to proceed
```

**Problem:** "ask to proceed" is weak, implies uncertainty about whether to continue

**Fix:**
```markdown
<5 sources after exhaustive search → Report limitation, request direction
```

**Intention carried:** "ask to proceed" → tentative | "request direction" → professional, clear need

---

#### Issue #7: "When uncertain" contradicts autonomy (Line 262)
**Current:**
```markdown
**When uncertain:** Be thorough, not fast. Quality > speed.
```

**Problem:** "When uncertain" directly contradicts autonomy principle (line 54 says operate independently), creates confusion about when to be uncertain

**Fix:**
```markdown
**Priority:** Thoroughness over speed. Quality > speed.
```

**Intention carried:** "When uncertain" → hesitation, doubt | "Priority" → clear directive, no uncertainty

---

#### Issue #8: "acceptable" is passive (Line 280)
**Current:**
```markdown
Extended reasoning acceptable (5-45 min)
```

**Problem:** "acceptable" is passive, permission-seeking, weak

**Fix:**
```markdown
Time investment: 5-45 minutes
```

