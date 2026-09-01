import streamlit as st
from groq import Groq
import json
import os
from datetime import datetime

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_memory(summary):
    memory = load_memory()
    memory.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "summary": summary
    })
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

st.title("brainpass")
st.caption("keeping memory alive")

conversation = st.text_area("paste your conversation here", height=300)

if st.button("summarize"):
    if conversation:
        with st.spinner("reading your memory..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a memory summarizer. Extract key information: who the user is, what they are building, what decisions were made, and where they left off. Format it as a clean context prompt."
                    },
                    {
                        "role": "user",
                        "content": f"Summarize this conversation:\n{conversation}"
                    }
                ]
            )
        result = response.choices[0].message.content
        save_memory(result)
        st.success("your context is ready ")
        st.text_area("copy this and carry it anywhere", result, height=300)
    else:
        st.warning("paste a conversation first!")

st.divider()
st.subheader("your memory vault")

memory = load_memory()
if memory:
    for i, entry in enumerate(reversed(memory)):
        with st.expander(f"{entry['time']}"):
            st.text_area("context", entry['summary'], height=150, key=f"memory_{i}")
else:
    st.caption("no memories saved yet. summarize something first!")