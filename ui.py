import streamlit as st
import requests

st.header("Codebase & Document Whisperer 🤖")

user_input = st.chat_input("Ask a question about your codebase")

if user_input:
    st.chat_message("user").write(user_input)
    try:
        response = requests.post("http://localhost:8000/chat", json={"question": user_input})
        data = response.json()
        if "answer" in data:
            st.chat_message("ai").write(data["answer"])
        else:
            st.chat_message("ai").write(f"API Error: {data.get('error')}")
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")


