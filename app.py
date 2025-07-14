import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# 🔽 Load CSV with error handling and sustainability score
try:
    df = pd.read_csv("products.csv", on_bad_lines='skip')
    df['Sustainability Score'] = df[['Recyclable', 'Organic', 'Carbon Neutral']].apply(
        lambda row: sum(x == 'Yes' for x in row), axis=1
    )
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()  # Stops app if critical error occurs

# Page Config
st.set_page_config(page_title="Eco-Friendly Product Recommender", layout="wide")

# Dataset Loading
df['Sustainability Score'] = df[['Recyclable', 'Organic', 'Carbon Neutral']].apply(
    lambda row: sum(x == 'Yes' for x in row), axis=1
)


# TF-IDF Vectorization
df['combined_features'] = df[['Product Name', 'Category']].fillna('').agg(' '.join, axis=1)
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['combined_features'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


# Recommendation Function
def get_recommendations(product_name, top_n=3):
    if product_name not in df['Product Name'].values:
        return pd.DataFrame(columns=['Product Name', 'Sustainability Score', 'Price'])
    idx = df[df['Product Name'] == product_name].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    recommended_indices = [i[0] for i in sim_scores]
    return df.loc[recommended_indices][['Product Name', 'Sustainability Score', 'Price']]

# Navigation State
page_order = ['main', 'comparison', 'charts', 'dashboard', 'recommend','add_product','feedback', 'thankyou']
if 'page_index' not in st.session_state:
    st.session_state.page_index = 0
current_page = page_order[st.session_state.page_index]

# -------------------- Universal Top Navigation --------------------
if current_page != 'thankyou':
    
    visible_pages = page_order[:-1]  # Exclude 'thankyou'
    current_index = min(st.session_state.page_index, len(visible_pages) - 1)

    section = st.radio(
    label="",
    options=visible_pages,
    index=current_index,
    horizontal=True
)

    # Jump only if user selected a different page
    new_index = visible_pages.index(section)
    if new_index != st.session_state.page_index:
        st.session_state.page_index = new_index
        st.rerun()



# Navigation Controls
def go_next():
    if st.session_state.page_index < len(page_order) - 1:
        st.session_state.page_index += 1
        st.rerun()

def go_back():
    if st.session_state.page_index > 0:
        st.session_state.page_index -= 1
        st.rerun()

# ----------------------- MAIN PAGE -----------------------
if current_page == 'main':
    st.title("🌿 Eco-Friendly Product Recommender")
    st.markdown("Welcome to your personal sustainability assistant! Use filters to find eco-friendly products.")

    with st.sidebar:
        st.header("🔍 Search Products")
        search_term = st.text_input("Enter product name")
        search_button = st.button("🔍 Search")
        st.markdown("---")
        st.header("🔎 Filter Options")
        category = st.selectbox("Select Product Category", sorted(df['Category'].unique()))
        recyclable = st.checkbox("♻️ Recyclable Only")
        organic = st.checkbox("🌿 Organic Only")
        carbon = st.checkbox("🌍 Carbon Neutral Only")
        sort_option = st.selectbox("Sort by", ['None', 'Price (Low to High)', 'Price (High to Low)', 'Sustainability Score'])
        show_all = st.button("📋 Show All Products")

    if search_button and search_term:
        filtered = df[df['Product Name'].str.contains(search_term, case=False)]
        st.subheader(f"🔍 Search Results for '{search_term}'")
        try:
            with open("search_log.csv", "a", encoding="utf-8") as log_file:
                log_file.write(f"{datetime.datetime.now()},{search_term}\n")
        except Exception as e:
            st.error(f"Error logging search term: {e}")
    elif show_all:
        filtered = df.copy()
        st.subheader("📋 All Products (No Filters Applied)")
    else:
        filtered = df[df['Category'] == category]
        if recyclable:
            filtered = filtered[filtered['Recyclable'] == 'Yes']
        if organic:
            filtered = filtered[filtered['Organic'] == 'Yes']
        if carbon:
            filtered = filtered[filtered['Carbon Neutral'] == 'Yes']
        st.subheader(f"🛍️ Products in '{category}' Category")

    if sort_option == 'Price (Low to High)':
        filtered = filtered.sort_values('Price')
    elif sort_option == 'Price (High to Low)':
        filtered = filtered.sort_values('Price', ascending=False)
    elif sort_option == 'Sustainability Score':
        filtered = filtered.sort_values('Sustainability Score', ascending=False)

    if not filtered.empty:
        st.dataframe(filtered[['Product Name', 'Recyclable', 'Organic', 'Carbon Neutral', 'Sustainability Score', 'Price']])
    else:
        st.warning("⚠️ No products match the selected filters.")
        suggestion = df[df['Sustainability Score'] >= 2].sample(min(3, len(df)))
        st.info("Try these alternatives:")
        st.table(suggestion[['Product Name', 'Sustainability Score', 'Price']])

    st.subheader("🌟 Top Eco-Friendly Picks")
    top_picks = df[df['Sustainability Score'] == 3].sort_values('Price').head(3)
    st.table(top_picks[['Product Name', 'Price', 'Sustainability Score']])

# ----------------------- COMPARISON PAGE -----------------------
elif current_page == 'comparison':
    st.subheader("📊 Compare Products")
    selected = st.multiselect("Select products:", df['Product Name'].unique())
    if st.button("🔍 Compare"):
        if len(selected) < 2:
            st.warning("Select at least 2 products.")
        else:
            compare_df = df[df['Product Name'].isin(selected)]
            cols = st.columns(len(selected))
            for col, (_, row) in zip(cols, compare_df.iterrows()):
                with col:
                    st.markdown(f"### {row['Product Name']}")
                    st.write(f"Category: {row['Category']}")
                    st.write(f"Price: ₹{row['Price']}")
                    st.write(f"Sustainability Score: {row['Sustainability Score']}")

# ----------------------- CHARTS PAGE -----------------------
elif current_page == 'charts':
    st.title("📊 Charts and Insights")

    # --- Histogram: Sustainability Score Distribution ---
    st.subheader("📉 Sustainability Score Distribution")
    score_counts = df['Sustainability Score'].value_counts().sort_index()
    fig, ax = plt.subplots()
    score_counts.plot.bar(
        ax=ax,
        color=['#e74c3c', '#f39c12', '#27ae60', '#2ecc71'],
        edgecolor='black'
    )
    ax.set_xlabel("Score (0 = Low, 3 = High)")
    ax.set_ylabel("Number of Products")
    ax.set_title("Sustainability Score Distribution")
    st.pyplot(fig)

    # --- Bar Chart: Average Score by Category ---
    st.subheader("📂 Average Sustainability Score by Category")
    cat_avg = df.groupby('Category')['Sustainability Score'].mean().sort_values()
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    cat_avg.plot(kind='bar', ax=ax2, color="#2ecc71", edgecolor="black")
    ax2.set_ylabel("Average Score")
    ax2.set_xlabel("Product Category")
    ax2.set_title("Average Sustainability Score by Category")
    st.pyplot(fig2)

    # --- Pie Chart: Feature Spread ---
    st.subheader("🥧 Sustainability Feature Spread")
    labels = ['Recyclable', 'Organic', 'Carbon Neutral']
    sizes = [df[col].value_counts().get('Yes', 0) for col in labels]
    fig3, ax3 = plt.subplots()
    ax3.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#2ecc71', '#27ae60', '#16a085'])
    ax3.axis('equal')
    st.pyplot(fig3)


# ----------------------- DASHBOARD PAGE -----------------------
elif current_page == 'dashboard':
    st.subheader("📈 Dashboard Overview")
    st.metric("Total Products", len(df))
    st.metric("Avg. Sustainability Score", round(df['Sustainability Score'].mean(), 2))
    st.bar_chart(df["Sustainability Score"])

# ----------------------- RECOMMEND PAGE -----------------------
elif current_page == 'recommend':
    st.subheader("🤖 Recommended for You")
    product = st.selectbox("Choose a product:", df['Product Name'].unique())
    if st.button("💡 Show Recommendations"):
        recs = get_recommendations(product)
        st.table(recs)



elif current_page == 'add_product':
    st.title("➕ Add Your Eco-Friendly Product")

    with st.form("product_form"):
        name = st.text_input("Product Name")
        category = st.selectbox("Category", sorted(df['Category'].unique()))
        price = st.number_input("Price (₹)", min_value=0.0, step=1.0)
        recyclable = st.selectbox("Is it Recyclable?", ["Yes", "No"])
        organic = st.selectbox("Is it Organic?", ["Yes", "No"])
        carbon_neutral = st.selectbox("Is it Carbon Neutral?", ["Yes", "No"])

        submitted = st.form_submit_button("Submit")

        if submitted:
            new_product = {
                'Product Name': name,
                'Category': category,
                'Price': price,
                'Recyclable': recyclable,
                'Organic': organic,
                'Carbon Neutral': carbon_neutral
            }

            # Calculate score
            new_product['Sustainability Score'] = sum(x == 'Yes' for x in [recyclable, organic, carbon_neutral])

            try:
                # Append to CSV
                pd.DataFrame([new_product]).to_csv("products.csv", mode='a', header=False, index=False)
                st.success("✅ Product added successfully!")
            except Exception as e:
                st.error(f"❌ Failed to add product: {e}")


# ----------------------- FEEDBACK PAGE ------------------
elif current_page == 'feedback':
    st.subheader("📝 Feedback")
    with st.form("feedback_form"):
        name = st.text_input("Your Name")
        comment = st.text_area("Your Feedback")
        if st.form_submit_button("Submit"):
            with open("feedback.txt", "a") as f:
                f.write(f"{name}: {comment}\n")
            st.success("Thank you for your feedback!")
            st.session_state.page_index = page_order.index('thankyou')
            st.rerun()  # rerun to show thankyou page
            st.stop()   # ⛔ prevent rest of code from running

# ----------------------- THANK YOU PAGE -----------------------
elif current_page == 'thankyou':
    st.success("🎉 Thank you for your valuable feedback!")
    st.markdown("""

                    Your suggestions help us improve and grow greener together. 🌱

    Feel free to return to the home page or explore other sections.
    """)
    st.image("https://media.giphy.com/media/l0MYKDrf6U7JjzjH6/giphy.gif", width=300)

    st.markdown("### 🔙 Return Options")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🏠 Back to Home Page"):
            st.session_state.page_index = 0  # index of 'main'
            st.rerun()
    with col2:
        if st.button("🔁 Explore Again"):
            st.session_state.page_index = 1  # index of 'comparison' or wherever you want
            st.rerun()
# ----------------------- Navigation -----------------------
st.markdown("---")
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Back"):
        go_back()
with col2:
    if st.button("➡️ Next"):
        go_next()

st.caption("Created with 💚 by Team ECO-DUO | Powered by Streamlit")
