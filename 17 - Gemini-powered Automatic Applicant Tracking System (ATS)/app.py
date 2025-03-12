# Import necessary libraries
import streamlit as st  # Streamlit for creating the web app interface
from dotenv import load_dotenv  # Load environment variables from a .env file
import os  # Access environment variables and file paths
import io  # Handle input/output operations
import base64  # Encode binary data to base64
from PIL import Image  # Image processing using Python Imaging Library
import google.generativeai as genai  # Google's Generative AI for AI-powered responses

# Load environment variables from the .env file
load_dotenv()

# Configure the Gemini API Key using the environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to process the uploaded image file
def process_uploaded_image(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Open the uploaded image file
        image = Image.open(uploaded_file)

        # Convert the image to RGB mode if it is not already in RGB
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Convert the image to a byte array
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')  # Save the image in JPEG format
        img_byte_arr = img_byte_arr.getvalue()  # Get the byte array of the image

        # Prepare the image data in a dictionary format
        image_data = {
            "mime_type": "image/jpeg",  # Specify the MIME type of the image
            "data": base64.b64encode(img_byte_arr).decode()  # Encode the image data to base64
        }

        # Return the image data as a list
        return [image_data]
    else:
        # Raise an error if no file is uploaded
        raise FileNotFoundError("No file uploaded")

# Function to get a response from Google Gemini based on the input prompt, image content, and job description
def get_gemini_response(input_prompt, image_content, job_description):
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-1.5-pro')
    # Generate a response using the model
    response = model.generate_content([input_prompt, image_content[0], job_description])
    # Return the generated text response
    return response.text

# Streamlit UI Configuration
# Set the page title for the Streamlit app
st.set_page_config(page_title="ATS Resume Expert")

# Display the main header of the app
st.title("Automatic Applicant Tracking System (ATS)")

# Display the subheader with the developer's name
st.subheader("Developed by Emon Hasan")

# Input field for the job description
job_description = st.text_area("Enter Job Description:", key="input")

# File uploader for the resume image (JPG/PNG only)
uploaded_file = st.file_uploader("Upload Your Resume (JPG/PNG only)", type=["jpg", "jpeg", "png"])

# Display the uploaded image if a file is uploaded
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Resume", use_container_width=True)

# Create columns for organizing buttons
col1, col2, col3 = st.columns(3)

# Buttons for different functionalities in the first column
with col1:
    submit1 = st.button("Analyze Resume")  # Button to analyze the resume
    submit2 = st.button("Improve My Skills")  # Button to suggest skill improvements
    submit5 = st.button("Keywords Matching")  # Button to analyze keyword matching

# Buttons for different functionalities in the second column
with col2:
    submit3 = st.button("Match Percentage")  # Button to calculate ATS match percentage
    submit4 = st.button("Resume Optimization")  # Button to optimize the resume
    submit6 = st.button("HR's Perspective")  # Button to get HR's perspective

# Buttons for different functionalities in the third column
with col3:
    submit7 = st.button("Best Job Roles")  # Button to suggest best job roles
    submit8 = st.button("Download ATS-Friendly Resume")  # Button to download ATS-friendly resume
    submit9 = st.button("Candidate Strengths & Weaknesses")  # Button to analyze strengths and weaknesses
    submit10 = st.button("Skills Gap Analysis")  # Button to perform skills gap analysis

# Button to get a complete analysis of the resume
submit_all = st.button("Get Complete Analysis")

# Dictionary of AI prompt templates for different functionalities
prompts = {
    "Resume Analysis": """
    You are an experienced HR manager. Analyze the resume image and compare it to the job description.
    Provide a professional evaluation, highlighting strengths, weaknesses, and missing skills.
    """,
    
    "Skill Improvement": """
    You are an AI career advisor. Based on the job description, suggest key skills the candidate needs to improve.
    Recommend courses, certifications, or projects to enhance their profile.
    """,
    
    "ATS Match Percentage": """
    You are an ATS scanner. Compare the resume to the job description:
    - Provide a percentage match score.
    - List missing keywords.
    - Give final thoughts on compatibility.
    """,
    
    "Resume Optimization": """
    You are an AI resume optimizer. Rewrite key sections of the resume to improve clarity, ATS compatibility, and keyword density.
    Make the bullet points action-oriented.
    """,
    
    "Keywords Analysis": """
    You are an AI keyword extractor. Identify keywords in the resume that match the job description.
    Highlight missing important keywords that should be included.
    """,
    
    "HR Perspective": """
    You are an AI-powered recruiter. Simulate how HR would scan this resume.
    Point out things a recruiter might notice first and suggest improvements.
    """,
    
    "Suggested Job Roles": """
    You are a job recommendation AI. Based on the resume, suggest the top 5 job roles that match the candidate’s skills.
    """,
    
    "Candidate Strengths & Weaknesses": """
    You are an experienced HR professional. Analyze the strengths and weaknesses of the candidate based on the uploaded resume and the provided job description. Provide actionable feedback.
    """,
    
    "Skills Gap Analysis": """
    You are an AI career advisor. Analyze the skills gap between the candidate’s resume and the job description. Provide suggestions for how to bridge the gaps.
    """
}

# Combined prompt for the 'Get Complete Analysis' button
combined_prompt = """
Perform a comprehensive ATS resume analysis based on the uploaded resume and job description.
Provide insights on the following aspects:
1️⃣ **Resume Analysis** - Overall strengths and weaknesses of the resume.
2️⃣ **Skills Improvement** - Key technical and soft skills to improve.
3️⃣ **ATS Match Percentage** - A score indicating how well the resume matches the job.
4️⃣ **Resume Optimization** - Suggestions to enhance the resume for ATS systems.
5️⃣ **Keyword Matching** - Important keywords missing from the resume.
6️⃣ **HR Perspective** - How an HR professional would evaluate this resume.
7️⃣ **Best Job Roles** - Recommended roles based on resume skills.
8️⃣ **Candidate Strengths & Weaknesses** - A deep analysis of strengths and areas to work on.
9️⃣ **Skills Gap Analysis** - Identify missing skills and how to acquire them.

Make the summary brief, clear, and professional.
"""

# Handling button clicks and displaying results
if uploaded_file:
    # Process the uploaded image
    image_content = process_uploaded_image(uploaded_file)

    # Handle the 'Analyze Resume' button click
    if submit1:
        st.subheader("Resume Analysis:")
        st.write(get_gemini_response(prompts["Resume Analysis"], image_content, job_description))

    # Handle the 'Improve My Skills' button click
    if submit2:
        st.subheader("Skill Improvement Suggestions:")
        st.write(get_gemini_response(prompts["Skill Improvement"], image_content, job_description))

    # Handle the 'Match Percentage' button click
    if submit3:
        st.subheader("ATS Match Percentage:")
        st.write(get_gemini_response(prompts["ATS Match Percentage"], image_content, job_description))

    # Handle the 'Resume Optimization' button click
    if submit4:
        st.subheader("Optimized Resume Suggestions:")
        st.write(get_gemini_response(prompts["Resume Optimization"], image_content, job_description))

    # Handle the 'Keywords Matching' button click
    if submit5:
        st.subheader("Keywords Analysis:")
        st.write(get_gemini_response(prompts["Keywords Analysis"], image_content, job_description))

    # Handle the 'HR's Perspective' button click
    if submit6:
        st.subheader("HR's Perspective:")
        st.write(get_gemini_response(prompts["HR Perspective"], image_content, job_description))

    # Handle the 'Best Job Roles' button click
    if submit7:
        st.subheader("Suggested Job Roles:")
        st.write(get_gemini_response(prompts["Suggested Job Roles"], image_content, job_description))

    # Handle the 'Download ATS-Friendly Resume' button click
    if submit8:
        st.info("Coming Soon: AI-Generated ATS-Friendly Resume Templates!")

    # Handle the 'Candidate Strengths & Weaknesses' button click
    if submit9:
        st.subheader("Candidate Strengths & Weaknesses:")
        st.write(get_gemini_response(prompts["Candidate Strengths & Weaknesses"], image_content, job_description))

    # Handle the 'Skills Gap Analysis' button click
    if submit10:
        st.subheader("Skills Gap Analysis:")
        st.write(get_gemini_response(prompts["Skills Gap Analysis"], image_content, job_description))

    # Handle the 'Get Complete Analysis' button click
    if submit_all:
        st.subheader("Complete Resume Analysis Report:")
        st.write(get_gemini_response(combined_prompt, image_content, job_description))
else:
    # Display an error message if no resume is uploaded
    st.error("Please upload a resume image before proceeding.")
