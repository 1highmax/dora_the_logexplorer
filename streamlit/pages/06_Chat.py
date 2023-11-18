import streamlit as st
import utils.streamlit_utils as st_utils

st.set_page_config(page_title="Chat", layout='wide')

# Placeholder for the chatbot function
def chatbot_response(message):
    # Your chatbot logic goes here. For now, it just echoes the input.
    return f"Dora: {message}"

def process_file(uploaded_file):
    # Dummy function to represent file processing
    # You can replace this with your actual file processing logic
    return f"Processed {uploaded_file.name}"

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

with col1:
    # Create a file uploader widget
    uploaded_file = st.file_uploader("Upload a log file", type=["txt", "out"])

    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the content of the file
        content = uploaded_file.getvalue().decode("utf-8")

        # Display the file content in a text area
        st.text_area("File content", content, height=300)
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
    user_input = st.text_input("Your message", key="user_input", on_change=send_message)

    # Button to send the message
    if st.button('Send'):
        send_message()
