import streamlit as st
from openai import OpenAI
import time
import os
import base64
import re
import json

import streamlit as st
import openai
from openai import AssistantEventHandler
from tools import TOOL_MAP
from typing_extensions import override
from dotenv import load_dotenv
import streamlit_authenticator as stauth
from pyairtable import Api
import time
import uuid

# Add these to your existing environment variable loading
BASE_ID = os.environ.get('BASE_ID')
USER_TABLE_NAME = 'Users'
CHAT_TABLE_NAME = 'Chat History'
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')

selected_assistant_id = os.environ.get("OPENAI_ASSISTANTS_1")

# Initialize Airtable API
try:
    airtable = Api(AIRTABLE_API_KEY)
except Exception as e:
    st.error(f"Error initializing Airtable API: {str(e)}")
    st.stop()

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
instructions = os.environ.get("RUN_INSTRUCTIONS", "")
enabled_file_upload_message = os.environ.get(
    "ENABLED_FILE_UPLOAD_MESSAGE", "Upload a file"
)

client = openai.OpenAI(api_key=openai_api_key)

class EventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()
        self.run_id = None
        self.full_response = ""

    @override
    def on_event(self, event):
        if hasattr(event, 'run_id') and event.run_id:
            self.run_id = event.run_id

    @override
    def on_text_created(self, text):
        self.full_response = ""
        with st.chat_message("Assistant"):
            st.session_state.current_markdown = st.empty()

    @override
    def on_text_delta(self, delta, snapshot):
        if snapshot.value:
            self.full_response = snapshot.value
            text_value = re.sub(
                r"\[(.*?)\]\s*\(\s*(.*?)\s*\)", "Download Link", self.full_response
            )
            st.session_state.current_markdown.markdown(text_value, True)

    @override
    def on_text_done(self, text):
        format_text = format_annotation(text)
        st.session_state.current_markdown.markdown(format_text, True)
        st.session_state.chat_log.append({"name": "assistant", "msg": format_text})
        last_message = client.beta.threads.messages.list(
            thread_id=st.session_state.thread.id, limit=1
        ).data[0]
        if last_message.role == "assistant" and last_message.run_id:
            self.run_id = last_message.run_id

def format_annotation(text):
    citations = []
    text_value = text.value
    for index, annotation in enumerate(text.annotations):
        text_value = text.value.replace(annotation.text, f" [{index}]")

        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(
                f"[{index}] {file_citation.quote} from {cited_file.filename}"
            )
        elif file_path := getattr(annotation, "file_path", None):
            link_tag = create_file_link(
                annotation.text.split("/")[-1],
                file_path.file_id,
            )
            text_value = re.sub(r"\[(.*?)\]\s*\(\s*(.*?)\s*\)", link_tag, text_value)
    text_value += "\n\n" + "\n".join(citations)
    return text_value

def create_file_link(file_name, file_id):
    content = client.files.content(file_id)
    content_type = content.response.headers["content-type"]
    b64 = base64.b64encode(content.text.encode(content.encoding)).decode()
    link_tag = f'<a href="data:{content_type};base64,{b64}" download="{file_name}">Download Link</a>'
    return link_tag

def handle_uploaded_file(uploaded_file):
    file = client.files.create(file=uploaded_file, purpose="assistants")
    return file

def create_thread():
    return client.beta.threads.create()

def create_message(thread, content, file):
    attachments = []
    if file is not None:
        attachments.append(
            {"file_id": file.id, "tools": [{"type": "code_interpreter"}, {"type": "file_search"}]}
        )
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=content, attachments=attachments
    )

def save_chat_history(session_id, username, student_id, user_input, response, assistant_id, model, prompt_tokens, completion_tokens, total_tokens):
    try:
        table = airtable.table(BASE_ID, CHAT_TABLE_NAME)
        table.create({
            "SessionID": session_id,
            "Timestamp": int(time.time()),
            "StudentID": student_id,
            "Username": username,
            "UserInput": user_input,
            "Response": response,
            "AssistantID" : assistant_id,
            "Model": model,
            "PromptTokens": prompt_tokens,
            "CompletionTokens": completion_tokens,
            "TotalTokens": total_tokens
        })
    except Exception as e:
        st.error(f"Error saving chat history: {str(e)}")

