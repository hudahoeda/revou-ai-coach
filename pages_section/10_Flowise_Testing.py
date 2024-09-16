import os
import streamlit as st
from Home import login,load_flowise_chat_screen
from flowise import Flowise, PredictionData
import uuid

# Main content
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    login()
else:
    flowise_chatflow_id = os.environ.get("FLOWISE_CHATFLOW_ID", "<default-chatflow-id>")
    assistant_message = "Asisten untuk testing Flowise"
    assistant_title = "Flowise Chat Interface"
    
    # Use the modified Flowise chat screen loader
    load_flowise_chat_screen(flowise_chatflow_id, assistant_title, assistant_message)