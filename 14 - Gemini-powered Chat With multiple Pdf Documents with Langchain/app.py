import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Google API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")

# Configure Google Generative AI with API key
genai.configure(api_key=api_key)

# Function to extract text from uploaded PDF files
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)  # Read the PDF file
        for page in pdf_reader.pages:
            text += page.extract_text()  # Extract text from each page
    return text

# Function to split text into smaller chunks for better processing
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)  # Split text into chunks
    return chunks

# Function to generate vector embeddings and store them in FAISS
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")  # Load embedding model
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)  # Create FAISS vector store
    vector_store.save_local("faiss_index")  # Save FAISS index locally

# Function to create a conversational AI model
def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context. Make sure to provide all the details. 
    If the answer is not in the provided context, just say, "answer is not available in the context", 
    and don't provide a wrong answer.

    Context:
    {context}?
    
    Question:
    {question}

    Answer:
    """
    
    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)  # Load Gemini AI model
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])  # Define prompt template
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)  # Load QA chain
    return chain

# Function to handle user input and return an AI-generated response
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")  # Load embedding model
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)  # Load FAISS index
    docs = new_db.similarity_search(user_question)  # Perform similarity search on user query
    chain = get_conversational_chain()  # Get conversational AI chain
    
    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )  # Generate response using AI model

    print(response)  # Print response in console (for debugging)
    st.write("Reply:", response["output_text"])  # Display response in Streamlit app

# Main function to handle Streamlit UI
def main():
    # Set up the Streamlit app with a specific page title
    st.set_page_config(page_title="Chat with PDF")

    # Display the main header of the application
    st.title("Chat With multiple Pdf Documents with Langchain")

    # Display the subheader of the application
    st.subheader("Developed by Emon Hasan")
    
    # Input field for user question
    user_question = st.text_input("Ask a Question from the PDF Files")
    
    # Button to submit user question
    if st.button("Submit Question"):
        if user_question:
            user_input(user_question)  # Process user question
    
    with st.sidebar:
        st.title("Menu:")  # Sidebar title
        
        # File uploader for PDF files
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        
        # Button to process uploaded PDF files
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)  # Extract text from PDFs
                text_chunks = get_text_chunks(raw_text)  # Split text into chunks
                get_vector_store(text_chunks)  # Store text in FAISS vector store
                st.success("Done")  # Display success message

# Run the Streamlit app
if __name__ == "__main__":
    main()
