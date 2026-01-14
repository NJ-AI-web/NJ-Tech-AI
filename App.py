import streamlit as st
import google.generativeai as genai

# 1. Setup Page
st.set_page_config(page_title="NJ Tech AI", page_icon="🤖")
st.title("📱 NJ Tech Assistant")

# 2. Check API Key
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("API Key Missing! Please add it in Secrets.")
    st.stop()

# 3. Configure Gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- IMPORTANT FIX: Using the most stable model 'gemini-pro' ---
model = genai.GenerativeModel('gemini-pro')

# 4. Initialize Chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add System Prompt via history trick (Best for Gemini Pro)
    st.session_state.messages.append({"role": "user", "content": "You are NJ Bot, a helpful assistant for NJ Tech mobile shop. Speak in Tanglish. Be polite."})
    st.session_state.messages.append({"role": "assistant", "content": "Sure! I am NJ Bot. How can I help?"})

# 5. Show Chat History (Hiding system prompt)
for message in st.session_state.messages[2:]:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["content"])

# 6. Handle User Input
if prompt := st.chat_input("Ask me anything..."):
    # Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate Reply
    with st.chat_message("assistant"):
        # Convert history for Gemini
        gemini_history = []
        for m in st.session_state.messages:
            role = "user" if m["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [m["content"]]})

        try:
            response = model.generate_content(gemini_history)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Error: Server Busy or Key Error. Try again later.")
  
