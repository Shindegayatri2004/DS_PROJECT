import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("products.csv")

# Calculate Sustainability Score if not present
if 'Sustainability Score' not in df.columns:
    df['Sustainability Score'] = df[['Recyclable', 'Organic', 'Carbon Neutral']].apply(
        lambda row: sum(x == 'Yes' for x in row), axis=1
    )

st.set_page_config(page_title="📈 Charts", layout="wide")
st.title("📊 Sustainability Charts & Insights")

# --- 1. Histogram: Sustainability Score Distribution ---
st.subheader("📉 Sustainability Score Distribution")
score_counts = df['Sustainability Score'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.bar(score_counts.index, score_counts.values,
            color=['#e74c3c', '#f39c12', '#27ae60', '#2ecc71'],
            edgecolor='black')
ax.set_xlabel("Sustainability Score (0 = Low, 3 = High)", fontsize=12)
ax.set_ylabel("Number of Products", fontsize=12)
ax.set_title("🌿 Eco-Friendliness of Products", fontsize=14, fontweight='bold')
ax.set_xticks([0, 1, 2, 3])
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5), textcoords="offset points", ha='center', fontsize=10)
ax.grid(axis='y', linestyle='--', alpha=0.6)
st.pyplot(fig)

# --- 2. Bar Chart: Category-wise Average Sustainability Score ---
st.subheader("📂 Average Sustainability Score by Category")
category_avg = df.groupby('Category')['Sustainability Score'].mean().sort_values()
fig2, ax2 = plt.subplots(figsize=(10, 4))
category_avg.plot(kind='bar', ax=ax2, color="#2ecc71", edgecolor="black")
ax2.set_title("📦 Categories with Higher Eco Scores", fontsize=13)
ax2.set_ylabel("Average Score")
ax2.set_xlabel("Product Category")
for i, val in enumerate(category_avg):
    ax2.text(i, val + 0.02, f"{val:.2f}", ha='center', va='bottom', fontsize=9)
st.pyplot(fig2)

# --- 3. Pie Chart: Sustainability Feature Spread ---
st.subheader("🥧 Sustainability Feature Spread")
labels = ['Recyclable', 'Organic', 'Carbon Neutral']
sizes = [df[col].value_counts().get('Yes', 0) for col in labels]
fig3, ax3 = plt.subplots()
ax3.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
        colors=['#2ecc71', '#27ae60', '#16a085'], textprops={'fontsize': 10})
ax3.set_title("♻️ Feature-wise Distribution", fontsize=13)
ax3.axis('equal')
st.pyplot(fig3)

# Optional: Add a summary note
st.markdown("---")
st.info("These charts provide a high-level overview of product sustainability and category performance. Use this data to guide your eco-friendly choices!")
