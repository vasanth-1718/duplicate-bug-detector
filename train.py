import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocessing.clean_text import clean_text

# load dataset
data = pd.read_csv("data/bug_reports.csv")

# clean descriptions
data["cleaned"] = data["description"].apply(clean_text)

print("\nCleaned Bug Reports:\n")
print(data[["id", "cleaned"]])

# convert text to vectors
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(data["cleaned"])

# calculate similarity
similarity_matrix = cosine_similarity(vectors)

print("\nSimilarity Matrix:\n")
print(similarity_matrix)

# find duplicates
threshold = 0.3

print("\nPossible Duplicate Bugs:\n")

for i in range(len(data)):
    for j in range(i + 1, len(data)):
        if similarity_matrix[i][j] > threshold:
            print(
                f"Bug {data['id'][i]} and Bug {data['id'][j]} "
                f"are similar (score={similarity_matrix[i][j]:.2f})"
            )
