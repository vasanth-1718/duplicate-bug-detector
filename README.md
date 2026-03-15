# 🐞 Duplicate Bug Detector

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-NLP-154f3c?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Automatically detect duplicate bug reports using NLP & cosine similarity.**  
Stop wasting time reading the same bug twice. 🚀

[Features](#-features) · [Demo](#-demo) · [Installation](#-installation) · [Usage](#-usage) · [How It Works](#-how-it-works) · [Project Structure](#-project-structure)

</div>

---

## 🧠 What Is This?

Ever had 50 developers filing the same bug in 50 different ways?

> *"App crashes on save"*  
> *"System stops working when save button is pressed"*  
> *"Clicking save breaks everything"*

They're all the **same bug**. This tool uses **Natural Language Processing (NLP)** to automatically catch those duplicates — so your team can focus on fixing bugs, not sorting them.

---

## ✨ Features

- 🔍 **Instant duplicate detection** — paste a bug description and get similarity scores in seconds
- 🧹 **Smart text preprocessing** — removes noise, stopwords, and special characters automatically
- 📊 **TF-IDF vectorization** — converts bug descriptions into meaningful numerical representations
- 📐 **Cosine similarity scoring** — mathematically compares bug reports for accuracy
- 🖥️ **Clean Streamlit UI** — no terminal needed, just a simple web interface
- ⚙️ **Auto port detection** — launcher finds a free port automatically, no config needed

---

## 🎬 Demo

```
Input:  "Login page freezes after entering credentials"

Results:
  Bug 3 → similarity: 1.00  ✅ Exact match!
  Bug 4 → similarity: 0.42  ⚠️  Possible duplicate: "System hangs when submitting login form"
  Bug 1 → similarity: 0.05  ✔️  Not a duplicate
```

---

## 📁 Project Structure

```
duplicate-bug-detector/
│
├── 📂 data/
│   └── bug_reports.csv          # Bug dataset (id, title, description)
│
├── 📂 preprocessing/
│   └── clean_text.py            # NLP text cleaning pipeline
│
├── 📂 streamlit_app/
│   └── app.py                   # Streamlit web UI
│
├── train.py                     # CLI script — prints full similarity matrix
├── run_streamlit.py             # Smart launcher with auto port detection
├── requirements.txt             # Python dependencies
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/vasanth-1718/duplicate-bug-detector.git
cd duplicate-bug-detector
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### 🖥️ Run the Web App (recommended)

```bash
python run_streamlit.py
```

Opens automatically at `http://localhost:8501` (or next free port).  
Type a bug description → Click **"Check Duplicate"** → See results instantly!

### 💻 Run the CLI Training Script

```bash
python train.py
```

Prints the full similarity matrix and lists all detected duplicate pairs in the terminal.

---

## 🔬 How It Works

```
 Input Bug Description
         │
         ▼
 ┌─────────────────────┐
 │   Text Cleaning     │  lowercase → remove symbols → remove stopwords
 └─────────────────────┘
         │
         ▼
 ┌─────────────────────┐
 │  TF-IDF Vectorizer  │  converts words → numerical vectors
 └─────────────────────┘
         │
         ▼
 ┌─────────────────────┐
 │  Cosine Similarity  │  compares vectors → score between 0 and 1
 └─────────────────────┘
         │
         ▼
  Score > 0.3 → ⚠️ Possible Duplicate!
  Score ≤ 0.3 → ✅ Likely Unique
```

### Why TF-IDF + Cosine Similarity?

| Approach | Why it works here |
|---|---|
| **TF-IDF** | Gives more weight to unique/important words, ignores common filler words |
| **Cosine Similarity** | Measures angle between vectors — works well even when descriptions have different lengths |
| **Threshold = 0.3** | Tuned to catch paraphrased duplicates without too many false positives |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.8+** | Core language |
| **Streamlit** | Web UI framework |
| **scikit-learn** | TF-IDF vectorization & cosine similarity |
| **NLTK** | Tokenization & stopword removal |
| **Pandas** | Data loading and manipulation |

---

## 📊 Dataset Format

Your `bug_reports.csv` must have these columns:

```csv
id,title,description
1,App crashes on save,Application crashes when clicking save button
2,Save button causes crash,System stops working when save button is pressed
```

You can swap in your own bug dataset — just keep the same column structure!

---

## 🤝 Contributing

Contributions are welcome! Here's how:

```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
git commit -m "Add your feature"
git push origin feature/your-feature-name
# Open a Pull Request 🎉
```

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute.

---

## 👤 Author

**vasanth-1718**  
[![GitHub](https://img.shields.io/badge/GitHub-vasanth--1718-181717?style=flat&logo=github)](https://github.com/vasanth-1718)

---

<div align="center">

⭐ **If this project helped you, give it a star!** ⭐

</div>