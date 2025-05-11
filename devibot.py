import streamlit as st

# === Streamlit Page Config (Must be first) ===
st.set_page_config(page_title="DeviBot - Chatbot")
st.title("DeviBot")
st.markdown("Welcome to DeviBot, your AI assistant.")

# === Sidebar: API Key Input (Only shown if API key isn't entered) ===
if "api_key" not in st.session_state:
    st.session_state.api_key = None

if st.session_state.api_key is None:
    st.sidebar.header("API Configuration")
    st.sidebar.text_input("Enter your API key", type="password", key="api_key")
else:
    st.sidebar.empty()  # This removes the sidebar once the API key is entered

# === API Key Validation ===
if st.session_state.api_key is None:
    st.warning("Please enter your API key in the sidebar to start chatting.")
    st.stop()

# === Initialize Chat History ===
if "messages" not in st.session_state:
    st.session_state.messages = []

# === Display Chat History ===
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# === Handle New Input ===
user_input = st.chat_input("Say something to DeviBot...")

if user_input:
    # Show user input
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate a simple bot response (you can replace this with any AI logic)
    bot_reply = f"DeviBot says: You said: {user_input}"

    # Show bot response
    st.chat_message("assistant").markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
