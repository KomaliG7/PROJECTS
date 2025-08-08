import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv("learning_resources_large.csv")


df['text'] = df['title'] + " " + df['description'] + " " + df['subject']


vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['text'])


def get_recommendations_from_query(user_query, top_n=5):
    query_vector = vectorizer.transform([user_query])
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    top_indices = similarities.argsort()[-top_n:][::-1]
    return df[['title', 'url', 'subject', 'difficulty', 'description']].iloc[top_indices].to_dict(orient='records')

if __name__ == "__main__":
    query = "I want to learn about algebra or math equations"
    results = get_recommendations_from_query(query)
    for res in results:
        print(res)




