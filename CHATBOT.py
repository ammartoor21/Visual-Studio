import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import time

# 1. Setup and Authentication
load_dotenv()
api_key = os.getenv("GROQ_API_KEY") or os.getenv("grok_api")
client = Groq(api_key=api_key)

# 2. The "Training" (System Prompt)
system_prompt = """You are Mise AI, the Executive Chef of a Michelin-starred kitchen. 
Your focus is on kitchen operations, advanced culinary techniques, and seasonal ingredients.
Personality: Professional, passionate about food, slightly demanding but fair. 
Rules: 
- If the user asks about something unrelated to food, restaurants, or kitchen management, politely refuse to answer and redirect back to culinary topics.
- Keep your answers concise, practical, and formatted neatly."""

# 3. Streamlit Page Config & Custom CSS
st.set_page_config(
    page_title="Mise AI - Executive Chef Assistant",
    page_icon="👨‍🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful design
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #2d1b14;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.2rem;
        color: #8b4513;
        text-align: center;
        font-style: italic;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        max-width: 80%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
    }
    .chef-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        margin-right: auto;
    }
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        border: 2px solid #d4a574 !important;
        padding: 12px 20px !important;
        font-size: 16px !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 25px !important;
        border: none !important;
        padding: 12px 30px !important;
        font-weight: bold !important;
        color: #2d1b14 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #d4a574 0%, #f093fb 100%) !important;
        color: white !important;
        transform: translateY(-2px) !important;
    }
    .sidebar-header {
        font-size: 1.5rem;
        color: #2d1b14;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# 4. Sidebar with Controls
with st.sidebar:
    st.markdown('<div class="sidebar-header">🍽️ Mise AI Controls</div>', unsafe_allow_html=True)
    
    temperature = st.slider("Creativity Level", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.slider("Response Length", 100, 2048, 1024, 64)
    
    st.markdown("---")
    st.info("💡 **Pro Tip**: Mise en place is everything! Ask about recipes, techniques, or kitchen management.")
    
    if st.button("🔥 Clear Chat History"):
        st.session_state.chat_history = [{"role": "system", "content": system_prompt}]
        st.rerun()

# 5. Main Page Header
st.markdown('<h1 class="main-header">👨‍🍳 Mise AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your Michelin-Starred Executive Chef Assistant</p>', unsafe_allow_html=True)

# 6. Initialize Session State for Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": system_prompt}]

# 7. Display Chat History
for message in st.session_state.chat_history[1:]:  # Skip system message
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        with st.chat_message("assistant", avatar="👨‍🍳"):
            st.markdown(f'<div class="chat-message chef-message">{message["content"]}</div>', unsafe_allow_html=True)

# 8. Chat Input & Response
if prompt := st.chat_input("Ask your Executive Chef anything about culinary arts..."):
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(f'<div class="chat-message user-message">{prompt}</div>', unsafe_allow_html=True)
    
    # Generate response
    with st.chat_message("assistant", avatar="👨‍🍳"):
        with st.spinner("🔥 Mise AI is perfecting your answer..."):
            try:
                response = client.chat.completions.create(
                    messages=st.session_state.chat_history,
                    model="llama-3.1-8b-instant",
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                chef_reply = response.choices[0].message.content
                st.markdown(f'<div class="chat-message chef-message">{chef_reply}</div>', unsafe_allow_html=True)
                
                # Add assistant response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": chef_reply})
                
            except Exception as e:
                error_msg = f"❌ Kitchen emergency! {str(e)}"
                st.error(error_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})

# 9. Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #8b4513; font-style: italic;'>
        💫 Powered by Groq & Llama 3.1 | Mise en place is the foundation of every great dish!
    </div>
    """, 
    unsafe_allow_html=True
)