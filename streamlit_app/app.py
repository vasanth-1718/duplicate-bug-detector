import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocessing.clean_text import clean_text


DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "bug_reports.csv")

EXAMPLE_BUGS = [
    "Application crashes when clicking save button",
    "Login page freezes after entering credentials",
    "Dark theme not applied correctly",
    "Image upload fails with error",
    "Database connection drops after 30 seconds",
    "API returns 500 error on POST request",
    "Search bar returns empty results for valid keywords",
    "OTP code is not being sent to the user phone",
]


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


def get_confidence(score: float) -> tuple:
    if score >= 0.75:
        return "High Match", "🔴", "error"
    elif score >= 0.45:
        return "Medium Match", "🟠", "warning"
    elif score >= 0.3:
        return "Low Match", "🟡", "info"
    return None, None, None


def show_dashboard(data: pd.DataFrame):
    st.subheader("📊 Bug Report Dashboard")

    total = len(data)
    categories = data["category"].nunique() if "category" in data.columns else "N/A"
    col1, col2, col3 = st.columns(3)
    col1.metric("📁 Total Bug Reports", total)
    col2.metric("🗂️ Categories", categories)
    col3.metric("🧹 Cleaned Records", total)

    st.markdown("---")

    if "category" in data.columns:
        st.markdown("#### 🗂️ Bugs by Category")
        cat_counts = data["category"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Count"]
        st.bar_chart(cat_counts.set_index("Category"))

        st.markdown("#### 📋 Category Summary Table")
        st.dataframe(cat_counts, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🐞 All Bug Reports")
    display_cols = ["id", "title", "category", "description"] if "category" in data.columns else ["id", "title", "description"]
    st.dataframe(data[display_cols], use_container_width=True)


def show_detector(data: pd.DataFrame, vectors, vectorizer):

    # ── How it works banner ───────────────────────────────────────────────────
    with st.expander("💡 How does this work? (click to learn)", expanded=True):
        st.markdown("""
        This tool checks if a bug you're about to report **already exists** in the system.

        **Steps:**
        1. 📝 Type your bug description in the box below
        2. 🔎 Click **Check Duplicate**
        3. 📊 The system compares your bug with **all existing reports**
        4. ✅ You'll see a confidence score telling you how similar they are

        **Confidence levels:**
        | Label | Score | Meaning |
        |---|---|---|
        | 🔴 High Match | ≥ 0.75 | Very likely a duplicate — check before filing! |
        | 🟠 Medium Match | ≥ 0.45 | Possibly related — review carefully |
        | 🟡 Low Match | ≥ 0.30 | Slightly similar — might be a new bug |
        | ✅ No Match | < 0.30 | Unique bug — safe to file! |
        """)

    st.markdown("---")

    # ── Example bugs ──────────────────────────────────────────────────────────
    st.markdown("#### 🧪 Try an Example Bug")
    st.caption("Click any example below to auto-fill the input box 👇")

    cols = st.columns(2)
    for i, example in enumerate(EXAMPLE_BUGS):
        if cols[i % 2].button(f"📌 {example}", key=f"example_{i}", use_container_width=True):
            st.session_state["bug_input"] = example

    st.markdown("---")

    # ── Category filter ───────────────────────────────────────────────────────
    if "category" in data.columns:
        all_categories = ["All"] + sorted(data["category"].unique().tolist())
        selected_category = st.selectbox(
            "🗂️ Filter by Category (optional)",
            all_categories,
            help="Narrow the search to a specific bug category"
        )
    else:
        selected_category = "All"

    # ── Input box ─────────────────────────────────────────────────────────────
    user_input = st.text_area(
        "📝 Enter Bug Description",
        value=st.session_state.get("bug_input", ""),
        height=120,
        placeholder="e.g. The app crashes every time I click the save button on the profile page...",
    )

    char_count = len(user_input.strip())
    if char_count > 0:
        st.caption(f"✏️ {char_count} characters entered")

    if st.button("🔎 Check Duplicate", use_container_width=True, type="primary"):
        if user_input.strip() == "":
            st.warning("⚠️ Please enter a bug description first.")
            return

        if char_count < 10:
            st.warning("⚠️ Description is too short. Please be more descriptive.")
            return

        with st.spinner("🔍 Scanning all bug reports..."):

            if selected_category != "All":
                filtered_data = data[data["category"] == selected_category].reset_index(drop=True)
                filtered_vectors, filtered_vectorizer = build_vectorizer(tuple(filtered_data["cleaned"]))
            else:
                filtered_data = data
                filtered_vectors = vectors
                filtered_vectorizer = vectorizer

            cleaned_input = clean_text(user_input)
            user_vector = filtered_vectorizer.transform([cleaned_input])
            similarity_scores = cosine_similarity(user_vector, filtered_vectors)[0]

        results = []
        for i, score in enumerate(similarity_scores):
            confidence, emoji, alert_type = get_confidence(score)
            if confidence:
                results.append({
                    "Bug ID": filtered_data["id"][i],
                    "Title": filtered_data["title"][i] if "title" in filtered_data.columns else "N/A",
                    "Category": filtered_data["category"][i] if "category" in filtered_data.columns else "N/A",
                    "Description": filtered_data["description"][i],
                    "Score": round(float(score), 2),
                    "Confidence": f"{emoji} {confidence}",
                    "_alert": alert_type,
                })

        results = sorted(results, key=lambda x: x["Score"], reverse=True)

        st.markdown("---")
        st.subheader("📋 Results")

        if not results:
            st.success("✅ Great news! No duplicates found. This looks like a brand new bug — safe to file!")
            st.balloons()
            return

        high = sum(1 for r in results if "High" in r["Confidence"])
        medium = sum(1 for r in results if "Medium" in r["Confidence"])
        low = sum(1 for r in results if "Low" in r["Confidence"])

        st.warning(f"⚠️ Found **{len(results)}** possible duplicate(s) — 🔴 {high} High · 🟠 {medium} Medium · 🟡 {low} Low")

        for r in results:
            alert_fn = getattr(st, r["_alert"])
            alert_fn(
                f"**Bug #{r['Bug ID']}** | {r['Confidence']} | Score: `{r['Score']}`  \n"
                f"**Title:** {r['Title']}  \n"
                f"**Category:** {r['Category']}  \n"
                f"**Description:** {r['Description']}"
            )

        st.markdown("#### 📊 Match Summary Table")
        df_results = pd.DataFrame([{
            "Bug ID": r["Bug ID"],
            "Title": r["Title"],
            "Category": r["Category"],
            "Score": r["Score"],
            "Confidence": r["Confidence"],
        } for r in results])
        st.dataframe(df_results, use_container_width=True)


def main():
    st.set_page_config(
        page_title="Duplicate Bug Detector",
        page_icon="🐞",
        layout="wide"
    )

    st.title("🐞 Duplicate Bug Detection System")
    st.markdown(
        "**Stop filing the same bug twice!** This tool uses AI-powered NLP to instantly check "
        "if your bug report already exists in the system."
    )

    try:
        data = load_data(DATA_PATH)
        vectors, vectorizer = build_vectorizer(tuple(data["cleaned"]))
    except Exception as e:
        st.error("Unable to load data or build the model.")
        st.exception(e)
        return

    # ── Quick stats bar ───────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🐞 Bugs in Database", len(data))
    col2.metric("🗂️ Categories", data["category"].nunique() if "category" in data.columns else "N/A")
    col3.metric("🤖 Model", "TF-IDF + Cosine")
    col4.metric("🎯 Threshold", "0.30")

    st.markdown("---")

    tab1, tab2 = st.tabs(["🔍 Duplicate Detector", "📊 Dashboard"])

    with tab1:
        show_detector(data, vectors, vectorizer)

    with tab2:
        show_dashboard(data)


if __name__ == "__main__":
    main()