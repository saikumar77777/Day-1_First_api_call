import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set page config
st.set_page_config(
    page_title="OpenAI Chat Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    st.markdown("---")
    
    # System prompt configuration
    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful, friendly, and knowledgeable AI assistant. Provide clear and concise responses.",
        height=100
    )
    
    # Model selection
    model = st.selectbox(
        "Select Model",
        ["gpt-3.5-turbo", "gpt-4"],
        index=0
    )
    
    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher values make the output more random, lower values make it more deterministic."
    )
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main content
st.title("🤖 OpenAI Chat Assistant")
st.markdown("---")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Prepare messages for API call
    messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages
    
    try:
        # Show a spinner while generating response
        with st.spinner("Thinking..."):
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
            
            # Extract assistant reply
            assistant_reply = response["choices"][0]["message"]["content"]
            
            # Add assistant message to chat history
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            
            # Display assistant reply
            with st.chat_message("assistant"):
                st.write(assistant_reply)
            
            # Display token usage in expander
            with st.expander("Token Usage Details"):
                usage = response["usage"]
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Prompt Tokens", usage["prompt_tokens"])
                with col2:
                    st.metric("Completion Tokens", usage["completion_tokens"])
                with col3:
                    st.metric("Total Tokens", usage["total_tokens"])
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your API key and internet connection.")
