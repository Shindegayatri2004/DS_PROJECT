import streamlit as st
import pandas as pd

df = pd.read_csv("products.csv")
df['Sustainability Score'] = df[['Recyclable', 'Organic', 'Carbon Neutral']].apply(
    lambda row: sum(x == 'Yes' for x in row), axis=1
)

st.title("⚖️ Product Comparison")

selected = st.multiselect("Select at least 2 products to compare:", df['Product Name'].unique())

if len(selected) >= 2:
    comp_df = df[df['Product Name'].isin(selected)]
    avg_scores = df.groupby('Category')['Sustainability Score'].mean().to_dict()

    cols = st.columns(len(selected))
    for col, (_, row) in zip(cols, comp_df.iterrows()):
        with col:
            st.markdown(f"### {row['Product Name']}")
            st.write(f"**Category:** {row['Category']}")
            st.write(f"**Price:** ₹{row['Price']}")
            st.markdown(f"- ♻️ Recyclable: `{row['Recyclable']}`")
            st.markdown(f"- 🌿 Organic: `{row['Organic']}`")
            st.markdown(f"- 🌍 Carbon Neutral: `{row['Carbon Neutral']}`")
            st.write(f"**Score:** {row['Sustainability Score']}")
            st.info(f"Category Avg: {avg_scores.get(row['Category'], 0):.2f}")
else:
    st.info("Select at least 2 products to view comparison.")
