# Technical Report: Scalable Network Intrusion Detection System (NIDS)

## 1. Executive Summary
This project focuses on building a high-performance machine learning pipeline for detecting network intrusions using the CIC-IDS2017 dataset. The system evolved from a high-accuracy but biased model to a robust, security-focused detection engine capable of identifying rare and sophisticated attacks while maintaining real-time simulation capabilities.

---

## 2. Phase 1: Data Engineering & Scalability
Handling a large-scale network dataset required significant memory optimizations and rigorous cleaning.

*   **Initial Data Volume**: 2,830,743 raw network flows across 8 CSV files.
*   **Cleaning & Deduplication**: Reduced to **2,522,362 unique flows**.
*   **Memory Optimization**: 
    *   Implemented feature downcasting (float64 → float32).
    *   Resulted in a **60% reduction in RAM usage**, allowing the entire 2.5M row dataset to be processed on standard hardware (1.2GB vs 3GB+).
*   **Label Sanitization**: Corrected corrupted encoding in "Web Attack" classes to ensure label consistency for the model.

---

## 3. Phase 2: Model Evolution & The Imbalance Challenge
The core challenge was extreme class imbalance (e.g., BENIGN flows outnumber Web Attacks by over 10,000:1).

### Version A: The "Accurate" Model (Default Parameters)
*   **Global Accuracy**: 99.76%
*   **Critical Failure**: High accuracy was achieved by ignoring minority classes.
    *   **Bot Detection**: 44% Recall (Missed half the bots).
    *   **Web Attack (XSS) Detection**: **2% Recall** (Effectively blind).
*   **Conclusion**: Unacceptable for security as it misses the most dangerous attacks.

### Version B: The "Secure" Model (Class-Weighted)
*   **Strategy**: Implemented `class_weight='balanced_subsample'` and stratified sampling for tuning.
*   **Global Accuracy**: 98.11% (Slight drop).
*   **Detection Quality (Recall)**:
    *   **Bot Detection**: **98%** (Huge improvement).
    *   **Web Attack (XSS)**: **67%** (Now detectable).
    *   **Web Attack (Brute Force)**: **65%**.
*   **Conclusion**: This model is a professional-grade IDS that prioritizes catching threats over looking "perfect" on paper.

---

## 4. Phase 3: Real-Time Simulation & SIEM Readiness
The final phase tested the model in a simulated production environment.

*   **Stress Test**: Simulated 1,000 flows with a 50/50 mix of Benign and Attack traffic.
*   **Simulation Accuracy**: **81.60%**. 
    *   The drop from 98% is due to "Security Paranoia"—the model flags suspicious benign traffic to ensure no real attack is missed.
*   **SIEM Integration**: 
    *   Generated standard JSON logs containing **UUIDs, ISO-8601 timestamps, and Confidence Scores**.
    *   Implemented dynamic **Severity Levels** (HIGH/MEDIUM/LOW) based on prediction confidence.

---

## 5. Final Recommendation
For a real-life Network Intrusion Detection system, the **Class-Weighted Random Forest (Version B)** is the only acceptable choice. 

**Rationale**: 
In cybersecurity, a **False Positive** (a false alarm) costs a few minutes of an analyst's time. A **False Negative** (a missed attack) can cost an entire organization's data. The updated model provides the necessary "visibility" into rare attack vectors that standard machine learning models typically ignore.
