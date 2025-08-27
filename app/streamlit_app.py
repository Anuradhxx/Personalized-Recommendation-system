import streamlit as st
import pandas as pd

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Book Recommender", layout="wide")
st.title("📚 Personalized Book Recommendation System")

# -----------------------------
# Load Dataset
# -----------------------------
try:
    books_df = pd.read_excel("../Books_Dataset.xlsx")  # adjust path if needed
except FileNotFoundError:
    st.error("Books_Dataset.xlsx not found. Please check the path.")
    st.stop()

# -----------------------------
# Normalize column names
# -----------------------------
books_df.columns = (
    books_df.columns
    .str.strip()           # remove extra spaces
    .str.lower()           # lowercase
    .str.replace(r'[^\w]', '_', regex=True)  # replace non-word characters with underscore
)

# Optional: display columns for debugging
# st.write("Columns detected:", books_df.columns.tolist())

# -----------------------------
# Sidebar Search
# -----------------------------
st.sidebar.header("Search Books")
query = st.sidebar.text_input("Enter book title, author, genre, or tags")

# -----------------------------
# Recommendation Functions
# -----------------------------
def content_based_recs(query, n=5):
    if not query:
        return []
    matches = books_df[
        books_df['title'].str.contains(query, case=False, na=False) |
        books_df['author'].str.contains(query, case=False, na=False) |
        books_df['genre'].str.contains(query, case=False, na=False) |
        books_df['tags'].str.contains(query, case=False, na=False)
    ]
    return matches.head(n).to_dict('records')

def top_rated_recs(n=5):
    if 'rating' in books_df.columns:
        top_books = books_df.sort_values('rating', ascending=False).head(n)
        return top_books.to_dict('records')
    else:
        return books_df.sample(n).to_dict('records')  # fallback

# -----------------------------
# Tabs for Recommendations
# -----------------------------
tab1, tab2 = st.tabs(["Content-Based", "Top Rated / Matrix Factorization"])

with tab1:
    st.subheader("Content-Based Recommendations")
    recs = content_based_recs(query)
    if recs:
        for book in recs:
            st.markdown(f"### {book['title']}")
            st.markdown(f"**Author:** {book['author']} | **Genre:** {book['genre']} | ⭐ {book.get('rating', 'N/A')}")
            st.markdown(f"*Summary:* {book.get('summary','')[:200]}...")
            st.markdown("---")
    else:
        st.write("Enter a search term to see recommendations.")

with tab2:
    st.subheader("Top Rated Books")
    recs = top_rated_recs()
    for book in recs:
        st.markdown(f"### {book['title']}")
        st.markdown(f"**Author:** {book['author']} | **Genre:** {book['genre']} | ⭐ {book.get('rating','N/A')}")
        st.markdown(f"*Summary:* {book.get('summary','')[:200]}...")
        st.markdown("---")
