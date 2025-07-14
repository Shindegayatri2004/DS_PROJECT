import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendations(product_name, df, top_n=3):
    df['combined_features'] = df[['Product Name', 'Category']].fillna('').agg(' '.join, axis=1)
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['combined_features'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    if product_name not in df['Product Name'].values:
        return pd.DataFrame()

    idx = df[df['Product Name'] == product_name].index[0]
    sim_scores = sorted(list(enumerate(cosine_sim[idx])), key=lambda x: x[1], reverse=True)[1:top_n+1]
    indices = [i[0] for i in sim_scores]
    return df.loc[indices][['Product Name', 'Sustainability Score', 'Price']]
