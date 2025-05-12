import streamlit as st
import google.generativeai as genai

# === Page Setup ===
st.set_page_config(page_title="DeviBot - Chatbot", layout="centered")
st.title("DeviBot")
st.markdown("Chat with DeviBot powered by Gemini.")

# === Sidebar: API Key and Mode Selection ===
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter your Gemini API key", type="password", key="api_key")
view_history = st.sidebar.checkbox("Show history")

# === Require API key ===
if not api_key:
    st.warning("Please enter your Gemini API key in the sidebar.")
    st.stop()

# === Configure Gemini API ===
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# === Init session states ===
if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = {}

# === Show Chat History Tab ===
if view_history:
    st.subheader("Past Conversations")
    user_history = st.session_state.history.get(api_key, [])
    if not user_history:
        st.info("No past conversations found for this API key.")
    else:
        for idx, convo in enumerate(user_history[::-1], 1):
            with st.expander(f"Conversation #{len(user_history) - idx + 1}"):
                for msg in convo:
                    role = "User" if msg["role"] == "user" else "DeviBot"
                    st.markdown(f"**{role}**: {msg['content']}")
    st.stop()

# === Display Current Chat ===
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# === Chat Input ===
user_input = st.chat_input("Say something to DeviBot...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Build full chat history prompt
    chat_history = ""
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "DeviBot"
        chat_history += f"{role}: {msg['content']}\n"
    chat_history += "DeviBot:"

    # Get Gemini response
    try:
        response = model.generate_content(chat_history)
        reply = response.text

        st.chat_message("assistant").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        error_msg = f"Error: {e}"
        st.chat_message("assistant").markdown(error_msg)
        st.session_state.messages.append({"role": "assistant", "content": error_msg})

# === Save conversation to history ===
def save_conversation():
    if st.session_state.messages:
        if api_key not in st.session_state.history:
            st.session_state.history[api_key] = []
        st.session_state.history[api_key].append(st.session_state.messages.copy())
        st.session_state.messages = []

st.button("End Chat and Save", on_click=save_conversation)
