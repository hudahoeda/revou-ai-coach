import os
import streamlit as st
from Home import login, load_chat_screen

# Main content
if not st.session_state['logged_in']:
    login()
else:
    # Check if multi-agent settings are defined
    single_agent_id = os.environ.get("OPENAI_ASSISTANTS_2", None)
    single_agent_title = os.environ.get("OPENAI_ASSISTANTS_TITLE_2", "Assistants API UI")
    if single_agent_id:
        load_chat_screen(single_agent_id, single_agent_title)
    else:
        st.error("No assistant configurations defined in environment variables.")