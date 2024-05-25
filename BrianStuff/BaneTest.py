import requests
import openai
from dotenv import load_dotenv # This is where I want to keep my API key secret
import os

def configure(): # In charge of getting .env from my environment, this contains my API key
    load_dotenv()


def openai_test():
    configure()
    OPENAI_API_KEY = os.getenv('api_key') # Grabs the API key and puts it into the variable OPENAI_API_KEY (Has to be named this)
    openai.api_key = OPENAI_API_KEY # Feed it into openai

    if not OPENAI_API_KEY:
        raise ValueError("API Key not found. Please set the 'api_key' environment variable in your .env file.")
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY) # Create a client, passing in the API key

    prompts = [] # Initial creation of prompt lists. For some reason openai does not take multiple request so we must use a for loop at the bottom

    subject = input("Please provide a subject!\n")
    prompt = f"Please give me some videos links to help study {subject}" # Creates a prompt. Might need to make a better one in the future
    learner = input("What kind of learner are you?\n")
    prompt2 = f"What study tips do you have if I am a {learner} learner?"
    prompts.append(prompt)
    prompts.append(prompt2)

    responses = []

    for specific_prompt in prompts: # Loop through all the prompts we have in order to get multiple responses.
        string = ""
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": specific_prompt}],
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                string += chunk.choices[0].delta.content
            else:
                responses.append(string.split("\n"))
                string = ""
    return responses


def create_post():
    configure()
    NOTION_TOKEN = os.getenv('NOTION_KEY')
    DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
    headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
    }

    description = input("Whats your name!\n")
    title = input("Write a message!\n")
    data = {
    "Name": {"title": [{"text": {"content": description}}]},
    "Message": {"rich_text": [{"text": {"content": title}}]}
    }

    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)

    return res



def main():
    #configure()
    responses = openai_test()
    for response in responses:
        for line in response:
            if line == "\n":
                continue
            print(line)

    create_post()
if __name__ == "__main__":
    main()
