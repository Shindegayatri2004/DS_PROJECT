# pages/6_🎉_ThankYou.py

import streamlit as st

# --- Optional Page Config ---
st.set_page_config(page_title="Thank You", layout="centered")

# --- Success Message ---
st.success("🎉 Thank you for your valuable feedback!")

# --- Appreciation Content ---
st.markdown("""
### 🙏 We appreciate your time!
Your suggestions help us improve and grow greener together. 🌱

Feel free to return to the home page or explore other sections.
""")

# --- Thank You Image / GIF ---
st.image("https://media.giphy.com/media/l0MYKDrf6U7JjzjH6/giphy.gif", width=300)

# --- Navigation Buttons ---
cols = st.columns([1, 1])
with cols[0]:
    if st.button("🏠 Return to Home"):
        st.switch_page("app.py")  # Navigates to the main page
with cols[1]:
    if st.button("🔁 Explore Again"):
        st.switch_page("pages/2_🤖_Recommend.py")  # Or any other section you prefer
