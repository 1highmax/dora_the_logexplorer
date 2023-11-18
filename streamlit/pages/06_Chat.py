import streamlit as st
import utils.streamlit_utils as st_utils
from utils.chat_response import get_backend_response
from utils.log_to_db import process_log_file 
import os
import tempfile
from langchain.document_loaders import DirectoryLoader, TextLoader

st.set_page_config(page_title="Chat", layout='wide')

def cached_backend_response(message):
    response = get_backend_response(message)
    print("response: ", response)
    return response

# Placeholder for the chatbot function
def chatbot_response(message):
    # Now using the cached function to get the response
    return f"Dora: {cached_backend_response(message)}"


def save_uploaded_file(uploaded_file, directory="data", filename="uploaded_log.txt"):
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, filename)

    # Write the uploaded file to the file system
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getvalue())
    
    return file_path

# Function to display messages in speech bubbles
def display_message(message, is_user=True):
    bubble_color = "#009BEA" if is_user else "#A0A0A0"
    align_text = "right" if is_user else "left"
    html = f"""
    <div style="margin: 5px; padding: 10px; background-color: {bubble_color}; border-radius: 15px; text-align: {align_text}; max-width: 60%; float: {align_text}; clear: both;">
        {message}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# Function to handle sending messages
def send_message():
    user_input = st.session_state['user_input']
    if user_input:  # Check if the input is not empty
        # Add user message to conversation
        st.session_state['conversation'].append(user_input)
        
        # Get chatbot response and add to conversation
        response = chatbot_response(user_input)
        st.session_state['conversation'].append(response)

    # Reset the input box
    st.session_state['user_input'] = ""


st.header('Dora the Log-Explorer')

desc = """
Start questioning Dora about the specified log file.
"""
st.markdown(desc)

col1, col2 = st.columns(2)

# In your Streamlit app
with col1:
    uploaded_file = st.file_uploader("Upload a log file", type=["txt", "out"], key="log_file_uploader")

    if uploaded_file is not None:
        # Save the uploaded file and get its path
        saved_file_path = save_uploaded_file(uploaded_file)

        # Now you can use TextLoader to load from this file path
        loader = TextLoader(saved_file_path, encoding='UTF-8')
        doc = loader.load()

        # Process the file content with your function
        #vectordb = process_log_file(doc)

        #init()

        # Display the file content in a text area
        st.text_area("File content", doc, height=300)
    else:
        st.write("Please upload a text file.")

with col2:
    # Initialize session state to store conversation
    if 'conversation' not in st.session_state:
        st.session_state['conversation'] = []

    # Display existing conversation
    for i, message in enumerate(st.session_state['conversation']):
        is_user = i % 2 == 0
        display_message(message, is_user)

    # Text input for user message with a callback
    # Use a default value that resets each time the button is pressed
    default_value = "" if st.session_state.get('clear_input', False) else st.session_state.get('user_input', '')
    user_input = st.text_input("Your message", key="user_input", value=default_value, on_change=send_message)

    # Button to send the message
    if st.button('Send'):
        send_message()
        st.session_state['clear_input'] = True
