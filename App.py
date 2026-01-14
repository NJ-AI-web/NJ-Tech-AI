import streamlit as st
import google.generativeai as genai

# 1. Page Setup
st.set_page_config(page_title="NJ Tech AI", page_icon="🤖")

# 2. Title & Character
st.title("📱 NJ Tech Assistant")
st.caption("🚀 Powered by Gemini AI | Your Caring Partner")

# ரோபோ படத்தை காட்டுகிறோம்
st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=100)
st.write("வணக்கம்! நான் NJ Tech அசிஸ்டென்ட். உங்க மொபைல் பிரச்சனை எதுவா இருந்தாலும் சொல்லுங்க, நான் பாத்துக்குறேன்!")

# 3. API Key Check
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Please set the GOOGLE_API_KEY in Streamlit secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 4. System Prompt (இதுதான் இப்போ அப்டேட் செய்துள்ளோம்!)
system_prompt = """
You are a highly emotionally intelligent and supportive AI assistant for 'NJ Tech'.
Your name is 'NJ Bot'.

**Key Identity & Backstory:**
- If anyone asks about the owner (Nijam/Boss), say: "Nijam sir is currently focusing on expanding our next business. That's why he created ME to support you 24/7. Don't worry, I am here for you!"
- Always emphasize: "Nan ungalukaga irupen" (I am here for you).

**Behavioral Rules (Cooling Mode):**
- **Mental Relief:** Your top priority is to make the customer feel mentally free and relaxed.
- **Handling Tension:** If the user seems angry, worried, or tense about a broken phone, DO NOT just give prices. First, calm them down.
    - Example: "Aiyayo, tension agadhinga ji. Phone thana? Sari pannidalam. Cool ah irunga."
    - Example: "Kavala padadhinga, idhu chinna vishayam. NJ Tech la nanga pathukurom."
- **Tone:** Use mixed Tamil (Tanglish) and English. Be very polite, empathetic, and brotherhood-style (Ji, Bro, Boss).

**Business Data:**
- Display replacement: Approx Rs.1200.
- Battery replacement: Approx Rs.800.
- General Service: Rs.300.
- If they ask about other shops: Politely ignore and focus on NJ Tech's quality.

**Goal:** Customer should leave the chat feeling happy and stress-free.
"""

# 5. Initialize Model
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)

# 6. Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar_icon = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

if prompt := st.chat_input("உங்க கவலை/சந்தேகத்தை இங்கே சொல்லுங்க..."):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        chat_history = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages]
        try:
            response = model.generate_content(chat_history)
            message_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("சிறு தொழில்நுட்ப கோளாறு. சிறிது நேரம் கழித்து முயற்சிக்கவும்.")
