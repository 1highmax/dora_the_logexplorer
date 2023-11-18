# Import libraries
import langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader, TextLoader
import re

def extract_log_data(line):
    # Regular expression to match the time, prefix, and message
    pattern = r'(\b\w{3}\s\d{2}\s\d{2}:\d{2}:\d{2}\b)\s+(.*?)\s*:\s*(.*)'
    match = re.match(pattern, line)
    if match:
        time, prefix, message = match.groups()
        return time, prefix, message
    else:
        return None, None, None



    

import hashlib

# Function to generate a unique hash for a file
def generate_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()

def create_database(saved_file_path):
    print("starting")
    # OpenAI embeddings
    embedding = OpenAIEmbeddings()
    log_data=[]
    lines = []
    file_path = saved_file_path
    persist_directory = 'streamlit/db'

    loader = TextLoader(saved_file_path, encoding = 'UTF-8')
    doc = loader.load()
    len(doc)

    # Splitting the text into chunks
    text_splitter = RecursiveCharacterTextSplitter (chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(doc)

    # Count the number of chunks
    len(texts)

    # Generate a unique identifier for the file
    file_identifier = generate_file_hash(file_path)

    # Use the unique identifier in the persist directory
    unique_persist_directory = os.path.join(persist_directory, file_identifier)

    # Initialize the vector database with the unique persist directory
    vectordb = Chroma.from_documents(documents=texts,
                                    embedding=embedding,
                                    persist_directory=unique_persist_directory)
    vectordb.persist()

    print("Vectordb initialized with unique persist directory:", unique_persist_directory)