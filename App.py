import streamlit as st
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="NJ Tech AI",
    page_icon="🤖",
    layout="centered"
)

st.title("📱 NJ Tech Assistant")
st.caption("🚀 Powered by Gemini")

# ---------------- API KEY ----------------
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ Gemini API Key missing. Please add it in Streamlit Secrets.")
    st.stop()

# ---------------- GEMINI CONFIG ----------------
genai.configure(api_key=api_key)

# ✅ STABLE MODEL (NO 404)
model = genai.GenerativeModel("gemini-pro")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "user",
            "content": (
                "You are NJ Bot for NJ Tech mobile shop. "
                "Speak in friendly Tanglish Tamil. "
                "Help customers with mobiles, service, warranty."
            )
        },
        {
            "role": "assistant",
            "content": "Vanakkam 🙏 Naan NJ Bot. Enna help venum sollunga!"
        }
    ]

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- USER INPUT ----------------
if prompt := st.chat_input("Customer enna kettaanga...?"):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            gemini_history = []
            for m in st.session_state.messages:
                role = "user" if m["role"] == "user" else "model"
                gemini_history.append(
                    {"role": role, "parts": [m["content"]]}
                )

            response = model.generate_content(gemini_history)
            reply = response.text

            st.markdown(reply)
            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )

        except Exception as e:
            st.error(f"⚠️ Gemini Error: {e}")
