import os
import streamlit as st
from Home import load_chat_screen, login

assistant_message = "Apa ini?: Asisten ini bakal bantu kamu mendalami detail dari pengalaman yang kamu punya, biar bisa kamu pakai sebagai aset personal branding dan info penting buat interview. Cara Pakainya: Ceritakan pengalamanmu, dan asisten ini bakal bantu kamu menggali detail penting yang bisa jadi nilai tambah."


# Main content
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    login()
else:
    current_page = st.session_state.get('current_page', 'Unknown Page')
    single_agent_id = os.environ.get("OPENAI_ASSISTANTS_3", None)
    single_agent_title = os.environ.get("OPENAI_ASSISTANTS_TITLE_3", "Assistants API UI")
    if single_agent_id:
        load_chat_screen(single_agent_id, single_agent_title, assistant_message)
    else:
        st.error(f"No assistant configuration defined for {current_page}")

    # Use the current page name to manage page-specific chat logs
    if 'page_chat_logs' not in st.session_state:
        st.session_state.page_chat_logs = {}
    if current_page not in st.session_state.page_chat_logs:
        st.session_state.page_chat_logs[current_page] = []