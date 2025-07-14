import streamlit as st

st.title("📝 Feedback")

with st.form("feedback_form"):
    name = st.text_input("Your Name")
    comment = st.text_area("Your Feedback")
    if st.form_submit_button("Submit"):
        with open("feedback.txt", "a") as f:
            f.write(f"{name}: {comment}\n")
        st.success("Thanks for your feedback!")

st.subheader("📬 Additional Comments")
st.text_area("Drop more ideas or suggestions:")
