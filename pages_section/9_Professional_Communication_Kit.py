import os
import streamlit as st
from Home import load_chat_screen, login

assistant_message = "Asisten ini bantu kamu menyusun cover letter dan pesan lainnya dengan nada profesional, supaya komunikasi kamu terlihat berkualitas tinggi. Tulis pesan atau cover letter yang ingin kamu kirim, dan asisten ini bakal bantu kamu menyusunnya dengan nada profesional yang tepat."

# Main content
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    login()
else:
    current_page = st.session_state.get('current_page', 'Unknown Page')
    single_agent_id = os.environ.get("OPENAI_ASSISTANTS_9", None)
    single_agent_title = os.environ.get("OPENAI_ASSISTANTS_TITLE_9", "Assistants API UI")
    if single_agent_id:
        load_chat_screen(single_agent_id, single_agent_title, assistant_message)
    else:
        st.error(f"No assistant configuration defined for {current_page}")

    # Use the current page name to manage page-specific chat logs
    if 'page_chat_logs' not in st.session_state:
        st.session_state.page_chat_logs = {}
    if current_page not in st.session_state.page_chat_logs:
        st.session_state.page_chat_logs[current_page] = []