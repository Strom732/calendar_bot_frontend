import streamlit as st
import requests
import uuid

# ✅ Set this to your hosted backend URL
API_URL = "https://calendar-bot-backend.onrender.com"

# Generate or reuse a unique session_id for conversation state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Streamlit UI
st.set_page_config(page_title="Calendar Bot 🤖", layout="centered")
st.title("📅 Calendar Bot")
st.caption("I'll help you schedule meetings on your calendar step by step!")

# Session state to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.chat_input("Say hi or ask to book a meeting...")
if user_input:
    # Display user message
    st.session_state.chat_history.append(("user", user_input))

    # Send request to FastAPI backend with session_id
    try:
        with st.spinner("Thinking..."):
            res = requests.post(
                f"{API_URL}/chat",
                json={
                    "user_input": user_input,
                    "session_id": st.session_state.session_id
                },
                timeout=15
            )
            res_json = res.json()

            # Extract response
            bot_reply = res_json.get("response", "⚠️ Something went wrong.")
            st.session_state.chat_history.append(("bot", bot_reply))

    except Exception as e:
        st.session_state.chat_history.append(("bot", f"❌ Error: {str(e)}"))

# Display chat history
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)
