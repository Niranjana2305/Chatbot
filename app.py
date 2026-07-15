import uuid
import streamlit as st
import requests

st.set_page_config(page_title = "Habit Builder Bot", layout = "centered")
st.title("Habit Builder Coach")
st.caption("Build and track meaningful habits for life. Your AI accountability partner.")

API_BASE_URL = "http://localhost:8000/chat"

if "thread_id" not in st.session_state:
    st.session_state.thread_id = f"chat-{uuid.uuid4().hex[:6]}"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Message your habit coach..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    format_api_call = {
        "thread_id": st.session_state.thread_id,
        "message": user_input
    }

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            backend_response = requests.post(API_BASE_URL, json=format_api_call, timeout = 30)
            backend_response.raise_for_status()
            coach_reply = backend_response.json()["response"]
        except requests.exceptions.RequestException as e:
            coach_reply = f"Couldn't reach the coach right now. Is the backend running? (Error: {e})"

        message_placeholder.markdown(coach_reply)
    
    st.session_state.messages.append({"role": "assistant", "content": coach_reply})

    

    