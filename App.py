import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="NJ Tech AI", page_icon="🤖")
st.title("📱 NJ Tech Assistant")
st.caption("🚀 Powered by Gemini AI")

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Please set the GOOGLE_API_KEY in Streamlit secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

system_prompt = """
You are 'NJ Bot' for NJ Tech mobile shop.
Answer in Tanglish. Be polite.
"""
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    role = "user" if m["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(m["content"])

if prompt := st.chat_input("Say Hi..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        gemini_history = [{"role": "user" if m["role"]=="user" else "model", "parts": [m["content"]]} for m in st.session_state.messages]
        response = model.generate_content(gemini_history)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
