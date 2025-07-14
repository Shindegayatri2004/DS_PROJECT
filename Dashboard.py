import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np

st.title("📈 Sustainability Dashboard")

df = pd.read_csv("products.csv")
df['Sustainability Score'] = df[['Recyclable', 'Organic', 'Carbon Neutral']].apply(
    lambda row: sum(x == 'Yes' for x in row), axis=1
)

# 1. Most searched
if os.path.exists("search_log.csv"):
    search_df = pd.read_csv("search_log.csv", header=None, names=["Timestamp", "Term"])
    term_counts = search_df['Term'].value_counts().reset_index()
    term_counts.columns = ['Search Term', 'Count']
    st.subheader("🔍 Most Searched Terms")
    fig1 = px.bar(term_counts.head(5), x='Search Term', y='Count')
    st.plotly_chart(fig1)
else:
    st.info("No search logs yet.")

# 2. Most Eco-Friendly Categories
avg_scores = df.groupby('Category')['Sustainability Score'].mean().sort_values(ascending=False).reset_index()
st.subheader("🌿 Most Eco-Friendly Categories")
fig2 = px.bar(avg_scores, x='Category', y='Sustainability Score', color='Sustainability Score', color_continuous_scale='Greens')
st.plotly_chart(fig2)

# 3. Simulated Monthly Growth
df['Month Added'] = np.random.choice(
    pd.date_range(start='2024-01-01', periods=6, freq='M'),
    size=len(df)
)
monthly_growth = df.groupby(df['Month Added'].dt.strftime('%b %Y')).size().reset_index(name='Products')
st.subheader("📆 Monthly Product Growth")
fig3 = px.line(monthly_growth, x='Month Added', y='Products', markers=True)
st.plotly_chart(fig3)

# KPIs
st.metric("Total Products", len(df))
st.metric("Avg. Sustainability Score", round(df['Sustainability Score'].mean(), 2))
