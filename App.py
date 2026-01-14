import streamlit as st
import google.generativeai as genai

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="NJ Tech Assistant",
    page_icon="📱",
    layout="centered"
)

# ---------- LOAD API KEY ----------
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ Gemini API Key missing. Please add it in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# ---------- MODEL ----------
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""
You are NJ Tech Assistant.
Speak like a friendly Coimbatore-based tech expert.
Give short, clear, customer-friendly answers.
Always add a personal touch.
"""
)

# ---------- UI ----------
st.title("📱 NJ Tech Assistant")
st.caption("🚀 Powered by Gemini 1.5 Flash")

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# ---------- CHAT HISTORY ----------
for msg in st.session_state.chat.history:
    role = "assistant" if msg.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(msg.parts[0].text)

# ---------- USER INPUT ----------
user_input = st.chat_input("Customer enna kettaanga...?")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = st.session_state.chat.send_message(user_input)

        with st.chat_message("assistant"):
            st.markdown(response.text)

    except Exception as e:
        st.error(f"⚠️ Something went wrong: {e}")
