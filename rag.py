# Import necessary libraries
import langchain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain import hub

# Additional imports
import os
import re
import time

# Initialize the OpenAI client (ensure your API key is set up)
client = langchain.llms.OpenAI()

# Setup the directory for database
persist_directory = 'db'
embedding = OpenAIEmbeddings()

# Initialize the vector database
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

# Create a retriever
retriever = vectordb.as_retriever(search_kwargs={"k": 10})

# Initialize the LLM
llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0)

# Define format_docs function
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Create the custom RAG prompt
template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Use three sentences maximum and keep the answer as concise as possible. 
Always say "thanks for asking!" at the end of the answer. 
{context}
Question: {question}
Helpful Answer:"""
rag_prompt_custom = PromptTemplate.from_template(template)

# Define the RAG chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt_custom
    | llm
    | StrOutputParser()
)

# Function to handle chat and questions using RAG chain
def handle_chat():
    while True:
        question = input("Ask a question: ")
        if question.lower() == 'exit':
            break
        response = rag_chain.invoke(question)
        print(response)

# Start the chat
handle_chat()
