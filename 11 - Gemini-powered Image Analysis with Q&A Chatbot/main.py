# Import necessary libraries
from dotenv import load_dotenv  # For loading environment variables from a .env file
import streamlit as st  # For building the web application interface
import os  # For interacting with the operating system
import textwrap  # For text formatting
import google.generativeai as genai  # For interacting with Google's Generative AI models
from IPython.display import display, Markdown  # For displaying content in Jupyter notebooks

# Function to convert text to Markdown format
def to_markdown(text):
    text = text.replace('•', '  *')  # Replace bullet points with Markdown list format
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))  # Indent text for blockquote

# Load environment variables from .env file
load_dotenv()

# Retrieve the Google API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")

# Check if the API key is available
if api_key:
    # Configure the Generative AI client with the API key
    genai.configure(api_key=api_key)
else:
    # Display an error message if the API key is not found
    st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")

# Function to get a response from the Gemini model
def get_gemini_response(question):
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-1.5-pro')
    # Generate a response to the input question
    response = model.generate_content(question)
    # Return the text of the response
    return response.text

# Set up the Streamlit app with a title
st.set_page_config(page_title="Q&A Demo")

# Display the header of the app
st.header("Gemini Application")

# Create a text input field for the user's question
input_question = st.text_input("Input:", key="input")

# Create a button that the user can click to submit their question
submit = st.button("Ask the question")

# If the submit button is clicked
if submit:
    # Check if the input field is not empty
    if input_question.strip():
        # Get the response from the Gemini model
        response = get_gemini_response(input_question)
        # Display the response in a subheader
        st.subheader("The Response is")
        # Write the response text to the app
        st.write(response)
    else:
        # Display a warning message if the input field is empty
        st.warning("Please enter a question before submitting.")