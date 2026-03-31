# 📡 ECHO 
> **Tactical AI Assistant for Emergency Response & Patrol Intelligence**

ECHO is a hybrid AI framework designed to bridge the "Information Gap" in emergency services. By combining local audio transcription with advanced Large Language Model (LLM) reasoning, ECHO transforms chaotic emergency audio into structured, actionable intelligence in real-time.

---

## 📖 Project Overview
In high-stress emergency environments, the "golden minutes" are often lost to manual data entry and mental filtering. ECHO acts as a "Third Ear" for dispatchers and officers, providing:
* **Active Intelligence:** Moving from passive recording to real-time analysis.
* **Cognitive Offloading:** Reducing the manual burden on dispatchers so they can focus on the caller.
* **Tactical Awareness:** Ensuring field units have suspect and threat data before arriving on the scene.

---

## 🚀 Key Features
- **Real-Time Transcription:** Powered by OpenAI Whisper (Local) for secure, on-device audio processing.
- **Cognitive Analysis:** Integrates DeepSeek-V3 to extract entities (Suspects, Vehicles, Weapons) and assess threat levels.
- **Automated Reporting:** Generates standardized PDF Intelligence Briefs instantly using FPDF.
- **Audit Vault:** Secure SQLite integration for searchable incident history and legal evidence.

---

## 🛠️ Technical Stack
- **Backend:** Flask (Python)
- **AI Models:** OpenAI Whisper (ASR), DeepSeek-V3 (NLP)
- **Database:** SQLite
- **Environment:** Python Dotenv (Security)
- **Reporting:** FPDF Library

---

## 📦 Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yui0uwu/ECHO-AI-Transcription.git](https://github.com/yui0uwu/ECHO-AI-Transcription.git)
   cd ECHO-AI-Transcription
