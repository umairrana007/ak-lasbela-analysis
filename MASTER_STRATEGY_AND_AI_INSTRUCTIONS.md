# 🏆 THE 15-TRICK MASTER SPECIFICATION FOR LOTTERY ANALYTICS

This document defines the complete logical framework for the "Lottery Pattern Analytics & Prediction System". It is designed to be used by an AI to build a predictive web application.

---

## 📅 THE CORE TARGET MATRIX (MULTI-LINE LOGIC)
Target Lines are derived dynamically from the Master Number of the day (e.g., 71.20.59).

### **Line 1 (71.20.59) Targets:**
1. 712 -> 059 | 2. 710 -> 259 | 3. 715 -> 209 | 4. 719 -> 205 | 5. 120 -> 759
6. 105 -> 927 | 7. 109 -> 527 | 8. 207 -> 159 | 9. 907 -> 125 | 10. 507 -> 129

### **Line 2 (59.57.66) Targets (Example):**
1. 595 -> 076 | 2. 597 -> 056 | 3. 596 -> 057 | 4. 596 -> 057 | 5. 957 -> 066
*(System will automatically generate 10 lines for any master input following the split-digit logic).*

---

## 🧹 AUTOMATIC CLEANUP & STATE RULE
- **Hit & Clear:** Once a prediction matches a result in any draw (GM, LS1, AK, LS2, LS3), it MUST be marked as **"COMPLETED"** and moved to the History log.
- **Wait Management:** Only pending patterns should be displayed on the active dashboard.
- **7-Day Expiry:** If a pattern does not hit within 7 days, mark it as **"EXPIRED"** to keep the system fresh.

---

## ⚡ THE 15 MASTER TRICKS & RULES

### [SIGNAL TRICKS & COMBINATIONS]
1. **Horizontal Trigger (Aamne-Samne):** Signal fires when adjacent games show target digits.
   - **Allowed Pairs:** (GM + LS1), (LS1 + AK), (AK + LS2), (LS2 + LS3)

2. **Vertical Trigger (Upar-Neechay):** Signal fires when the same game shows target digits across consecutive days.
   - **Allowed Pairs:** (Today's GM + Yesterday's GM), (Today's LS1 + Yesterday's LS1), (Today's AK + Yesterday's AK), (Today's LS2 + Yesterday's LS2), (Today's LS3 + Yesterday's LS3)

3. **Cluster Trigger (3-Game Span):** Signal fires when 3 consecutive games form a "Super Target".
   - **Allowed Trios:** (GM + LS1 + AK), (LS1 + AK + LS2), (AK + LS2 + LS3)

4. **Diagonal Signal (Tircha):** Target digits appearing diagonally (e.g., Yesterday's GM + Today's LS1).

### [ANALYTICAL TRICKS]
5. **Common Overlap (The Confirm Figure):** If 2+ targets fire, the digit common to their counterparts is a "Sure Hit". *Example: 19/03 (Common 2 & 9 led to hit).*
6. **Mirror Reflection (The Lock):** If target digits and their mirrors (1=6, 2=7, 0=5) appear together, the signal is 100% locked.
7. **Missing Digit (Gap Filler):** If a 3-digit target shows only 2 digits, the missing digit becomes the leading figure of the next hit.
8. **Bridge Digit (Zero Logic):** Since 7/10 targets contain '0', a Zero in the trigger acts as a strong connection between Purane and Naye numbers.
9. **Repeat Alert (Urgency):** If trigger digits repeat in the next draw, the hit is imminent (within 24h).

### [PROBABILITY & TIMING TRICKS]
10. **The 82% Jora (Double) Rule:** Multiple triggers on the same day lead to a Double (99, 22, etc.) in the next 3 days with 82% accuracy.
11. **72-Hour Intensity Window:** Peak hit probability is within the first 3 days after a trigger.
12. **7th Day Rule (Same Day Next Week):** If a hit misses the 72h window, it will likely hit exactly 7 days later (Same Day).
13. **Weekend Dump (Mon-Tue):** Targets from Sat/Sun usually "dump" results on Monday/Tuesday (highest volume days).
14. **Game Routing (Pathing):** Targets in AK usually hit in LS2/LS3. Targets in GM usually hit in LS1/AK.
15. **Line 2 Transition:** After a Line 1 hit, the system often moves to Line 2 (59.57.66) patterns.

---

## 🤖 THE AI SYSTEM PROMPT (For Google AI Studio / Gemini)

"You are a Senior Pattern Analyst. Your task is to process daily lottery records (GM, LS1, AK, LS2, LS3) using 15 specific logical rules.

**Goal:** Identify active triggers and predict the next 'Counterpart Double' (Jodi).

**Logic Rules:**
[Paste the 15 Tricks listed above here]

**Expected Output Format:**
1. **Detected Trigger:** (e.g. Horizontal AK-LS2 on 19/03)
2. **Target Line:** (e.g. 710)
3. **Applied Tricks:** (e.g. Overlap shows digit 2 is strong)
4. **Predicted Jodi:** (List of 2-3 most likely pairs)
5. **Window:** (Expected hit date and game name)
6. **Confidence Level:** (High/Medium/Urgent based on Overlap/Repeat tricks)"

---

## 📊 DATA EXAMPLE FOR AI TRAINING
Date: 19/03 | GM: XX | LS1: XX | AK: 71 | LS2: 20 | LS3: 59 | Day: Thu
Trigger: Horizontal (71-20) | Target: 710, 712, 715...
Hit: 20/03 | LS2: 52 | LS3: 21 (Common digit 2 Hit!)
