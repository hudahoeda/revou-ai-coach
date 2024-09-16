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
from flowise import Flowise, PredictionData
import requests
# Add these to your existing environment variable loading
BASE_ID = os.environ.get('BASE_ID')
USER_TABLE_NAME = 'Users'
CHAT_TABLE_NAME = 'Chat History'
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')

# Initialize Airtable API
try:
    airtable = Api(AIRTABLE_API_KEY)
except Exception as e:
    st.error(f"Error initializing Airtable API: {str(e)}")
    st.stop()

load_dotenv()


def str_to_bool(str_input):
    if not isinstance(str_input, str):
        return False
    return str_input.lower() == "true"

# Load environment variables
openai_api_key = os.environ.get("OPENAI_API_KEY")
instructions = os.environ.get("RUN_INSTRUCTIONS", "")
enabled_file_upload_message = os.environ.get(
    "ENABLED_FILE_UPLOAD_MESSAGE", "Upload a file"
)
azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
azure_openai_key = os.environ.get("AZURE_OPENAI_KEY")
authentication_required = str_to_bool(os.environ.get("AUTHENTICATION_REQUIRED", False))

# Define your pages using st.Page with actual icons
message = st.Page("message.py", 
                  title="Message", 
                  icon="💬")

flowise = st.Page("pages_section/10_Flowise_Testing.py", 
                        title="Flowise Testing", 
                        icon="📝")

professional_value_dicoveries = st.Page("pages_section/1_Professional_Value_Discoveries.py", 
                        title="Professional Value Discoveries", 
                        icon="📝")

relevance_experiences_discovery = st.Page("pages_section/2_Relevance_Experiences_Discovery.py", 
                                   title="Relevance Experiences Discovery", 
                                   icon="💼")

experience_detail_discovery = st.Page("pages_section/3_Experience_Detail_Discovery.py", 
                                  title="Experience Detail Discovery", 
                                  icon="📱")

about_me_summary_crafting = st.Page("pages_section/5_About_Me_Summary_Crafting.py", 
                                   title="About Me Preparation", 
                                   icon="📋")

professionals_and_organizational_experience_crafting = st.Page("pages_section/4_Professionals_and_Organizational_Experience_Crafting.py", 
                                                        title="Professionals and Organizational Experience Crafting", 
                                                        icon="📋")

project_crafting = st.Page("pages_section/6_Project_Crafting.py",
                           title="Project Crafting",
                           icon="🔧")

CV_reviewer = st.Page("pages_section/7_CV_Reviewer.py",
                        title="CV Reviewer",
                        icon="📄")

assets_personalization_kit = st.Page("pages_section/8_Assets_Personalization_Kit.py",
                                     title="Assets Personalization Kit",
                                     icon="📋")

professional_communication_kit = st.Page("pages_section/9_Professional_Communication_Kit.py",
                                        title="Professional Communication Kit",
                                        icon="📋")


# Load authentication configuration
if authentication_required:
    if "credentials" in st.secrets:
        authenticator = stauth.Authenticate(
            st.secrets["credentials"].to_dict(),
            st.secrets["cookie"]["name"],
            st.secrets["cookie"]["key"],
            st.secrets["cookie"]["expiry_days"],
        )
    else:
        authenticator = None  # No authentication should be performed

client = None
if azure_openai_endpoint and azure_openai_key:
    client = openai.AzureOpenAI(
        api_key=azure_openai_key,
        api_version="2024-05-01-preview",
        azure_endpoint=azure_openai_endpoint,
    )
else:
    client = openai.OpenAI(api_key=openai_api_key)

