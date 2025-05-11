import streamlit as st
import google.generativeai as genai

# === Sidebar for API Key ===
st.sidebar.header("API Configuration")
api_key = st.sidebar.text_input("Enter your Gemini API key", type="password")

# === Gemini Configuration Function ===
def configure_gemini_chat(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
    return model.start_chat(history=[])

# === Page Setup ===
st.set_page_config(page_title="DeviBot - Gemini Chat", page_icon="🤖")
st.title("🤖 DeviBot")
st.markdown("Chat with **DeviBot**, your AI assistant powered by Gemini with memory.")

# === Validate API Key ===
if not api_key:
    st.warning("Please enter your Gemini API key in the sidebar to start chatting.")
    st.stop()

# === Initialize Chat ===
if "chat" not in st.session_state:
    try:
        st.session_state.chat = configure_gemini_chat(api_key)
        st.session_state.messages = []
    except Exception as e:
        st.error(f"Failed to configure Gemini: {e}")
        st.stop()

# === Show Chat History ===
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# === Handle User Input ===
user_input = st.chat_input("Say something to DeviBot...")

if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get DeviBot's response
    try:
        response = st.session_state.chat.send_message(user_input)
        reply = response.text.strip()
    except Exception as e:
        reply = f"❌ Error from Gemini: {e}"

    # Display assistant response
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
