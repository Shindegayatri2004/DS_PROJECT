import streamlit as st
import pandas as pd
from utils.recommendation import get_recommendations

df = pd.read_csv("products.csv")
df['Sustainability Score'] = df[['Recyclable', 'Organic', 'Carbon Neutral']].apply(
    lambda row: sum(x == 'Yes' for x in row), axis=1
)

st.title("🤖 Product Recommendations")

selected_product = st.selectbox("Choose a product:", df['Product Name'].unique())

if st.button("💡 Show Recommendations"):
    recs = get_recommendations(selected_product, df)
    if not recs.empty:
        st.table(recs)
    else:
        st.info("No recommendations found.")

st.header("🌿 Other Highly Sustainable Products")
st.dataframe(df[df['Sustainability Score'] >= 2])
