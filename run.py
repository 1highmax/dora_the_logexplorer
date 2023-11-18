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

client = OpenAI()

def searchDatabase(query):
    print("database query", query)

    persist_directory = 'db'
    embedding = OpenAIEmbeddings()
    # question = "what error were there in ssh?"
    question = "are there any anomalies in terms of systemd?"

    vectordb = Chroma(persist_directory=persist_directory,
                    embedding_function=embedding)

    retriever = vectordb.as_retriever(search_kwargs={"k": 10})
    docs = retriever.get_relevant_documents(question)
    print(docs) 


    # Write the result to a file
    with open('retrieval_results.txt', 'w') as file:
        for doc in docs:
            file.write(str(doc) + '\n')

    # Assume docs is the list of documents retrieved from Chroma
    aggregated_content = " ".join([doc.page_content for doc in docs])

    return aggregated_content


# message=[{"role": "user", "content": "As an intelligent AI model, if you could be any fictional character, who would you choose and why?"}]

# response = client.chat.completions.create(model="gpt-4-1106-preview",
# max_tokens=100,
# temperature=1.2,
# messages = message)

# Print the response from GPT-4
# print(response)


client = OpenAI()

file = client.files.create(
  file=open("retrieval_results.txt", "rb"),
  purpose='assistants'
)
    
# Create the Assistant with the new function
assistant = client.beta.assistants.create(
    instructions="You are an advanced bot. Use the provided functions to answer questions and search the database.",
    model="gpt-4-1106-preview",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "searchFile",
                "description": "Search the logfile for specific occurrences",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The query to search in the database"},
                    },
                    "required": ["query"]
                }
            }
        }
    ]
)

thread = client.beta.threads.create()


# message = client.beta.threads.messages.create(
#     thread_id=thread.id,
#     role="user",
#     content=question
# )

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Admin. The user needs an interpretation of the log file based on the question he asks. Be precise and remember all your context"
)

run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)

# Function to check the Run status
def check_run_status(client, thread_id, run_id):
    while True:
        # Retrieve the Run
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )

        # Check if the Run status is 'completed'
        if run.status == 'completed':
            print("Run is completed.")
            break
        else:
            print("Run is still in progress. Waiting for completion...")
            time.sleep(1)  # Wait for 5 seconds before checking again

# Function to display the Assistant's response
def display_assistant_response(client, thread_id):
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    for message in messages.data:
        print(message.content)

# Check the Run status
check_run_status(client, thread.id, run.id)

# Display the Assistant's response
display_assistant_response(client, thread.id)