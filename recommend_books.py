import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches

# Load dataset
df = pd.read_excel('Books_Dataset.xlsx')

# Combine only Author + Genre + Title + Tags
df['metadata'] = df['AUTHOR'].astype(str) + ' ' + df['GENRE'].astype(str) + ' ' + df['TITLE'].astype(str) + ' ' + df['TAGS'].astype(str)

# TF-IDF vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['metadata'])

# Cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Recommendation function
def recommend_books(search_term, top_n=5):
    # Find closest match in Author, Genre, Title, or Tags
    possible_matches = (
        df['AUTHOR'].astype(str).tolist() + 
        df['GENRE'].astype(str).tolist() + 
        df['TITLE'].astype(str).tolist() + 
        df['TAGS'].astype(str).tolist()
    )
    
    match = get_close_matches(search_term, possible_matches, n=1)
    if not match:
        return pd.DataFrame(columns=['TITLE', 'AUTHOR', 'Type'])  # Empty DataFrame if no match
    
    # Get all books that contain this match in metadata
    matched_books = df[df['metadata'].str.contains(match[0], case=False, na=False)]
    if matched_books.empty:
        return pd.DataFrame(columns=['TITLE', 'AUTHOR', 'Type'])
    
    # Take the first matched index
    idx = matched_books.index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Skip the book itself and take top_n
    sim_scores = sim_scores[1:top_n+1]
    recommended_books = [df['TITLE'].iloc[i[0]] for i in sim_scores]
    recommended_authors = [df['AUTHOR'].iloc[i[0]] for i in sim_scores]
    
    return pd.DataFrame({
      'TITLE': recommended_books,
      'AUTHOR': recommended_authors
    })

# Combined recommendation
def recommend_books_combined(search_genre=None, search_author=None, search_title=None, search_tags=None, top_n=5):
    results = []

    if search_genre:
        genre_rec = recommend_books(search_genre, top_n)
        genre_rec['Type'] = 'Genre-based'
        results.append(genre_rec)

    if search_author:
        author_rec = recommend_books(search_author, top_n)
        author_rec['Type'] = 'Author-based'
        results.append(author_rec)

    if search_title:
        title_rec = recommend_books(search_title, top_n)
        title_rec['Type'] = 'Title-based'
        results.append(title_rec)

    if search_tags:
        tags_rec = recommend_books(search_tags, top_n)
        tags_rec['Type'] = 'Tags-based'
        results.append(tags_rec)

    if results:
        return pd.concat(results, ignore_index=True)
    else:
        return pd.DataFrame(columns=['TITLE', 'AUTHOR', 'Type'])

# Run combined recommendation
print(recommend_books_combined("Thriller", "Thomas Gates", "Some Title", "Adventure", top_n=5))

# Example: "Thriller, Fantasy" 
search_terms = "Thriller, Fantasy".split(", ")
for term in search_terms:
    print(recommend_books(term))
