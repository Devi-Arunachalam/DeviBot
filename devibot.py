import streamlit as st
import google.generativeai as genai

# === Streamlit Page Config ===
st.set_page_config(page_title="DeviBot - Chatbot")
st.title("DeviBot")
st.markdown("Welcome to DeviBot, your AI assistant!")

# === Sidebar: API Key Input ===
st.sidebar.header("API Configuration")
api_key = st.sidebar.text_input("Enter your Gemini API key", type="password", key="api_key")

# === API Key Validation ===
if not api_key:
    st.warning("Please enter your Gemini API key in the sidebar to start chatting.")
    st.stop()

# === Configure Gemini API Client ===
genai.configure(api_key=api_key)

# === Initialize Chat History ===
if "messages" not in st.session_state:
    st.session_state.messages = []  # Initialize message history if not already done

# === Display Chat History ===
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# === Handle New Input ===
user_input = st.chat_input("Say something to DeviBot...")

if user_input:
    # Show user input immediately
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Send user input to Gemini for evaluation
    try:
        response = genai.GenerativeModel("gemini-2.0-flash").generate_content(user_input)
        bot_reply = response.text

        # Show bot response
        st.chat_message("assistant").markdown(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        st.error(f"Error communicating with Gemini: {e}")
