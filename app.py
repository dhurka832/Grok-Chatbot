import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

GROK_API_KEY = os.getenv("GROK_API_KEY")

client = OpenAI(
    api_key=GROK_API_KEY,
    base_url="https://api.poe.com/v1" 
)

st.set_page_config(page_title="Grok AI Chatbot", layout="centered")
st.title("🤖 AI Chatbot using Grok API")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask anything...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = client.chat.completions.create(
            model="grok-3-mini",  
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                *st.session_state.messages
            ]
        )

        answer = response.choices[0].message.content

    except Exception as e:
        answer = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
