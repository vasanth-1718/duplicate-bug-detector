import os
import sys

# Fix import path so Streamlit can access preprocessing module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocessing.clean_text import clean_text


DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "bug_reports.csv")


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path)
    df["cleaned"] = df["description"].apply(clean_text)
    return df


@st.cache_data
def build_vectorizer(texts):
    vec = TfidfVectorizer()
    return vec.fit_transform(texts), vec


def main():
    st.set_page_config(page_title="Duplicate Bug Detector", page_icon="🐞")

    st.title("🐞 Duplicate Bug Detection System")

    st.write("Enter a bug description to check if a similar bug already exists.")

    try:
        data = load_data(DATA_PATH)
        vectors, vectorizer = build_vectorizer(data["cleaned"])
    except Exception as e:
        st.error("Unable to load data or build the model.")
        st.exception(e)
        return

    user_input = st.text_area("Enter Bug Description")

    if st.button("Check Duplicate"):
        if user_input.strip() == "":
            st.warning("Please enter a bug description.")
            return

        cleaned_input = clean_text(user_input)
        user_vector = vectorizer.transform([cleaned_input])
        similarity_scores = cosine_similarity(user_vector, vectors)[0]

        st.subheader("Similarity Results")
        threshold = 0.3
        found_duplicate = False

        for i, score in enumerate(similarity_scores):
            bug_id = data["id"][i]
            bug_desc = data["description"][i]

            st.write(f"Bug {bug_id} → similarity score: **{score:.2f}**")

            if score > threshold:
                found_duplicate = True
                st.success(f"Possible duplicate of Bug {bug_id}: {bug_desc}")

        if not found_duplicate:
            st.info("No strong duplicates found.")


if __name__ == "__main__":
    main()
