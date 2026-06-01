# CyberGuard AI 🛡️🤖

CyberGuard AI is an educational, autonomous penetration testing assistant built from scratch in Python. Given a single target configuration (a local development VM or authorized CTF sandbox container), it uses **Gemini 2.0 Flash** via function-calling mechanics to reason through network discoveries, analyze software banners, cross-reference vulnerabilities, and compile defensive mitigation reports.

---

## 🏗️ System Architecture

The tool uses a decoupled, four-layer architecture to keep the AI's analytical capabilities separate from execution:

```text
       +-------------------------------------------------------+
       |                  User Target Input                    |
       +---------------------------+---------------------------+
                                   |
                                   v
       +-------------------------------------------------------+
       |       Layer 1: Network Scanner (Subprocess/Nmap)      |
       +---------------------------+---------------------------+
                                   | (Structured Pydantic Model)
                                   v
+---------------------------------------------------------------------+
|                  Layer 2: AI Core Loop Engine                       |
|  +---------------------------------------------------------------+  |
|  |             Gemini 2.0 Flash Tool Routing Config              |  |
|  +-------------------------------+-------------------------------+  |
|                                  |                                  |
|                                  v (Function Call Event)            |
|  +-------------------------------+-------------------------------+  |
|  |                  Layer 3: Functional Toolset                  |  |
|  |    * Socket Banner Grabber    * NVD Live CVE Lookup API       |  |
|  +-------------------------------+-------------------------------+  |
+----------------------------------+----------------------------------+
                                   |
                                   v
       +-------------------------------------------------------+
       |           Layer 4: State Memory & Reporting           |
       |     * JSON Session Ledger    * Markdown Documentation |
       +-------------------------------------------------------+