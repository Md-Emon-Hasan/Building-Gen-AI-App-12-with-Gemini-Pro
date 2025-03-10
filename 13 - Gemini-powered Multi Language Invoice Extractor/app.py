# Q&A Chatbot Application
# Import necessary modules
from dotenv import load_dotenv  # For loading environment variables from a .env file
import streamlit as st  # Streamlit for creating web applications
import os  # For operating system interactions
from PIL import Image  # For image processing
import google.generativeai as genai  # Google's Generative AI library

# Load environment variables from a .env file
load_dotenv()  # This loads environment variables from a .env file into the environment

# Retrieve and configure the Google API key
api_key = os.getenv("GOOGLE_API_KEY")  # Fetch the API key from environment variables
genai.configure(api_key=api_key)  # Configure the Generative AI client with the API key

def get_gemini_response(input_text, image, prompt):
    """
    Generate a response using the Gemini AI model based on the provided input text, image, and prompt.

    Args:
        input_text (str): The textual input provided by the user.
        image (list): A list containing image data.
        prompt (str): A predefined prompt to guide the AI's response.

    Returns:
        str: The generated response text from the AI model.
    """
    # Initialize the Gemini AI model
    model = genai.GenerativeModel('gemini-1.5-pro')
    # Generate content based on the input text, image, and prompt
    response = model.generate_content([input_text, image[0], prompt])
    # Return the generated response text
    return response.text

def input_image_setup(uploaded_file):
    """
    Prepare the uploaded image for processing.

    Args:
        uploaded_file (UploadedFile): The image file uploaded by the user.

    Returns:
        list: A list containing the image data and its MIME type.

    Raises:
        FileNotFoundError: If no file is uploaded.
    """
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        # Prepare the image data with its MIME type
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the MIME type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        # Raise an error if no file is uploaded
        raise FileNotFoundError("No file uploaded")

# Set up the Streamlit app with a specific page title
st.set_page_config(page_title="Invoice Extractor")

# Display the main header of the application
st.title("Multi Language Invoice Extractor")

# Display the subheader of the application
st.subheader("Developed by Emon Hasan")

# Create a text input field for user prompts
input_text = st.text_input("Input Prompt: ", key="input")

# Create a file uploader for users to upload images
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Initialize the image variable
image = ""   
if uploaded_file is not None:
    # Open and display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)

# Create a button for submitting the input
submit = st.button("Tell me about the image")

# Define a prompt for the AI model
input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """

# If the submit button is clicked
if submit:
    try:
        # Prepare the image data
        image_data = input_image_setup(uploaded_file)
        # Get the response from the Gemini model
        response = get_gemini_response(input_text, image_data, input_prompt)
        # Display the response
        st.subheader("The Response is")
        st.write(response)
    except FileNotFoundError as e:
        # Display an error message if no file is uploaded
        st.error(str(e))