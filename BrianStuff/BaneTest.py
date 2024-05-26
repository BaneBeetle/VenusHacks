import requests
import openai
from dotenv import load_dotenv # This is where I want to keep my API key secret
import os

def configure(): # In charge of getting .env from my environment, this contains my API key
    load_dotenv()


def generate_flashcards(): # Will return a string formatted in JSON
    configure()
    OPENAI_API_KEY = os.getenv('api_key') # Grabs the API key and puts it into the variable OPENAI_API_KEY (Has to be named this)
    openai.api_key = OPENAI_API_KEY # Feed it into openai

    if not OPENAI_API_KEY:
        raise ValueError("API Key not found. Please set the 'api_key' environment variable in your .env file.")
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY) # Create a client, passing in the API key

    subject = input("Please provide a subject!\n")
    prompt = f"Generate 5 questions and answers on the subject {subject} as a JSON object with the keys Question, Answer."

    string = ""
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            string += chunk.choices[0].delta.content
        else:
            return string
    return string

def generate_tips(): # Will return a list of tips
    configure()
    OPENAI_API_KEY = os.getenv('api_key') # Grabs the API key and puts it into the variable OPENAI_API_KEY (Has to be named this)
    openai.api_key = OPENAI_API_KEY # Feed it into openai

    if not OPENAI_API_KEY:
        raise ValueError("API Key not found. Please set the 'api_key' environment variable in your .env file.")
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY) # Create a client, passing in the API key

    learner = input("What kind of learner are you?\n")
    learn_prompt = f"Provide 5 study tips if I am a {learner} learner?"

    responses = []
    string = ""
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": learn_prompt}],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            string += chunk.choices[0].delta.content
        else:
            responses = string.split("\n")
            string = ""
    return responses

def main():
    response = generate_flashcards()
    print(response)

    tips = generate_tips()
    print(tips)

if __name__ == "__main__":
    main()
