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
from openai import OpenAI
import time
from summary import to_dict


context_history = ""

# Initialize the OpenAI client
client = OpenAI()

# Setup the directory for database
persist_directory = 'db_final'
embedding = OpenAIEmbeddings()

# Initialize the vector database
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

# Create a retriever
retriever = vectordb.as_retriever(search_kwargs={"k": 10})

# Initialize the LLM
llmm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0)

# Create the QA chain
qa_chain = RetrievalQA.from_chain_type(llm=llmm,
                                       chain_type="stuff",
                                       retriever=retriever,
                                       return_source_documents=True,
                                       verbose=True)

# Function to process the LLM response
def process_llm_response(llm_response):
    response = llm_response['result']
    sources = '\n\nSources:\n' + '\n'.join([source.metadata['source'] for source in llm_response["source_documents"]])
    return response + sources

def handle_chat():
    global context_history  # Use the global context history variable

    while True:
        question = input("Ask a question: ")
        if question.lower() == 'exit':
            break

        # Update context with the new question
        context_history += f'Question: {question}\n'

        docs = retriever.get_relevant_documents(question)
        if not docs:
            print("No relevant documents found.")
            continue

        # Include the context in the LLM invocation
        # The method to invoke the LLM might differ; this is a generalized example
        llm_response = qa_chain("Context so far:\n" + context_history + "\n\n\n" + question)  # Adjust this line as per LangChain's implementation
        response = process_llm_response(llm_response)
        print(response)

        # Update context with the response
        context_history += f'Answer: {response}\n'

# Start the chat
handle_chat()