class EventHandler(AssistantEventHandler):
    def __init__(self, thread_id):
        super().__init__()
        self.run_id = None
        self.thread_id = thread_id

    @override
    def on_event(self, event):
        if hasattr(event, 'run_id') and event.run_id:
            self.run_id = event.run_id

    @override
    def on_text_created(self, text):
        st.session_state.current_message = ""
        with st.chat_message("Assistant"):
            st.session_state.current_markdown = st.empty()

    @override
    def on_text_delta(self, delta, snapshot):
        if snapshot.value:
            text_value = re.sub(
                r"\[(.*?)\]\s*\(\s*(.*?)\s*\)", "Download Link", snapshot.value
            )
            st.session_state.current_message = text_value
            st.session_state.current_markdown.markdown(
                st.session_state.current_message, True
            )

    @override
    def on_text_done(self, text):
        format_text = format_annotation(text)
        st.session_state.current_markdown.markdown(format_text, True)
        current_page = st.session_state.get('current_page', 'Unknown Page')
        if current_page not in st.session_state.page_chat_logs:
            st.session_state.page_chat_logs[current_page] = []
        st.session_state.page_chat_logs[current_page].append({"name": "assistant", "msg": format_text})
        # Retrieve run_id from the last assistant message
        last_message = client.beta.threads.messages.list(
            thread_id=self.thread_id, limit=1
        ).data[0]
        if last_message.role == "assistant" and last_message.run_id:
            self.run_id = last_message.run_id

    # @override
    # def on_tool_call_created(self, tool_call):
    #     if tool_call.type == "code_interpreter":
    #         st.session_state.current_tool_input = ""
    #         with st.chat_message("Assistant"):
    #             st.session_state.current_tool_input_markdown = st.empty()

    # @override
    # def on_tool_call_delta(self, delta, snapshot):
    #     if 'current_tool_input_markdown' not in st.session_state:
    #         with st.chat_message("Assistant"):
    #             st.session_state.current_tool_input_markdown = st.empty()

    #     if delta.type == "code_interpreter":
    #         if delta.code_interpreter.input:
    #             st.session_state.current_tool_input += delta.code_interpreter.input
    #             input_code = f"### code interpreter\ninput:\n```python\n{st.session_state.current_tool_input}\n```"
    #             st.session_state.current_tool_input_markdown.markdown(input_code, True)

    #         if delta.code_interpreter.outputs:
    #             for output in delta.code_interpreter.outputs:
    #                 if output.type == "logs":
    #                     pass

    # @override
    # def on_tool_call_done(self, tool_call):
    #     st.session_state.tool_calls.append(tool_call)
    #     if tool_call.type == "code_interpreter":
    #         if tool_call.id in [x.id for x in st.session_state.tool_calls]:
    #             return
    #         input_code = f"### code interpreter\ninput:\n```python\n{tool_call.code_interpreter.input}\n```"
    #         st.session_state.current_tool_input_markdown.markdown(input_code, True)
    #         st.session_state.chat_log.append({"name": "assistant", "msg": input_code})
    #         st.session_state.current_tool_input_markdown = None
    #         for output in tool_call.code_interpreter.outputs:
    #             if output.type == "logs":
    #                 output = f"### code interpreter\noutput:\n```\n{output.logs}\n```"
    #                 with st.chat_message("Assistant"):
    #                     st.markdown(output, True)
    #                     st.session_state.chat_log.append(
    #                         {"name": "assistant", "msg": output}
    #                     )
    #     elif (
    #         tool_call.type == "function"
    #         and self.current_run.status == "requires_action"
    #     ):
    #         with st.chat_message("Assistant"):
    #             msg = f"### Function Calling: {tool_call.function.name}"
    #             st.markdown(msg, True)
    #             st.session_state.chat_log.append({"name": "assistant", "msg": msg})
    #         tool_calls = self.current_run.required_action.submit_tool_outputs.tool_calls
    #         tool_outputs = []
    #         for submit_tool_call in tool_calls:
    #             tool_function_name = submit_tool_call.function.name
    #             tool_function_arguments = json.loads(
    #                 submit_tool_call.function.arguments
    #             )
    #             tool_function_output = TOOL_MAP[tool_function_name](
    #                 **tool_function_arguments
    #             )
    #             tool_outputs.append(
    #                 {
    #                     "tool_call_id": submit_tool_call.id,
    #                     "output": tool_function_output,
    #                 }
    #             )

    #         with client.beta.threads.runs.submit_tool_outputs_stream(
    #             thread_id=st.session_state.thread.id,
    #             run_id=self.current_run.id,
    #             tool_outputs=tool_outputs,
    #             event_handler=EventHandler(),
    #         ) as stream:
    #             stream.until_done()

def generate_session_id():
    return str(uuid.uuid4())

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


def create_thread(content, file):
    current_page = st.session_state.get('current_page', 'Unknown Page')
    if current_page not in st.session_state.page_thread_ids:
        thread = client.beta.threads.create()
        st.session_state.page_thread_ids[current_page] = thread.id
        st.session_state.page_chat_logs[current_page] = []
    return client.beta.threads.retrieve(st.session_state.page_thread_ids[current_page])


def create_message(thread, content, file):
    attachments = []
    if file is not None:
        attachments.append(
            {"file_id": file.id, "tools": [{"type": "code_interpreter"}, {"type": "file_search"}]}
        )
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=content, attachments=attachments
    )


def create_file_link(file_name, file_id):
    content = client.files.content(file_id)
    content_type = content.response.headers["content-type"]
    b64 = base64.b64encode(content.text.encode(content.encoding)).decode()
    link_tag = f'<a href="data:{content_type};base64,{b64}" download="{file_name}">Download Link</a>'
    return link_tag


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


