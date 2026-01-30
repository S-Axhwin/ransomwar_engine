# 🛡️ Ransomware Detector & Honeynet Engine

A **modular ransomware detection and containment system** built for labs, security research, and controlled enterprise testing. This engine uses **decoy (canary) files**, **file integrity monitoring**, and **entropy-based encryption detection** to identify ransomware-like behavior and trigger containment actions.

> ⚠️ This is a **defensive security tool** intended for research and mitigation testing only.

---

## 🔍 Overview

The system is designed to detect ransomware **behavior**, not signatures.

It works by:

* Planting **decoy files** with embedded canary tokens
* Monitoring them for unauthorized modifications
* Detecting **encryption-like behavior** via entropy analysis
* Triggering **containment actions** (safe by default)
* Logging everything in **structured JSON** for analysis and replay

---

## 🧩 Architecture & Modules

### 1. Decoy System

* Generates realistic fake files (documents, spreadsheets, etc.)
* Each decoy embeds a **unique canary token**
* Any modification to a decoy is treated as a high-confidence alert

**Location:**

```
ransomware_engine/decoy/
```

---

### 2. Detection Engine

#### 📁 File Integrity Monitor (FIM)

* Uses filesystem event monitoring (Watchdog)
* Watches decoy directories recursively
* Detects:

  * File modification
  * Unauthorized writes
  * Tampering with canary files

#### 🔐 Crypto / Entropy Monitor

* Calculates file entropy after modification
* High entropy = likely encryption
* Helps distinguish ransomware from normal edits

**Location:**

```
ransomware_engine/detector/
```

---

### 3. Containment System

Triggered automatically on confirmed detection.

Capabilities:

* Network isolation
* Process termination
* Network drive protection

⚠️ **Safe Mode is enabled by default**:

* Actions are logged but **not executed**
* Prevents accidental system disruption during testing

**Location:**

```
ransomware_engine/containment/
```

---

### 4. Logging System

* Structured **JSON logs**
* Timestamped, module-aware, severity-based
* Designed for SIEM ingestion or forensic replay

**Location:**

```
ransomware_engine/logger/
```

---

## 🚀 How to Run

### 1️⃣ Setup Environment

Activate your virtual environment and install dependencies:

```bash
./venv/bin/pip install -r requirements.txt
```

---

### 2️⃣ Run the Engine

Run the main orchestrator. You must set `PYTHONPATH` so internal modules resolve correctly.

```bash
PYTHONPATH=. ./venv/bin/python ransomware_engine/main.py --watch . --decoys my_decoys
```

#### Arguments

| Flag                 | Description                                      |
| -------------------- | ------------------------------------------------ |
| `--watch .`          | Monitors the current directory recursively       |
| `--decoys my_decoys` | Creates and monitors decoy files in `my_decoys/` |

---

### 3️⃣ Simulate an Attack

In another terminal, modify a decoy file:

```bash
echo "ENCRYPTED_DATA" >> my_decoys/salary_data.docx
```

This simulates ransomware-style file modification.

---

### 4️⃣ Observe the Response

Expected log output:

```
CRITICAL:ransomware_engine.detector.fim: 🚨 DECOY TOUCHED: .../salary_data.docx was modified!
CRITICAL:ransomware_engine.containment.isolate: 🚨 CONTAINMENT TRIGGERED: Network Isolation Requested
WARNING:ransomware_engine.containment.isolate: SAFE MODE ACTIVE: Network isolation skipped.
```

---

## 📁 Directory Structure

```
ransomware_engine/
├── decoy/          # Decoy (canary) file generation
├── detector/       # FIM and entropy-based detection
├── containment/    # Isolation and response logic
├── logger/         # Structured JSON logging
├── main.py         # Entry point / orchestrator
```

---

## ✅ Verified Features

* ✅ Decoy generation with unique canary tokens
* ✅ Real-time file modification detection
* ✅ Entropy-based encryption detection
* ✅ Automated containment triggering
* ✅ Safe Mode to prevent accidental system isolation
* ✅ Structured logs suitable for forensic analysis

---

## ⚠️ Important Notes

* This tool **requires elevated privileges** for real containment actions
* Designed for **labs, VMs, and test environments**
* Advanced ransomware may throttle or evade detection — this system focuses on **early-stage detection**

---

## 🧠 Intended Use Cases

* Blue-team training labs
* Ransomware simulation & testing
* Endpoint detection research
* Honeynet experimentation

---

## 📌 Next Possible Extensions

* Dashboard UI for live alerts
* SIEM / ELK integration
* Process tree correlation
* VM snapshot-based replay
* Network traffic anomaly detection

---

**Built for realism, not demos.**
If it trips — something is seriously w
