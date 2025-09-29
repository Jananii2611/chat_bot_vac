import streamlit as st
import requests

st.set_page_config(
    page_title="🤖 LangGraph + Gemini Chatbot",
    page_icon="💬"
)
st.markdown(
    """
    <style>
    body, .block-container {
        background: linear-gradient(135deg,#e6e9f8 0%,#f9fafb 100%) !important;
    }
   .user-bubble {
  background: #56f4c6; color: #034d41; border-radius: 20px 20px 4px 20px; 
  padding: 14px 22px; margin: 14px 0 10px auto;
  max-width: 60%;             /* Reduce max width from 72% to 60% or lower */
  width: fit-content;          /* Add this */
  min-width: 90px;             /* Optional: minimum bubble size */
  font-size: 1.08em; box-shadow: 0 2px 12px #b6efc3a8; text-align: right;
  word-break: break-word;
}

.bot-bubble {
  background: #e3eafb; color: #073c53; border-radius: 20px 20px 20px 4px; 
  padding: 14px 22px; margin: 12px auto 14px 0;
  max-width: 60%;             /* Reduce max width */
  width: fit-content;          /* Add this */
  min-width: 90px;             /* Optional */
  font-size: 1.08em; box-shadow: 0 2px 12px #8ec1f1a8; text-align: left;
  word-break: break-word;
}

    </style>
    """,
    unsafe_allow_html=True,
)
st.title("🤖 LangGraph Powered Chatbot")
st.caption("Built with LangGraph + Streamlit + FastAPI 🚀")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    bubble_class = "user-bubble" if msg["role"] == "user" else "bot-bubble"
    bubble_align = "justify-content: flex-end;" if msg["role"] == "user" else "justify-content: flex-start;"
    st.markdown(
        f'<div class="chat-row chat-container" style="{bubble_align}">' \
        f'<div class="{bubble_class}">{msg["content"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

with st.form(key="send_form", clear_on_submit=True):
    cols = st.columns([11, 1])
    user_input = cols[0].text_input(
        "Type your message...", key="input", placeholder="Type your message...", label_visibility="hidden"
    )
    submit = cols[1].form_submit_button("↑", use_container_width=True)

if submit and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    # Make request to FastAPI
    with st.spinner("Generating response..."):
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"messages": st.session_state.messages}
        )
        if response.ok:
            bot_reply = response.json()["reply"]
        else:
            bot_reply = "❗ Error communicating with backend"
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.rerun()
