import streamlit as st
import os
from Home import login, load_chat_screen, handle_uploaded_file, run_stream

# Main content
selected_assistant_id = os.environ.get("OPENAI_ASSISTANTS_5")
if not st.session_state['logged_in']:
    login()
else:
    st.title("📝 Resume Reviewer")
    uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"])

    if uploaded_file:
        st.write("Resume uploaded successfully!")

        if st.button("Submit for Review"):
            with st.spinner("Analyzing the resume..."):
                file = handle_uploaded_file(uploaded_file)
                user_input = f"Tolong bantu saya review CV berikut dan berikan feedback yang komprehensif {uploaded_file.name}"
                run_stream(user_input,file,selected_assistant_id)

    if "chat_log" not in st.session_state:
        st.session_state.chat_log = []