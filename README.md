# Linux Command Translator (English → Bash)

A lightweight, CPU‑friendly tool that converts **plain English instructions into safe Linux shell commands** using a **Small Language Model (SLM)** running locally via **Ollama**.  
The project is designed with **feedback collection**, **data quality**, and **future fine‑tuning** in mind.

---

## ✨ Key Features

- **Plain English → Bash command translation**
- **Streamlit** App UI
- Uses **Phi‑3‑mini** (efficient, instruction‑tuned SLM)
- **Dockerized PostgreSQL** for zero‑friction setup
- Stores prompts, outputs, and metadata for future fine‑tuning of SLM
- Structured feedback‑ready database schema
- Proper logging (no noisy `print()` calls)
- Runs fully on **CPU‑only hardware**

---

## 🧱 Architecture Overview

```
Streamlit App UI
        │
        ▼
User Input (English)
        │
        ▼
Translate Prompt
        │
        ▼
Ollama (phi3:mini)
        │
        ▼
Generated Bash Command
        │
        ├── Display to user in UI
        └── Persist to PostgreSQL (for feedback & future training)
```
---

## 🚀 Getting Started

### 1️. Prerequisites

- Python **3.10+**
- Docker + Docker Compose
- Ollama installed locally

---

### 2️. Start PostgreSQL (Docker)

```bash
docker compose up -d
```

This will:
- Start PostgreSQL
- Create the database
- Initialize schema via `db/init.sql`

---

### 3️. Create & activate virtual environment

```bash
python -m venv myenv
```

**Linux / macOS**
```bash
source myenv/bin/activate
```

**Windows**
```powershell
myenv\Scripts\activate
```

---

### 4️. Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

---

### 5️. Pull the SLM model (if not already present)

```bash
ollama pull phi3:mini
```

---

### 6️. Run the application (Streamlit will run in http://localhost:8501/)

```bash
python app.py
```

---

## 🖼️ Streamlit UI Snapshots

<img width="940" height="491" alt="image" src="https://github.com/user-attachments/assets/b13a1f4e-2f00-4867-b036-294b09857dc5" /> 

<img width="940" height="556" alt="image" src="https://github.com/user-attachments/assets/d24477d8-36a5-4ac6-8ba3-d25ebcb0a1d5" />

---

## 🔁 Feedback Loop (Future‑Ready)

The stored data enables:

- Manual or UI‑based feedback (`is_correct`)
- Human‑corrected outputs
- Clean dataset export (JSONL)
- LoRA fine‑tuning of Phi‑3‑mini

This project is designed to **improve over time**.

---

## 📁 Project Structure

```
linux-command-translator/
├── app.py              # Main entry point
├── translate.py        # Ollama prompt + inference logic
├── db.py               # PostgreSQL connection helper
├── logger.py           # Centralized logging setup
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # PostgreSQL container
└── db/
    └── init.sql        # DB schema initialization
```

---

## 📌 Roadmap Ideas

- User feedback from CLI / UI
- Finetune SLM using LoRA and command feedback from DB
- Implement RAG with `man` pages
- Safety classifier for destructive commands
- Enhanced Promt Template for more accurate results

---

## 🤝 Contributing

PRs welcome. Keep changes:
- deterministic
- well‑logged
- schema‑safe

---

Built with engineering discipline — not hype.
