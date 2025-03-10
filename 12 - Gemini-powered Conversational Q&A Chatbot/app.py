# Import necessary modules
from dotenv import load_dotenv  # For loading environment variables from a .env file
import os  # For interacting with the operating system
import streamlit as st  # For building the web application
import google.generativeai as genai  # For interacting with Google's Generative AI

# Load environment variables from the .env file
load_dotenv()

# Configure the Generative AI client with the API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini Pro model and start a chat session
model = genai.GenerativeModel("gemini-1.5-pro")
chat = model.start_chat(history=[])

# Define a function to get responses from the Gemini model
def get_gemini_response(question):
    """
    Sends a question to the Gemini model and retrieves the response.

    Args:
        question (str): The user's question.

    Returns:
        response: The model's response, streamed in chunks.
    """
    response = chat.send_message(question, stream=True)
    return response

# Set up the Streamlit app with a specific page title
st.set_page_config(page_title="Q&A Demo")

# Display the main header of the application
st.title("Conversational Q&A Chatbot")

# Display the subheader of the application
st.subheader("Developed by Emon Hasan")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Create a text input field for user questions
input = st.text_input("Input:", key="input")

# Create a button for submitting the question
submit = st.button("Ask the question")

# Process the user's input when the submit button is pressed
if submit and input:
    # Get the model's response to the user's question
    response = get_gemini_response(input)

    # Add the user's question and the model's response to the chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Display the chat history
st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
