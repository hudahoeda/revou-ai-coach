import os
import streamlit as st
from Home import load_chat_screen, login

assistant_message = "Apa ini?: Asisten ini siap bantu kamu menyusun dan memperbaiki bagian 'About Me' biar sesuai standar RevoU dan menarik perhatian. Cara Pakainya: Jawab beberapa pertanyaan, dan asisten ini bakal bantu kamu bikin 'About Me' yang kuat dan sesuai standar."

# Main content
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    login()
else:
    current_page = st.session_state.get('current_page', 'Unknown Page')
    single_agent_id = os.environ.get("OPENAI_ASSISTANTS_5", None)
    single_agent_title = os.environ.get("OPENAI_ASSISTANTS_TITLE_5", "Assistants API UI")
    if single_agent_id:
        load_chat_screen(single_agent_id, single_agent_title, assistant_message)
    else:
        st.error(f"No assistant configuration defined for {current_page}")

    # Use the current page name to manage page-specific chat logs
    if 'page_chat_logs' not in st.session_state:
        st.session_state.page_chat_logs = {}
    if current_page not in st.session_state.page_chat_logs:
        st.session_state.page_chat_logs[current_page] = []