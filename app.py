import uuid
import streamlit as st
import requests

st.set_page_config(page_title="Habit Builder Bot", layout="centered")
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
        if msg["role"] == "assistant":
            answer_type = msg.get("answer_type", "direct")
            if answer_type == "rag":
                st.caption("**Source:** Verified Health KB")
                retrieved_context = msg.get("retrieved_context", [])
                if retrieved_context:
                    with st.expander("Retrieved Health Knowledge Base Passages"):
                        for ctx in retrieved_context:
                            st.markdown(ctx)
            else:
                st.caption("**Source:** Direct Answer")

if user_input := st.chat_input("Message your habit coach..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    format_api_call = {
        "thread_id": st.session_state.thread_id,
        "message": user_input
    }

    with st.chat_message("assistant"):
        answer_type = "direct"
        retrieved_context = []

        try:
            backend_response = requests.post(API_BASE_URL, json=format_api_call, timeout=30)
            backend_response.raise_for_status()
            
            payload = backend_response.json()
            coach_reply = payload.get("response", "")
            answer_type = payload.get("answer_type", "direct")
            retrieved_context = payload.get("retrieved_context", [])
            
        except requests.exceptions.RequestException as e:
            coach_reply = f"Couldn't reach the coach right now. Is the backend running? (Error: {e})"

        st.markdown(coach_reply)

        if answer_type == "rag":
            st.caption("**Source:** Verified Health KB")
            if retrieved_context:
                with st.expander("Retrieved Health Knowledge Base Passages"):
                    for ctx in retrieved_context:
                        st.markdown(ctx)
        else:
            st.caption("**Source:** Direct Answer")
    
    st.session_state.messages.append({
        "role": "assistant", 
        "content": coach_reply,
        "answer_type": answer_type,
        "retrieved_context": retrieved_context
    })
