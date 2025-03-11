import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from database import read_sql_query  # Import database functions from database.py

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API key (retrieved from environment variables)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to generate SQL query using Gemini AI
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')  # Load Gemini model
    response = model.generate_content([prompt[0], question])  # Get response from AI
    return response.text.strip()  # Return only the generated SQL query

# Define prompt to instruct Gemini on how to convert text to SQL queries
prompt = [
    """
    You are an expert in converting English questions to SQL queries!
    The database name is STUDENT with columns: NAME, CLASS, SECTION, SCORE.

    Example:
    - Question: How many records are in the table?
      SQL Query: SELECT COUNT(*) FROM STUDENT;

    - Question: List all students in Data Science.
      SQL Query: SELECT * FROM STUDENT WHERE CLASS='Data Science';

    Make sure:
    1. Do NOT include `sql` or ``` in the response.
    2. Generate only valid SQL queries.
    3. Do NOT delete existing table data.
    """
]

# Set up the Streamlit app with a specific page title
st.set_page_config(page_title="Text2SQL")

# Display the main header of the application
st.title("Convert Text to SQL Queries")

# Display the subheader of the application
st.subheader("Developed by Emon Hasan")

# User input for the question
question = st.text_input("Enter your question:")

# Button to generate SQL query
if st.button("Generate & Execute SQL Query"):
    if question:  # Ensure input is not empty
        sql_query = get_gemini_response(question, prompt)  # Convert question to SQL query
        st.subheader("Generated SQL Query:")  # Display generated SQL query
        st.code(sql_query, language="sql")  # Show SQL query in formatted code block

        # Execute the SQL query on the database
        response = read_sql_query(sql_query)

        # Display results
        st.subheader("Query Result:")
        if response:
            for row in response:
                st.write(row)  # Display each row of query results
        else:
            st.write("No data found.")  # Show warning if query returns no results
    else:
        st.warning("Please enter a question.")  # Show warning if input is empty
