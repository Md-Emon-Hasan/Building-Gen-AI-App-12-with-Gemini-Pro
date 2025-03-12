import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables from .env file (like Google API key)
load_dotenv()

# Configure Gemini API Key using environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the prompt used to summarize the YouTube video transcript
prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video, providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

# Function to extract transcript from YouTube video using YouTubeTranscriptApi
def extract_transcript_details(youtube_video_url):
    try:
        # Extract video ID from the YouTube URL
        video_id = youtube_video_url.split("=")[1]

        # Retrieve the transcript of the video
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        # Combine all transcript text into one string
        transcript = ""
        for item in transcript_text:
            transcript += " " + item["text"]

        return transcript

    except Exception as e:
        # If an error occurs, display an error message
        st.error(f"Error extracting transcript: {e}")
        return None
    
# Function to generate summary using Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    # Using the Gemini model to generate content
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit app configuration
# Initialize the Streamlit app and set the page title
st.set_page_config(page_title="YouTube Transcript")

# Display the main header for the app
st.title("YouTube Transcript to Detailed Notes Converter")

# Display the subheader, which shows the developer's name
st.subheader("Developed by Emon Hasan")

# Input box for YouTube video link
youtube_link = st.text_input("Enter YouTube Video Link:")

# If the link is provided, display the thumbnail of the video
if youtube_link:
    try:
        # Extract the video ID and display the video thumbnail
        video_id = youtube_link.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
    except IndexError:
        st.error("⚠️ Please enter a valid YouTube URL with the video ID.")

# Button to trigger the transcript extraction and summarization process
if st.button("Get Detailed Notes"):
    if youtube_link:
        # Get the transcript text from YouTube
        transcript_text = extract_transcript_details(youtube_link)

        if transcript_text:
            # Generate the summary based on the transcript
            summary = generate_gemini_content(transcript_text, prompt)

            # Display the generated summary
            st.markdown("## Detailed Notes:")
            st.write(summary)
        else:
            # If no transcript is found, display a warning
            st.warning("⚠️ No transcript available for this video. Please try another one.")
    else:
        # If no link is entered, show a warning
        st.warning("⚠️ Please enter a valid YouTube video link.")
