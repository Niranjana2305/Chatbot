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

    backend_response = requests.post(API_BASE_URL, json=format_api_call)

    reply_data = backend_response.json()
    coach_reply = reply_data["response"]

    with st.chat_message("assistant"):
        st.markdown(coach_reply)

    st.session_state.messages.append({"role": "assistant", "content": coach_reply})

    

    