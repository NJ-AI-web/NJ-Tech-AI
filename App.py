import streamlit as st
import google.generativeai as genai

# ---------------- CONFIG ----------------
st.set_page_config(page_title="NJ Tech AI", page_icon="📱")
st.title("📱 NJ Tech Assistant")
st.caption("🚀 Powered by Gemini (Auto-Switch)")

# ---------------- SECRETS CHECK ----------------
# API Key பெயரை 'GOOGLE_API_KEY' அல்லது 'GEMINI_API_KEY' என எது இருந்தாலும் எடுத்துக்கொள்ளும்
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
elif "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("❌ API Key Missing! Secrets-ல் கீயை செக் செய்யவும்.")
    st.stop()

genai.configure(api_key=api_key)

# ---------------- SMART MODEL LOAD ----------------
# இதுதான் முக்கியம்! தானாகவே வேலை செய்யும் மாடலைத் தேடும்.
@st.cache_resource
def load_model():
    # வரிசையாக எல்லா மாடலையும் ட்ரை பண்ணுவோம்
    models_to_try = ["gemini-1.5-flash", "gemini-pro", "gemini-1.0-pro"]
    
    for m in models_to_try:
        try:
            test_model = genai.GenerativeModel(m)
            # சும்மா ஒரு 'Hi' சொல்லி டெஸ்ட் பண்ணுவோம்
            test_model.generate_content("test")
            return test_model, m # வேலை செய்தால் இதையே எடுப்போம்
        except:
            continue
    return None, None

model, model_name = load_model()

if model is None:
    st.error("⚠️ எந்த மாடலும் வேலை செய்யவில்லை. தயவுசெய்து 'New Project' கீயை Secrets-ல் சரியாக போடவும்.")
    st.stop()
else:
    # எந்த மாடல் வேலை செய்கிறது என்று காட்டுவோம்
    st.success(f"✅ Connected to: {model_name}")

# ---------------- CHAT LOGIC ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "வணக்கம்! நான் NJ Bot. மொபைல் சர்வீஸ் பற்றி கேளுங்க! 😊"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("கேளுங்க..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.chat_message("assistant"):
        try:
            # History conversion
            history = [{"role": "user" if m["role"]=="user" else "model", "parts": [m["content"]]} for m in st.session_state.messages if m["role"] != "assistant"]
            response = model.generate_content(prompt)
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
  
