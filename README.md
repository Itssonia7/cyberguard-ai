```markdown
# CyberGuard AI 🛡️🤖

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Validation-Pydantic%20v2-red.svg)](https://docs.pydantic.dev/)
[![LLM](https://img.shields.io/badge/Reasoning-Gemini%202.0%20Flash-orange.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

CyberGuard AI is an advanced, autonomous penetration testing assistant built from scratch in Python. Given an authorized target configuration (such as a local development VM or isolated CTF docker container), it acts as a junior security analyst—combining raw active reconnaissance tooling with deterministic AI reasoning loops.

By leveraging **Gemini 2.0 Flash** native function-calling mechanics, the agent handles network discoveries, finger-prints service banners, cross-references vulnerabilities with live global registries, and compiles comprehensive architectural remediation reports completely on its own.

---

## 🏗️ System Architecture & Workflow

CyberGuard AI utilizes a strictly decoupled, 4-layer design pattern ensuring that data flows sequentially through structured validation boundaries before reaching the execution chassis or LLM context.

```text
       +-------------------------------------------------------+
       |                  User Target Input                    |
       +---------------------------+---------------------------+
                                   |
                                   v
       +-------------------------------------------------------+
       |       Layer 1: Network Scanner (Subprocess/Nmap)      |
       +---------------------------+---------------------------+
                                   | (Structured HostScanResult)
                                   v
+---------------------------------------------------------------------+
|                  Layer 2: LLM Reasoning Core Loop                   |
|  +---------------------------------------------------------------+  |
|  |           Gemini 2.0 Flash Function Routing Config            |  |
|  +-------------------------------+-------------------------------+  |
|                                  |                                  |
|                                  v (Emitted AgentAction Decision)   |
|  +-------------------------------+-------------------------------+  |
|  |             Layer 3: Functional Execution Tools               |  |
|  |    • Socket Banner Grabber    • NVD Live CVE Lookup API       |  |
|  +-------------------------------+-------------------------------+  |
+----------------------------------+----------------------------------+
                                   |
                                   v
       +-------------------------------------------------------+
       |          Layer 4: Memory Persistence & Reporting      |
       |     • JSON Session Ledger    • Markdown Compilation   |
       +-------------------------------------------------------+

```

---

## ⚡ Interactive CLI Dashboard Preview

The interface utilizes the `Rich` framework to bring a modern, terminal-ui environment to automated security analysis. Long-running asynchronous scan jobs and complex API analysis functions are paired with status indicators and clean presentation blocks:

```text
 ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
 ┃ CyberGuard AI — Autonomous Penetration Testing Agent                   ┃
 ┃ Session ID: cg-20260601-114530 | Target Scoped: 127.0.0.1              ┃
 ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

 ➔ Exposed Attack Surface Discovery
 ┏━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
 ┃ Port ┃ Protocol ┃ State ┃ Identified Service ┃
 ┡━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
 │ 22   │ TCP      │ open  │ ssh                │
 │ 80   │ TCP      │ open  │ http               │
 ┗━━━━━━┻━━━━━━━━━━┻━━━━━━━┻━━━━━━━━━━━━━━━━━━━━┛

 🚀 [➔] Brain Decision: Invoke tool 'grab_banner' on arguments {'port': 22}
 🏁 [✓] Turn Processed successfully. Persistent session synchronized to disk.

```

---

## 🛠️ Detailed Component Matrix

* **Sensory Scan Engine (`scanner.py`):** Runs native system `nmap` binaries inside a secure `subprocess` pipeline. Features strict input sanitation patterns (`_is_valid_target`) to inherently mitigate shell injection vulnerabilities.
* **Orchestration Brain (`agent.py`):** Utilizes the official `google-genai` SDK. Implements low-temperature functional routing contracts, transforming pure-python helper signatures into system payloads the LLM can selectively flag.
* **Granular Memory Handler (`memory.py`):** Serializes active assessment operational history directly into timestamped JSON schemas. This prevents execution amnesia, breaks recursive tool-call traps, and allows long audits to be resumed seamlessly.
* **Document Compiler (`reporter.py`):** Parses completed session states into a highly structured, executive-ready Markdown audit log detailing chronological tool paths and network maps.

---

## 🚀 Installation & Local Configuration

### 1. System Dependencies

Ensure your target host operating system has the core network exploration package installed:

```bash
sudo apt update && sudo apt install nmap -y

```

### 2. Environment Setup

Clone the repository (or navigate to your root folder) and spin up an isolated virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

### 3. Key Provisos

Create a `.env` file in your root workspace layout:

```env
GEMINI_API_KEY="AIzaSyYourActualGoogleAIStudioAPIKey"
GEMINI_MODEL="gemini-2.0-flash"
DEFAULT_TARGET="127.0.0.1"

```

---

## ⚙️ Usage Sequence

To launch the multi-turn autonomous assessment cycle against a target asset loopback, run:

```bash
python main.py 127.0.0.1

```

### Generated Artifact Deliverables

* **Memory Checkpoints:** Stored under `/sessions/session_[ID].json`
* **Audit Document:** Stored under `/reports/report_[ID].md`

---

## ⚖️ Ethical Use & Legal Disclaimer

**CRITICAL NOTICE:** CyberGuard AI is developed exclusively as an educational framework for defensive security architecture research, academic vulnerability assessment exploration, and authorized system auditing.

* **NEVER** target network clusters, public interfaces, or hardware endpoints without explicit, legally-binding written authorization from the underlying infrastructure owners.
* The developer assumes absolutely zero liability for misuse, intentional service disruptions, security alert noise generation, or legal complications arising from experimental iterations of this tooling.
* Keep generated audit data outputs completely protected on your system; compiled intelligence metrics could give unauthorized vectors an optimized layout mapping of the target topology.

```

```