def run_stream(user_input, file, selected_assistant_id):
    current_page = st.session_state.get('current_page', 'Unknown Page')
    
    if current_page not in st.session_state.page_thread_ids:
        thread = client.beta.threads.create()
        st.session_state.page_thread_ids[current_page] = thread.id
    else:
        thread = client.beta.threads.retrieve(st.session_state.page_thread_ids[current_page])
    
    create_message(thread, user_input, file)
    
    event_handler = EventHandler(thread.id)
    
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=selected_assistant_id,
        event_handler=event_handler,
    ) as stream:
        stream.until_done()

    # Check if the run_id was captured
    run_id = event_handler.run_id
    if not run_id:
        raise RuntimeError("Failed to retrieve run ID")

    # Fetch the run details using the run_id
    run_details = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run_id)

    # Extract the required details from the run object
    assistant_id = run_details.assistant_id
    model = run_details.model
    prompt_tokens = run_details.usage.prompt_tokens
    completion_tokens = run_details.usage.completion_tokens
    total_tokens = run_details.usage.total_tokens

    # Save chat history after the stream is complete
    last_assistant_message = client.beta.threads.messages.list(thread_id=thread.id).data[0]

    save_chat_history(
        st.session_state['session_id'],
        st.session_state['username'],
        get_student_id(st.session_state['username']),
        user_input,
        last_assistant_message.content[0].text.value,
        assistant_id,
        model,
        prompt_tokens,
        completion_tokens,
        total_tokens
    )

def handle_uploaded_file(uploaded_file):
    file = client.files.create(file=uploaded_file, purpose="assistants")
    return file


def render_chat():
    current_page = st.session_state.get('current_page', 'Unknown Page')
    if current_page in st.session_state.page_chat_logs:
        for chat in st.session_state.page_chat_logs[current_page]:
            with st.chat_message(chat["name"]):
                st.markdown(chat["msg"], True)


if "tool_call" not in st.session_state:
    st.session_state.tool_calls = []

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

if "in_progress" not in st.session_state:
    st.session_state.in_progress = False


def disable_form():
    st.session_state.in_progress = True


def reset_chat():
    current_page = st.session_state.get('current_page', 'Unknown Page')
    if current_page in st.session_state.page_chat_logs:
        st.session_state.page_chat_logs[current_page] = []
    st.session_state.in_progress = False

def load_chat_screen(assistant_id, assistant_title,assistant_message):
    current_page = st.session_state.get('current_page', 'Unknown Page')

    uploaded_file = st.sidebar.file_uploader(
        enabled_file_upload_message,
        type=[
            "txt",
            "pdf",
            "json",
        ],
        disabled=st.session_state.in_progress,
    )

    # Initialize chat logs and thread ID for the current page if they don't exist
    if 'page_chat_logs' not in st.session_state:
        st.session_state.page_chat_logs = {}
    if 'page_thread_ids' not in st.session_state:
        st.session_state.page_thread_ids = {}
    
    if current_page not in st.session_state.page_chat_logs:
        st.session_state.page_chat_logs[current_page] = []
    if current_page not in st.session_state.page_thread_ids:
        thread = client.beta.threads.create()
        st.session_state.page_thread_ids[current_page] = thread.id

    st.title(assistant_title if assistant_title else "")
    st.info(assistant_message)
    st.write(f"Halo, bisa perkenalkan namamu?")
    
    # Render existing chat for this page
    for chat in st.session_state.page_chat_logs[current_page]:
        with st.chat_message(chat["name"]):
            st.markdown(chat["msg"], True)

    user_msg = st.chat_input(
        "Message", on_submit=disable_form, disabled=st.session_state.in_progress
    )
    if user_msg:
        with st.chat_message("user"):
            st.markdown(user_msg, True)
        st.session_state.page_chat_logs[current_page].append({"name": "user", "msg": user_msg})

        file = None
        if uploaded_file is not None:
            file = handle_uploaded_file(uploaded_file)
        run_stream(user_msg, file, assistant_id)
        st.session_state.in_progress = False
        st.session_state.tool_call = None
        st.rerun()
        
def generate_custom_api_response(api_url, headers, question, session_id=None):
    # Create the payload for the API request
    payload = {
        "question": question,
        "streaming": False  # Assuming the API supports streaming, else you can remove this
    }
    
    # Send the sessionId if available, otherwise leave it out for the first request
    if session_id:
        payload["sessionId"] = session_id

    # Send the request to the custom API endpoint
    response = requests.post(api_url, json=payload, headers=headers)

    # Return the response content as JSON if status is 200 OK
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error {response.status_code}: {response.text}")
        return None

