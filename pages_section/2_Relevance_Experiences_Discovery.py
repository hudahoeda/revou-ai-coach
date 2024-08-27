import os
import streamlit as st
from Home import load_chat_screen, login

assistant_message = "Apa ini?: Asisten ini bakal bantu kamu mengidentifikasi dan mencatat semua pengalaman relevan yang kamu punya. Ini bakal ngebantu kamu paham skill apa yang bisa kamu angkat lebih tinggi. \n Cara Pakainya: Cukup jawab beberapa pertanyaan tentang pengalaman kamu, dan asisten ini bakal kasih insight tentang skill yang bisa kamu tonjolkan."

# Main content
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    login()
else:
    current_page = st.session_state.get('current_page', 'Unknown Page')
    single_agent_id = os.environ.get("OPENAI_ASSISTANTS_2", None)
    single_agent_title = os.environ.get("OPENAI_ASSISTANTS_TITLE_2", "Assistants API UI")
    if single_agent_id:
        load_chat_screen(single_agent_id, single_agent_title,assistant_message)
    else:
        st.error(f"No assistant configuration defined for {current_page}")

    # Use the current page name to manage page-specific chat logs
    if 'page_chat_logs' not in st.session_state:
        st.session_state.page_chat_logs = {}
    if current_page not in st.session_state.page_chat_logs:
        st.session_state.page_chat_logs[current_page] = []