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
    books_df = pd.read_excel("../Books_Dataset.xlsx")
 # adjust path if needed
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

# -----------------------------
# Sidebar Search
# -----------------------------
st.sidebar.header("Search Books")
# query = st.sidebar.text_input("Enter book Title, Author, Genre, or Tags")
# Collect unique options from dataset
book_titles = books_df['title'].dropna().unique().tolist()
authors = books_df['author'].dropna().unique().tolist()
genres = books_df['genre'].dropna().unique().tolist()

# Combine into one dropdown list
options = [""] + book_titles + authors + genres

# Sidebar dropdown
query = st.sidebar.selectbox("🔍 Choose a book, author, or genre", options)



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
# Initial First Page (when no search input)
# -----------------------------
images = [
    "../Page_Cover/Handbook.jpg",
    "../Page_Cover/read.jpg",
    "../Page_Cover/Harry Potter.jpg"
]

if not query:  
    # st.image(images,width=250) #replace with your image file

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(images[0], use_container_width=True)
    with col2:
        st.image(images[1], use_container_width=True)
    with col3:
        st.image(images[2], use_container_width=True)


    st.markdown(
        "<h3 style='text-align:center; color:#BDB82A;'>Welcome to the Book Recommender 📖</h3>",
        unsafe_allow_html=True
    )

    st.write("👉 Start by typing a title, author, genre, or tags in the sidebar to see recommendations.")

# -----------------------------
# Tabs for Recommendations
# -----------------------------
tab1, tab2 = st.tabs(["Content-Based", "Top Rated / Matrix Factorization"])

with tab1:
    st.subheader("Content-Based Recommendations")
    recs = content_based_recs(query)
    if recs:
        for book in recs:
            # Book Title in #BDB82A
            st.markdown(f"<h3 style='color:#BDB82A;'>{book['title']}</h3>", unsafe_allow_html=True)
            st.markdown(f"**Author:** {book['author']} | **Genre:** {book['genre']} | ⭐ {book.get('rating', 'N/A')}")
            st.markdown(f"*Summary:* {book.get('summary','')[:200]}...")
            st.markdown("---")
    else:
        if query:  # only show this if user typed something
            st.warning("No matching books found.")

with tab2:
    st.subheader("Top Rated Books")
    recs = top_rated_recs()
    for book in recs:
        # Book Title in #33308C
        st.markdown(f"<h3 style='color:#BDB82A;'>{book['title']}</h3>", unsafe_allow_html=True)
        st.markdown(f"**Author:** {book['author']} | **Genre:** {book['genre']} | ⭐ {book.get('rating','N/A')}")
        st.markdown(f"*Summary:* {book.get('summary','')[:200]}...")
        st.markdown("---")
