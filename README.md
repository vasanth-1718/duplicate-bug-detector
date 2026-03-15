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
- 🎯 **Confidence level labels** — results labeled as 🔴 High / 🟠 Medium / 🟡 Low match
- 🧪 **Example bug buttons** — click to auto-fill input, great for first-time users
- 📊 **Live dashboard** — bar charts, category stats, and full bug table in one view
- 🗂️ **Category filter** — narrow search to UI, Auth, Backend, or Database bugs
- 🖥️ **Wide Streamlit UI** — clean two-tab layout with onboarding guide built in
- 56 real-world bug reports across 4 categories out of the box

---

## 🎬 Demo

```
Input:  "Login page freezes after entering credentials"

Results:
  🔴 High Match   | Bug 3  | Score: 1.00 | "Login page freezes after entering credentials"
  🟠 Medium Match | Bug 4  | Score: 0.42 | "System hangs when submitting login form"

✅ Summary: 2 duplicates found — 🔴 1 High · 🟠 1 Medium · 🟡 0 Low
```

---

## 📁 Project Structure

```
duplicate-bug-detector/
│
├── 📂 data/
│   └── bug_reports.csv          # 56 bug reports across 4 categories
│
├── 📂 preprocessing/
│   ├── __init__.py
│   └── clean_text.py            # NLP text cleaning pipeline
│
├── 📂 streamlit_app/
│   ├── __init__.py
│   └── app.py                   # Streamlit web UI (2-tab layout)
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

### 2. Fix SSL certificates (Mac only — one time)

```bash
/Applications/Python\ 3.*/Install\ Certificates.command
```

### 3. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### 🖥️ Run the Web App

```bash
streamlit run streamlit_app/app.py
```

Opens at `http://localhost:8501` — type a bug → click **Check Duplicate** → see results instantly!

### 💻 Run the CLI Training Script

```bash
python train.py
```

Prints the full similarity matrix, category breakdown, and all detected duplicate pairs in the terminal.

### 🔁 Every time you reopen the project

```bash
source venv/bin/activate
streamlit run streamlit_app/app.py
```

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
  🔴 Score ≥ 0.75 → High Match
  🟠 Score ≥ 0.45 → Medium Match
  🟡 Score ≥ 0.30 → Low Match
  ✅ Score < 0.30 → Unique Bug
```

### Why TF-IDF + Cosine Similarity?

| Approach | Why it works here |
|---|---|
| **TF-IDF** | Gives more weight to unique/important words, ignores common filler words |
| **Cosine Similarity** | Measures angle between vectors — works well even when descriptions have different lengths |
| **Threshold = 0.3** | Tuned to catch paraphrased duplicates without too many false positives |

---

## 📊 Dataset

56 bug reports across 4 categories, each with realistic duplicates built in:

| Category | # Bugs | Examples |
|---|---|---|
| **UI** | 20 | crashes, layout, dark mode, pagination |
| **Auth** | 14 | login, OTP, session, JWT, roles |
| **Backend** | 14 | API errors, payments, exports, emails |
| **Database** | 8 | timeouts, slow queries, insert failures |

### CSV format:

```csv
id,title,description,category
1,App crashes on save,Application crashes when clicking save button,UI
2,Save button causes crash,System stops working when save button is pressed,UI
```

You can swap in your own dataset — just keep the same column structure!

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