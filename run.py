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
import json

client = OpenAI()

def searchDatabase(query):
    print("database query", query)

    persist_directory = 'db'
    embedding = OpenAIEmbeddings()
    # question = "what error were there in ssh?"
    question = "are there any anomalies in terms of systemd?"

    vectordb = Chroma(persist_directory=persist_directory,
                    embedding_function=embedding)

    retriever = vectordb.as_retriever(search_kwargs={"k": 15})
    docs = retriever.get_relevant_documents(question)
    print(docs) 

    print("\n\n\n\n\n\n\n\n")


    # Write the result to a file
    with open('retrieval_results.txt', 'w') as file:
        for doc in docs:
            file.write(str(doc) + '\n')

    # Assume docs is the list of documents retrieved from Chroma
    aggregated_content = " ".join([doc.page_content for doc in docs])

    print(aggregated_content)

    print("\n\n\n\n\n\n\n\n")

    return aggregated_content


# message=[{"role": "user", "content": "As an intelligent AI model, if you could be any fictional character, who would you choose and why?"}]

# response = client.chat.completions.create(model="gpt-4-1106-preview",
# max_tokens=100,
# temperature=1.2,
# messages = message)

# Print the response from GPT-4
# print(response)

def chat_iteration(user_input, previous_messages):
    # Add the user's message to the conversation history
    previous_messages.append({"role": "user", "content": user_input})

    # Add a system message (if needed) before making the API call
    system_message = "The user needs an interpretation of the log file based on the question he asks. Be precise and remember all your context"  # Customize this message as needed
    previous_messages.append({"role": "system", "content": system_message})

    
    # Define the tools and assistant model
    tools = [
        {
            "type": "function",
            "function": {
                "name": "searchFile",
                "description": "Search the logfile for specific occurrences",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "What to search for in complete sentence, e.g. Search for Malicious occurences in the file."},
                    },
                    "required": ["query"]
                }
            }
        }
    ]
    
    # Get the response from the assistant
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=previous_messages,
        tools=tools,
        tool_choice="auto",
    )

    # Process the response and tool calls
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            if function_name == "searchFile":
                # Extract arguments and call the appropriate function
                function_args = json.loads(tool_call.function.arguments)
                function_response = searchDatabase(query=function_args["query"])


                # Add function response as a system message for the next model call
                previous_messages.append({
                    "role": "assistant",
                    "content": function_response
                })

                # Add a system message for additional context or guidance
                previous_messages.append({
                    "role": "system", 
                    "content": 'The previous logs is the result of a verctordb search of the entire logfile. When responding to the user talk about you have searched the entire log-file.'
                })

        # Get a new response from the model incorporating the function response
        second_response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=previous_messages,
        )

        # Print the model's response interpreting the function output
        print(second_response.choices[0].message.content)
    else:
        print(response_message.content)

    return previous_messages


# Main chat loop with conversation history
def main_chat_loop():
    print("Welcome to Dora the Log Explorer. Type 'exit' to end the session.")
    conversation_history = []
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        conversation_history = chat_iteration(user_input, conversation_history)

# Run the main chat loop
main_chat_loop()
