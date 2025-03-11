import streamlit as st
import os
import shutil
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API Keys from environment variables
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

# Initialize the LLM using Google's Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)

# Initialize Google Generative AI embeddings for vector storage
st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Define structured prompt template for retrieval-augmented generation (RAG)
prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question.

    <context>
    {context}
    </context>

    Question: {input}
    """
)

# Create an upload directory for storing uploaded PDF files
UPLOAD_DIR = "uploaded_pdfs"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Set up the Streamlit app with a specific page title
st.set_page_config(page_title="Chat with PDF")

# Display the main header of the application
st.title("Document Q&A With GROQ API & Gemini")

# Display the subheader of the application
st.subheader("Developed by Emon Hasan")

# File Upload Option: Allows users to upload multiple PDFs
uploaded_files = st.file_uploader("Upload one or more PDF files", type=["pdf"], accept_multiple_files=True)

# Save uploaded PDFs to local directory
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())  # Save file to disk
    st.success("PDFs uploaded successfully!")  # Display success message

# Function to create FAISS vector embeddings from uploaded PDFs
def create_vector_embedding():
    if "vectors" not in st.session_state:
        # List all uploaded PDF files
        pdf_files = [os.path.join(UPLOAD_DIR, f) for f in os.listdir(UPLOAD_DIR) if f.endswith(".pdf")]
        if not pdf_files:
            st.error("No PDFs uploaded. Please upload documents first.")
            return
        
        # Load and process PDFs into documents
        documents = []
        for pdf_file in pdf_files:
            loader = PyPDFLoader(pdf_file)  # Load PDF content
            documents.extend(loader.load())  # Append extracted text
        
        # Split documents into smaller chunks for efficient processing
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        final_documents = text_splitter.split_documents(documents)
        
        if not final_documents:
            st.error("No text extracted from PDFs. Check the documents.")
            return

        # Create FAISS vector store from extracted text
        st.session_state.vectors = FAISS.from_documents(final_documents, st.session_state.embeddings)
        st.success("Vector database created successfully!")

# Button to trigger FAISS vector database creation
if st.button("Create Document Embeddings"):
    create_vector_embedding()

# User input box for entering queries
user_prompt = st.text_input("Enter your query from the research papers")

# Submit button to process user query
if st.button("Submit Query") and user_prompt:
    import time
    document_chain = create_stuff_documents_chain(llm, prompt)  # Create document processing chain
    
    # Ensure FAISS vector database is ready before querying
    if "vectors" not in st.session_state or st.session_state.vectors is None:
        st.error("Vector database is not ready. Click 'Create Document Embeddings' first.")
    else:
        retriever = st.session_state.vectors.as_retriever()  # Create retriever from FAISS
        retrieval_chain = create_retrieval_chain(retriever, document_chain)  # Create retrieval chain
        
        # Measure response time
        start = time.process_time()
        response = retrieval_chain.invoke({'input': user_prompt})
        elapsed_time = time.process_time() - start
        
        # Display the AI-generated answer
        st.subheader("Answer:")
        st.write(response['answer'])

        # Show relevant document snippets
        with st.expander("Document Similarity Search"):
            for i, doc in enumerate(response['context']):
                st.write(f"**Document {i+1}:**")
                st.write(doc.page_content)
                st.write('------------------------')
