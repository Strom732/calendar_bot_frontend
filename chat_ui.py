import streamlit as st
import requests

# Backend URL
API_URL = "https://calendar-bot-backend.onrender.com"

# Streamlit UI
st.set_page_config(page_title="Calendar Bot 🤖", layout="centered")
st.title("📅 Calendar Bot")
st.caption("Ask me to book a meeting! (e.g. *Book a meeting with Abhi on 2025-07-03 at 1:00pm for 30 minutes*)")

# Session state to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.chat_input("Enter your request...")
if user_input:
    # Display user message
    st.session_state.chat_history.append(("user", user_input))

    # Send request to FastAPI
    try:
        with st.spinner("Booking..."):
            res = requests.post(API_URL, json={"user_input": user_input})
            res_json = res.json()

            # Extract response
            bot_reply = res_json.get("response", "Something went wrong.")
            st.session_state.chat_history.append(("bot", bot_reply))

    except Exception as e:
        st.session_state.chat_history.append(("bot", f"❌ Error: {str(e)}"))

# Display chat history
for role, msg in st.session_state.chat_history:
    if role == "user":
        with st.chat_message("user"):
            st.markdown(msg)
    else:
        with st.chat_message("assistant"):
            st.markdown(msg)