# Function to load the chat interface and handle Flowise API interaction
def load_flowise_chat_screen(api_url, headers, assistant_title, assistant_message):
    current_page = st.session_state.get('current_page', 'Flowise Chat')

    # File uploader (optional, depending on your use case)
    uploaded_file = st.sidebar.file_uploader(
        "Upload a file if needed (txt, pdf, json)",  # Adjust the message as needed
        type=["txt", "pdf", "json"],
        disabled=st.session_state.get('in_progress', False),
    )

    # Initialize chat logs for the current page if they don't exist
    if 'page_chat_logs' not in st.session_state:
        st.session_state.page_chat_logs = {}

    if current_page not in st.session_state.page_chat_logs:
        st.session_state.page_chat_logs[current_page] = []

    st.title(assistant_title if assistant_title else "")
    st.info(assistant_message)
    st.write("Halo, bisa perkenalkan namamu?")  # Initial greeting message
    
    # Render existing chat for this page
    for chat in st.session_state.page_chat_logs[current_page]:
        with st.chat_message(chat["name"]):
            st.markdown(chat["msg"], True)

    user_msg = st.chat_input(
        "Message", on_submit=None, disabled=st.session_state.get('in_progress', False)
    )
    
    if user_msg:
        # Display the user message
        with st.chat_message("user"):
            st.markdown(user_msg, True)
        st.session_state.page_chat_logs[current_page].append({"name": "user", "msg": user_msg})

        # Fetch the session ID from state if it exists, else leave it None
        session_id = st.session_state.get('flowise_session_id', None)

        # Custom API response
        st.write("Asking Flowise via custom API...")
        response_json = generate_custom_api_response(api_url, headers, user_msg, session_id)
        
        if response_json:
            # Extract the sessionId and store it in the session state for future messages
            if 'sessionId' in response_json:
                st.session_state['flowise_session_id'] = response_json['sessionId']

            # Extract the text from the response and display it
            flowise_reply = response_json.get('text', "No response received.")
            with st.chat_message("Flowise"):
                st.markdown(flowise_reply, True)
            st.session_state.page_chat_logs[current_page].append({"name": "Flowise", "msg": flowise_reply})
            
            # Optionally, extract and display additional information (e.g., sourceDocuments)
            if 'sourceDocuments' in response_json:
                st.write("Source Documents:")
                for doc in response_json['sourceDocuments']:
                    st.write(f"- Page {doc['metadata']['loc']['pageNumber']}: {doc['pageContent']}")

        # Reset the progress state
        st.session_state.in_progress = False
        st.rerun()  # Refresh the page to display new chat message


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
    st.title("💬 Revo AI Coach")
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

def logout():
    st.session_state['logged_in'] = False
    st.session_state.pop('username', None)
    st.session_state['chat_history'] = []
    st.session_state['session_id'] = []
    st.session_state.page_thread_ids = {}
    st.session_state.page_chat_logs = {}
    st.success("Logged out successfully!")
    reset_chat()
    st.rerun()

def get_current_page_name(pg):
    if pg and hasattr(pg, 'title'):
        st.session_state['current_page'] = pg.title
        return pg.title
    return "Unknown Page"

def main():
    st.logo("https://cdn.prod.website-files.com/61af164800e38c4f53c60b4e/61af164800e38c11efc60b6d_RevoU.svg")
    st.set_page_config(page_title="Revo AI Coach")

    # Initialize session state
    if "page_thread_ids" not in st.session_state:
        st.session_state.page_thread_ids = {}
    if "page_chat_logs" not in st.session_state:
        st.session_state.page_chat_logs = {}
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = generate_session_id()
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = "Home"
        
    if st.session_state['logged_in']:
        pg = st.navigation({
            "Home" : [message],
            "Personal Branding Discovery": [flowise, relevance_experiences_discovery,experience_detail_discovery],
            "Assets Content Crafting": [about_me_summary_crafting, professionals_and_organizational_experience_crafting, project_crafting],
            "Quality Application Support": [assets_personalization_kit,professional_communication_kit],
            "Logout": [st.Page(logout, title="Logout", icon="🚪")]
        })
    else:
        pg = st.navigation([st.Page(login, title="Login", icon="🔑")])

    # Set the current page in session state
    if pg and hasattr(pg, 'title'):
        st.session_state['current_page'] = pg.title
    else:
        st.session_state['current_page'] = "Unknown Page"

    # Main content
    if not st.session_state['logged_in']:
        login()
    else:        
        pg.run()
        
if __name__ == "__main__":
    main()
