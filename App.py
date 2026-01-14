import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="NJ Tech AI", page_icon="🤖")
st.title("📱 NJ Tech Assistant")
st.caption("🚀 Powered by Gemini 1.5 Flash")

# 1. API Key Check
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("API Key காணவில்லை! Secrets-ல் செக் செய்யவும்.")
    st.stop()

# 2. Configure with REST (Fixes Connection Issues)
# இந்த 'transport=rest' நெட்வொர்க் பிரச்சனையை தடுக்கும்
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport="rest")

# 3. Model Setup (Using the Faster, Free Model)
# புது சாவிக்கு இந்த மாடல் கண்டிப்பாக வேலை செய்யும்
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
    # ரோபோவுக்கான அறிவுரை (Hidden Instruction)
    st.session_state.messages.append({"role": "user", "content": "You are NJ Bot for NJ Tech mobile shop. Speak in Tanglish. Be polite."})
    st.session_state.messages.append({"role": "assistant", "content": "வணக்கம்! நான் NJ Bot. மொபைல் சர்வீஸ் பற்றி கேளுங்க!"})

# 5. Display Messages (முதல் இரண்டு வரிகளை மறைத்து விடுவோம்)
for message in st.session_state.messages[2:]:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["content"])

# 6. User Input
if prompt := st.chat_input("சந்தேகத்தை இங்கே கேளுங்க..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        # வரலாற்றை ஜெமினிக்கு புரியும் படி மாற்றுதல்
        gemini_history = [{"role": "user" if m["role"]=="user" else "model", "parts": [m["content"]]} for m in st.session_state.messages]
        try:
            response = model.generate_content(gemini_history)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
  
