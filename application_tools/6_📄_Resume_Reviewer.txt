import streamlit as st
import os
from Home import handle_uploaded_file, run_stream, client

st.title("📄 Resume Reviewer")

# Get the current page name
current_page = "Resume Reviewer"

# Initialize session state for this page if it doesn't exist
if 'resume_reviewer_state' not in st.session_state:
    st.session_state.resume_reviewer_state = {
        'uploaded_file': None,
        'review_result': None
    }

# Check if there's a chat history for this page
if current_page not in st.session_state.page_chat_logs or not st.session_state.page_chat_logs[current_page]:
    # No chat history, display upload and submit
    uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"])

    if uploaded_file:
        st.write("Resume uploaded successfully!")

        if st.button("Submit for Review"):
            with st.spinner("Analyzing the resume..."):
                file = handle_uploaded_file(uploaded_file)
                user_input = f"Tolong bantu saya review CV berikut dan berikan feedback yang komprehensif {uploaded_file.name}"
                
                # Get the assistant ID from environment variables
                selected_assistant_id = os.environ.get("OPENAI_ASSISTANTS_5")
                
                # Run the conversation
                run_stream(user_input, file, selected_assistant_id)

                # Store the result in session state
                last_message = client.beta.threads.messages.list(
                    thread_id=st.session_state.page_thread_ids[current_page],
                    limit=1
                ).data[0]
                if last_message.role == "assistant":
                    st.session_state.resume_reviewer_state['review_result'] = last_message.content[0].text.value
                
                # Rerun to display the result
                st.rerun()

else:
    # Chat history exists, display the result and option to submit new CV
    st.subheader("Previous Resume Review Result:")
    st.write(st.session_state.page_chat_logs[current_page][-1]['msg'])

    st.subheader("Submit a New Resume")
    new_uploaded_file = st.file_uploader("Upload a new resume", type=["pdf", "docx", "txt"])

    if new_uploaded_file:
        st.write("New resume uploaded successfully!")

        if st.button("Submit for Review"):
            with st.spinner("Analyzing the new resume..."):
                file = handle_uploaded_file(new_uploaded_file)
                user_input = f"Tolong bantu saya review CV berikut dan berikan feedback yang komprehensif {new_uploaded_file.name}"
                
                # Get the assistant ID from environment variables
                selected_assistant_id = os.environ.get("OPENAI_ASSISTANTS_5")
                
                # Run the conversation
                run_stream(user_input, file, selected_assistant_id)

                # Rerun to update the display
                st.rerun()