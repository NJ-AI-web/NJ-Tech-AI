import streamlit as st
import google.generativeai as genai

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="NJ Tech Assistant",
    page_icon="📱",
    layout="centered"
)

# ---------- LOAD API KEY (Corrected Name) ----------
# இங்கே பெயரை 'GOOGLE_API_KEY' என மாற்றிவிட்டேன்
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ Google API Key missing. Please add it in Streamlit Secrets.")
    st.stop()

api_key = st.secrets["GOOGLE_API_KEY"]

# ---------- CONFIGURE (With Fix) ----------
# 'transport=rest' சேர்த்தால் தான் கனெக்ஷன் கட் ஆகாது
genai.configure(api_key=api_key, transport="rest")

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

# ---------- CHAT SESSION ----------
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# ---------- CHAT HISTORY ----------
for msg in st.session_state.chat.history:
    role = "assistant" if msg.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(msg.parts[0].text)

# ---------- USER INPUT ----------
if prompt := st.chat_input("Customer enna kettaanga...?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)

    except Exception as e:
        st.error(f"⚠️ Something went wrong: {e}")
