from openai import OpenAI
import time
client = OpenAI()

file = client.files.create(
  file=open("data/test_log1.txt", "rb"),
  purpose='assistants'
)
    
assistant = client.beta.assistants.create(
    name="Log Analyzer",
    instructions="You are an expert in analyzing linux log files. Summarize the content of a log file based on the specific questions asked. Be precise.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview",
    file_ids=[file.id]
)

thread = client.beta.threads.create()


message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="i need you to analyze this log file for me. please look for errors."
)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Dora-Abuser. The user needs an interpretation of the log file."
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