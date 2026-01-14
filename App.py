import streamlit as st
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="NJ Tech AI",
    page_icon="🤖",
    layout="centered"
)

# ---------------- HEADER ----------------
st.title("📱 NJ Tech Assistant")
st.caption("🚀 Powered by Gemini 1.5 Flash")

# ---------------- API KEY ----------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("❌ Gemini API Key missing. Please add it in Streamlit Secrets.")
    st.info("Go to Settings → Secrets and add: GEMINI_API_KEY = 'your-key-here'")
    st.stop()

# ---------------- GEMINI CONFIG ----------------
genai.configure(api_key=api_key)

# ✅ CORRECT MODEL - THIS IS THE FIX!
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "user",
            "content": (
                "You are NJ Bot, a friendly assistant for NJ Tech mobile shop. "
                "Respond in casual Tanglish (Tamil + English mix). "
                "Help customers with: mobile phones, repairs, service, warranty, accessories. "
                "Be warm, helpful, and use simple language. "
                "Use Tamil words naturally like: phone, repair, warranty, service."
            )
        },
        {
            "role": "assistant",
            "content": "Vanakkam! 🙏 Naan NJ Bot. NJ Tech shop-kaga ungalukku help panren. Mobile, repair, warranty - enna venum sollunga! 😊"
        }
    ]

# ---------------- DISPLAY CHAT HISTORY ----------------
for msg in st.session_state.messages[1:]:  # Skip system prompt
    with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# ---------------- USER INPUT ----------------
if prompt := st.chat_input("Type your message here... / இங்கே type பண்ணுங்க..."):
    
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    # Display user message
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Yosikuren... 🤔"):
            try:
                # Prepare conversation history for Gemini
                gemini_messages = []
                for m in st.session_state.messages:
                    role = "user" if m["role"] == "user" else "model"
                    gemini_messages.append({
                        "role": role,
                        "parts": [m["content"]]
                    })
                
                # Generate response
                response = model.generate_content(gemini_messages)
                reply = response.text
                
                # Display response
                st.markdown(reply)
                
                # Add to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })
                
            except Exception as e:
                error_msg = str(e)
                st.error(f"⚠️ Oops! Something went wrong:")
                st.code(error_msg)
                
                # Helpful error messages
                if "API_KEY" in error_msg.upper():
                    st.info("💡 Check your API key in Secrets")
                elif "QUOTA" in error_msg.upper():
                    st.info("💡 API quota exceeded. Try again later.")
                elif "404" in error_msg:
                    st.info("💡 Model not found. Using gemini-1.5-flash")
                else:
                    st.info("💡 Please try again or contact support")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    **NJ Tech Assistant** helps you with:
    - 📱 Mobile phones
    - 🔧 Repairs & Service
    - 📜 Warranty info
    - 🎧 Accessories
    
    ---
    Powered by Google Gemini 1.5 Flash
    """)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            st.session_state.messages[0],  # Keep system prompt
            {
                "role": "assistant",
                "content": "Vanakkam! 🙏 Naan NJ Bot. Enna help venum sollunga! 😊"
            }
        ]
        st.rerun()
    
    st.markdown("---")
    st.caption("Made with ❤️ for NJ Tech")
