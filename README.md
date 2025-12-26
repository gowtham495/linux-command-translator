# Linux Command Translator (Plain English → Bash)

A lightweight **Linux command translator** that converts plain English instructions into **single, valid Bash commands** using a **small language model (SLM)** running **locally on CPU** via **Ollama**.

This tool is designed for engineers, sysadmins, and power users who want fast, private, and dependency-light command generation without cloud LLMs.

---

## 🚀 Key Features

- Plain English → **one clean Bash command**
- Uses **SLMs only** (CPU-friendly)
- Runs **100% locally** via Ollama
- No explanations, no markdown, no noise — just the command
- Safe-by-design prompt rules
- Interactive CLI mode

---

## 🧠 Architecture Overview

```
User (English Input)
        ↓
translate.py
        ↓
Ollama REST API (localhost)
        ↓
phi-3-mini (CPU)
        ↓
Single Bash Command (stdout)
```

---

## 🤖 Model Choice

- **Model:** `phi3:mini`
- **Why?**
  - Optimized for CPU
  - Fast inference
  - Strong instruction-following
  - Available directly in Ollama

You can swap models if needed (see Configuration).

---

## 📦 Project Structure

```
linux-command-translator/
├── translate.py        # CLI + Ollama integration
├── requirements.txt   # Minimal Python dependencies
├── README.md
└── .gitignore
```

---

## 🔧 Requirements

### System
- Linux / macOS / Windows (WSL recommended)
- Python **3.9+**
- CPU-only machine is sufficient

### Software
- **Ollama** installed and running  
  👉 https://ollama.com

---

## 🛠 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/linux-command-translator.git
cd linux-command-translator
```

### 2️⃣ Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Pull the model in Ollama
```bash
ollama pull phi3:mini
```

### 4️⃣ Start Ollama
```bash
ollama serve
```

---

## ▶️ Usage

Run the translator in interactive mode:

```bash
python translate.py
```

You’ll see:
```
Describe task (or 'exit'):
```

Type a task in plain English.

---

## 🧪 Example Inputs & Outputs

| English Input | Generated Bash Command |
|--------------|-----------------------|
| Find all `.log` files modified today | `find . -name "*.log" -mtime 0` |
| Show top 5 memory-consuming processes | `ps aux --sort=-%mem | head -n 6` |
| Count lines in all txt files | `wc -l *.txt` |
| Find process using port 8080 | `lsof -i :8080` |

---

## ⚙️ Configuration

Edit `translate.py`:

```python
MODEL = "phi3:mini"
OLLAMA_URL = "http://localhost:11434/api/generate"
```

### Supported Alternatives (CPU-friendly)
- `qwen2.5:1.5b`
- `gemma:2b`
- `llama3.2:1b`

---

## 🔒 Safety & Prompt Rules

The system prompt enforces:

- Exactly **ONE Bash command**
- No explanations or comments
- No markdown or formatting
- Closest **safe** command if ambiguous

This makes the output:
- Scriptable
- Pipe-friendly
- CI/CD compatible

---

## ⚠️ Limitations

- Bash-focused (not PowerShell)
- No multi-command pipelines with explanations
- Assumes user has basic Linux context
- Not a replacement for understanding commands ⚠️

---

## 🛣 Roadmap

Planned improvements:
- `--dry-run` mode
- Command risk scoring
- Shell autodetection (bash/zsh/fish)
- JSON output mode for automation
- History + caching
- Reverse translation (Linux command -> Explanation in Plain English)

---

## 🤝 Contributing

Contributions are welcome.

Suggested areas:
- Prompt tuning
- Model benchmarking
- Safety guardrails
- UX improvements

Fork → Improve → PR.

---

## 📄 License

MIT License  
Use it, modify it, ship it.

---

## 🙌 Philosophy

> Fast. Local. Private. Practical.

If you understand Linux, this tool **multiplies your speed**.  
If you don’t — it forces you to learn responsibly.

Use wisely.
