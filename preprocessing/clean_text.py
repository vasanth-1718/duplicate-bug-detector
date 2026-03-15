#!/usr/bin/env python

import importlib
import re
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
REQ_FILE = ROOT_DIR / "requirements.txt"


def _install_requirements():
    if not REQ_FILE.exists():
        raise FileNotFoundError(
            f"Cannot auto-install dependencies because {REQ_FILE} does not exist.\n"
            "Please create a requirements.txt and install manually."
        )

    print(f"Installing dependencies from {REQ_FILE} using {sys.executable}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(REQ_FILE)])


def _ensure_nltk():
    try:
        import nltk
    except ImportError:
        _install_requirements()


_ensure_nltk()

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# download resources if missing
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

stop_words = set(stopwords.words('english'))


def clean_text(text):

    # lowercase
    text = text.lower()

    # remove numbers and special characters
    text = re.sub(r'[^a-zA-Z ]', '', text)

    # tokenize words
    tokens = word_tokenize(text)

    # remove stopwords
    filtered = [word for word in tokens if word not in stop_words]

    # join words again
    cleaned_text = " ".join(filtered)

    return cleaned_text


if __name__ == "__main__":

    sample = "Application crashes when clicking save button!"

    result = clean_text(sample)

    print("Original:", sample)
    print("Cleaned :", result)