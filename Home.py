import streamlit as st


st.title('Jakey AI')

"Welcome to Jakey AI"

st.markdown(
"""
### Here are the things you can do to get started:
- Ask real questions
- Get complete answers
- Analyze images

Chat with models:
"""
)

if st.button(label="OpenAI's ChatGPT"):
    st.switch_page("pages/OpenAI.py")