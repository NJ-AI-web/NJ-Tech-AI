import streamlit as st
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="NJ Tech AI", page_icon="📱", layout="centered")

# ---------------- HEADER ----------------
st.title("📱 NJ Tech Assistant")
st.caption("🚀 Powered by Gemini (Auto-Switch Mode)")

# ---------------- API KEY CHECK ----------------
# பெயரில் குழப்பம் வேண்டாம், இரண்டையும் தேடுவோம்
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
elif "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("❌ API Key Missing! Please add GOOGLE_API_KEY in Secrets.")
    st.stop()

# ---------------- CONFIGURE ----------------
# 'transport=rest' முக்கியம் (Server Busy வராமல் இருக்க)
genai.configure(api_key=api_key, transport="rest")

# ---------------- SMART MODEL SELECTOR (The Fix) ----------------
# இதுதான் முக்கியம்! தானாகவே வேலை செய்யும் மாடலைத் தேடும்.
def get_working_model():
    model_list = ["gemini-1.5-flash", "gemini-pro", "gemini-1.0-pro"]
    for model_name in model_list:
        try:
            model = genai.GenerativeModel(model_name)
            # சும்மா ஒரு டெஸ்ட் மெசேஜ் அனுப்பி பார்ப்போம்
            model.generate_content("Hi")
            return model # வேலை செய்தால் இதையே எடுப்போம்
        except:
            continue # வேலை செய்யலனா அடுத்த மாடல்
    return None

# மாடலைத் தேர்ந்தெடுப்போம்
if "model" not in st.session_state:
    with st.spinner("Connecting to Google..."):
        st.session_state.model = get_working_model()

if st.session_state.model is None:
    st.error("⚠️ எந்த மாடலும் வேலை செய்யவில்லை. தயவுசெய்து 'New Project' கீ எடுக்கவும்.")
    st.stop()

# ---------------- CHAT HISTORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": "You are NJ Bot for NJ Tech. Speak in Tanglish."},
        {"role": "assistant", "content": "Vanakkam! 🙏 Naan NJ Bot. Enna help venum?"}
    ]

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- USER INPUT ----------------
if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # History conversion
            gemini_history = []
            for m in st.session_state.messages:
                role = "user" if m["role"] == "user" else "model"
                gemini_history.append({"role": role, "parts": [m["content"]]})
            
            response = st.session_state.model.generate_content(gemini_history)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
