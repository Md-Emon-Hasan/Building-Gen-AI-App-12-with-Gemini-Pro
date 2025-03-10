# Import necessary modules
from dotenv import load_dotenv  # For loading environment variables from a .env file
import streamlit as st  # Streamlit for creating web applications
import os  # For operating system interactions
from PIL import Image  # For image processing
import google.generativeai as genai  # Google's Generative AI library

# Load environment variables from a .env file
load_dotenv()

# Retrieve the Google API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")

# Check if the API key is available
if api_key:
    # Configure the Generative AI client with the API key
    genai.configure(api_key=api_key)
else:
    # Display an error message if the API key is missing
    st.error("Google API key is missing. Please set it in the environment variables.")

# Function to load the Gemini model and get responses
def get_gemini_response(input_text, image=None):
    # Initialize the Gemini 2.0 Flash model
    model = genai.GenerativeModel('gemini-1.5-pro')
    # Generate content based on input text and image
    if input_text and image:
        response = model.generate_content([input_text, image])
    elif input_text:
        response = model.generate_content(input_text)
    elif image:
        response = model.generate_content(image)
    else:
        response = None
    # Return the generated response text
    return response.text if response else "No input provided."

# Initialize the Streamlit app with a specific page title
st.set_page_config(page_title="Image Q&A Demo")

# Display the main header of the application
st.title("Image Analysis with Q&A Chatbot")

# Display the subheader of the application
st.subheader("Developed by Emon Hasan")

# Create a text input field for user prompts
input_text = st.text_input("Input Prompt:", key="input")

# Create a file uploader for users to upload images
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Initialize the image variable
image = None

# If an image file is uploaded, open and display it
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)

# Create a button for submitting the input
submit = st.button("Tell me about the image")

# If the submit button is clicked
if submit:
    # Check if the API key is available before making a request
    if api_key:
        # Get the response from the Gemini model
        response = get_gemini_response(input_text, image)
        # Display the response in a subheader
        st.subheader("The Response is")
        st.write(response)
    else:
        # Display an error message if the API key is missing
        st.error("Cannot generate response without a valid API key.")
