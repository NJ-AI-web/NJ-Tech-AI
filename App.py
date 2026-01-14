import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="NJ Tech AI", page_icon="🤖")
st.title("📱 NJ Tech Assistant")
st.caption("🚀 Powered by Gemini Pro")

# 1. API Key Check
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("API Key காணவில்லை! Secrets-ல் செக் செய்யவும்.")
    st.stop()

# 2. Configure Gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport="rest")

# 3. Model Setup (நாம் மீண்டும் பழைய, ஆனால் உறுதியான மாடலுக்கே வருகிறோம்)
model = genai.GenerativeModel('gemini-pro')

# 4. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "user", "content": "You are NJ Bot for NJ Tech mobile shop. Speak in Tanglish."})
    st.session_state.messages.append({"role": "assistant", "content": "வணக்கம்! நான் NJ Bot. எப்படி உதவலாம்?"})

# 5. Display Messages
for message in st.session_state.messages[2:]:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["content"])

# 6. User Input
if prompt := st.chat_input("கேளுங்க..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        gemini_history = [{"role": "user" if m["role"]=="user" else "model", "parts": [m["content"]]} for m in st.session_state.messages]
        try:
            response = model.generate_content(gemini_history)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
