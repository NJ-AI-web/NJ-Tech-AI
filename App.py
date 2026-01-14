import streamlit as st
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="NJ Tech AI",
    page_icon="📱",
    layout="centered"
)

# ---------------- HEADER ----------------
st.title("📱 NJ Tech Assistant")
st.caption("🚀 Powered by Gemini 1.5 Flash")

# ---------------- API KEY ----------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("❌ API Key missing! Add GEMINI_API_KEY in Secrets")
    st.stop()

# ---------------- CONFIGURE GEMINI ----------------
genai.configure(api_key=api_key)

# ---------------- MODEL SETUP ----------------
# Simple & direct - no testing
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "user",
            "content": "You are NJ Bot for NJ Tech mobile shop in Tamil Nadu. Speak in friendly Tanglish (Tamil + English mix). Help customers with mobiles, repairs, service, warranty, and accessories. Be warm and helpful."
        },
        {
            "role": "assistant", 
            "content": "Vanakkam! 🙏 Naan NJ Bot. NJ Tech mobile shop-kaga ungalukku help panren. Mobile, repair, warranty - enna venum sollunga! 😊"
        }
    ]

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages[1:]:  # Skip system message
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- USER INPUT ----------------
if prompt := st.chat_input("உங்க message இங்கே type பண்ணுங்க..."):
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("யோசிக்கிறேன்... 🤔"):
            try:
                # Build conversation history
                history = []
                for m in st.session_state.messages:
                    role = "user" if m["role"] == "user" else "model"
                    history.append({
                        "role": role,
                        "parts": [m["content"]]
                    })
                
                # Get response from Gemini
                response = model.generate_content(history)
                reply = response.text
                
                # Display and save
                st.markdown(reply)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })
                
            except Exception as e:
                error_text = str(e)
                st.error(f"❌ Error: {error_text}")
                
                # Specific error messages
                if "404" in error_text:
                    st.warning("⚠️ Model not found!")
                    st.info("""
                    **Solution:**
                    1. Go to Google AI Studio
                    2. Create NEW API key in NEW project
                    3. Update Streamlit Secrets
                    4. Make sure library version is 0.8.3+
                    """)
                elif "API_KEY" in error_text.upper():
                    st.warning("⚠️ API Key issue!")
                    st.info("Check if your API key is correct in Secrets")
                elif "quota" in error_text.lower():
                    st.warning("⚠️ API quota exceeded!")
                    st.info("Wait a few minutes and try again")
                else:
                    st.info("Try refreshing the page")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### 📱 NJ Tech Bot")
    st.markdown("""
    **வணக்கம்!**
    
    I can help you with:
    - 📱 Mobile phones
    - 🔧 Repairs & Service
    - 📜 Warranty info
    - 🎧 Accessories
    
    ---
    Powered by Google Gemini 1.5 Flash
    """)
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = st.session_state.messages[:2]
        st.rerun()
    
    st.markdown("---")
    st.caption("Made with ❤️ for NJ Tech")
