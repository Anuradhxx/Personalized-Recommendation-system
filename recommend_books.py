
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches

# Load dataset
df = pd.read_excel('Books_Dataset.xlsx')

# Combine only Author + Genre for recommendation
df['metadata'] = df['AUTHOR'] + ' ' + df['GENRE']

# print(df[['TITLE', 'metadata']].head())

# TF-IDF vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['metadata'])

# Cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Recommendation function
def recommend_books(search_term, top_n=5):
    # Find closest match in Author or Genre
    possible_matches = df['AUTHOR'].tolist() + df['GENRE'].tolist()
    match = get_close_matches(search_term, possible_matches, n=1)
    if not match:
        return "No matching author or genre found."
    
    # Get all books that contain this match in metadata
    matched_books = df[df['metadata'].str.contains(match[0], case=False)]
    
    # If multiple matches, calculate similarity for each
    idx = matched_books.index[0]  # pick the first match
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Skip the book itself and take top_n
    sim_scores = sim_scores[1:top_n+1]
    recommended_books = [df['TITLE'].iloc[i[0]] for i in sim_scores]
    recommended_authors = [df['AUTHOR'].iloc[i[0]] for i in sim_scores]
    

# New return (row-wise)
    return pd.DataFrame({
      'TITLE': recommended_books,
      'AUTHOR': recommended_authors
})


# Example usage
def recommend_books_combined(search_genre, search_author, top_n=5):
    # Genre-based recommendations
    genre_rec = recommend_books(search_genre, top_n)
    genre_rec['Type'] = 'Genre-based'
    
    # Author-based recommendations
    author_rec = recommend_books(search_author, top_n)
    author_rec['Type'] = 'Author-based'
    
    # Combine both
    combined = pd.concat([genre_rec, author_rec], ignore_index=True)
    return combined


# Run combined recommendation
print(recommend_books_combined("Thriller", "Thomas Gates", top_n=5))

# Example: "Thriller, Fantasy" 
search_terms = "Thriller, Fantasy".split(", ")
for term in search_terms:
    print(recommend_books(term))
