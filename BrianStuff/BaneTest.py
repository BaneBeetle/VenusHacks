import openai
from dotenv import load_dotenv # This is where I want to keep my API key secret
import os

def configure(): # In charge of getting .env from my environment, this contains my API key
    load_dotenv()


def openai_test():
    #OPENAI_API_KEY = os.getenv('api_key') # Grabs the API key and puts it into the variable OPENAI_API_KEY (Has to be named this)
    OPENAI_API_KEY = "sk-proj-OockXV9SUEpoRiK0Yy84T3BlbkFJZTANvyHVWAybwKQ07VuL"
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

def main():
    configure()
    responses = openai_test()
    for response in responses:
        for line in response:
            print(line)


main()
