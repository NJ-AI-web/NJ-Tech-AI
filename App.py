import streamlit as st
from google.generativeai import client

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="NJ Tech AI",
    page_icon="🤖",
    layout="centered"
)

st.title("📱 NJ Tech Assistant")
st.caption("🚀 Powered by Gemini 1.5 Flash")

# -------------------------------
# API KEY CHECK
# -------------------------------
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ GOOGLE_API_KEY missing in Streamlit secrets")
    st.stop()

# -------------------------------
# GEMINI CLIENT (NEW v1 API)
# -------------------------------
genai_client = client.Client(
    api_key=st.secrets["GOOGLE_API_KEY"]
)

# -------------------------------
# SESSION STATE INIT
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "user",
            "content": (
                "You are NJ Bot for NJ Tech mobile shop. "
                "Speak in friendly Tanglish Tamil. "
                "Help customers with mobile sales, service, accessories, "
                "warranty, and troubleshooting. Be polite and simple."
            )
        },
        {
            "role": "assistant",
            "content": (
                "வணக்கம் 🙏 நான் NJ Bot. "
                "மொபைல், சர்வீஸ், ஆக்சஸரீஸ் எதுவானாலும் கேளுங்க 😊"
            )
        }
    ]

# -------------------------------
# DISPLAY CHAT (SKIP SYSTEM PROMPT)
# -------------------------------
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# USER INPUT
# -------------------------------
user_prompt = st.chat_input("கேளுங்க...")

if user_prompt:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )

    # -------------------------------
    # PREPARE GEMINI FORMAT
    # -------------------------------
    gemini_history = []
    for m in st.session_state.messages:
        gemini_history.append({
            "role": "user" if m["role"] == "user" else "model",
            "parts": [m["content"]]
        })

    # -------------------------------
    # GEMINI CALL (v1 – CORRECT WAY)
    # -------------------------------
    try:
        response = genai_client.models.generate_content(
            model="gemini-1.5-flash",
            contents=gemini_history
        )

        reply = response.text

        with st.chat_message("assistant"):
            st.markdown(reply)

        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )

    except Exception as e:
        with st.chat_message("assistant"):
            st.error(f"❌ Error: {e}")