def generate_session_id():
    return str(uuid.uuid4())

def run_stream(file):
    if "thread" not in st.session_state:
        st.session_state.thread = create_thread()

    create_message(st.session_state.thread, "Tolong bantu saya review CV berikut dan berikan feedback yang komprehensif.", file)

    event_handler = EventHandler()

    with client.beta.threads.runs.stream(
        thread_id=st.session_state.thread.id,
        assistant_id=selected_assistant_id,
        event_handler=event_handler,
    ) as stream:
        stream.until_done()

    # Check if the run_id was captured
    run_id = event_handler.run_id
    if not run_id:
        raise RuntimeError("Failed to retrieve run ID")

    # Fetch the run details using the run_id
    run_details = client.beta.threads.runs.retrieve(thread_id=st.session_state.thread.id, run_id=run_id)

    # Extract the required details from the run object
    assistant_id = run_details.assistant_id
    model = run_details.model
    prompt_tokens = run_details.usage.prompt_tokens
    completion_tokens = run_details.usage.completion_tokens
    total_tokens = run_details.usage.total_tokens

    # Save chat history after the stream is complete
    last_assistant_message = client.beta.threads.messages.list(thread_id=st.session_state.thread.id).data[0]

    # Remove the existing chat message if it's the same as the last one (to avoid duplicates)
    if st.session_state.chat_log and st.session_state.chat_log[-1]["msg"] == last_assistant_message.content[0].text.value:
        st.session_state.chat_log.pop()

    # Append the new chat message to the chat log
    st.session_state.chat_log.append({
        "name": "assistant",
        "msg": last_assistant_message.content[0].text.value
    })

    save_chat_history(
        session_id = st.session_state['session_id'],
        username = st.session_state['username'],
        student_id = get_student_id(st.session_state['username']),
        user_input= file.filename,
        response = last_assistant_message.content[0].text.value,
        assistant_id = assistant_id,
        model = model,
        prompt_tokens = prompt_tokens,
        completion_tokens = completion_tokens,
        total_tokens = total_tokens
    )


def reset_chat():
    st.session_state.chat_log = []
    st.session_state.in_progress = False

def get_user(username):
    try:
        table = airtable.table(BASE_ID, USER_TABLE_NAME)
        records = table.all(formula=f"{{Username}} = '{username}'")
        return records[0] if records else None
    except Exception as e:
        st.error(f"Error getting user: {str(e)}")
        return None

def get_student_id(username):
    try:
        table = airtable.table(BASE_ID, USER_TABLE_NAME)
        records = table.all(formula=f"{{Username}} = '{username}'")
        if records:
            return records[0]['fields'].get('StudentID')
        else:
            return None
    except Exception as e:
        st.error(f"Error getting user: {str(e)}")
        return None

def verify_password(stored_password, provided_password):
    return stored_password == provided_password

def login():
    st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    st.title("💬 RevoU AI Coach")
    st.text("Enter your credential")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = get_user(username)
        if user:
            if 'Password' in user['fields']:
                if verify_password(user['fields']['Password'], password):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid password")
            else:
                st.error("User record does not contain a password field")
        else:
            st.error("User not found")

def main():
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = generate_session_id()

    # Sidebar for logout
    if st.session_state['logged_in']:
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state.pop('username', None)
            st.session_state['chat_history'] = []
            st.success("Logged out successfully!")
            reset_chat()
            st.rerun()
    
    # Main content
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
                    run_stream(file)

        if "chat_log" not in st.session_state:
            st.session_state.chat_log = []

        # Render only the last chat message
        if st.session_state.chat_log:
            last_chat = st.session_state.chat_log[-1]
            with st.chat_message(last_chat["name"]):
                st.markdown(last_chat["msg"], True)

if __name__ == "__main__":
    main()