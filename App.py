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

# 4. Initialize Model
model = genai.GenerativeModel('gemini-pro')

# 5. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
    # System prompt as first exchange
    st.session_state.messages.append({
        "role": "user", 
        "content": "You are NJ Bot, a helpful assistant for NJ Tech mobile shop. Speak in Tanglish (Tamil + English mix). Be polite and friendly."
    })
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Sure da! I am NJ Bot from NJ Tech. Mobile, accessories ellam irukku. What do you need?"
    })

# 6. Initialize Chat Session
if "chat" not in st.session_state:
    # Convert messages to Gemini format for chat history
    history = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        history.append({"role": role, "parts": [msg["content"]]})
    
    st.session_state.chat = model.start_chat(history=history)

# 7. Display Chat History (skip system prompt)
for message in st.session_state.messages[2:]:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["content"])

# 8. Handle User Input
if prompt := st.chat_input("Ask me anything..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add to messages
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response
    with st.chat_message("assistant"):
        try:
            # Use the chat session to send message
            response = st.session_state.chat.send_message(prompt)
            reply = response.text
            
            # Display and save response
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Try refreshing the page or check your API key.")

# 9. Sidebar (Optional)
with st.sidebar:
    st.header("🛠️ NJ Tech")
    st.info("Latest mobiles, accessories, repairs!")
    
    if st.button("🔄 Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat = None
        st.rerun()
