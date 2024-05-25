import openai
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()


def openai_test():
    OPENAI_API_KEY = os.getenv('api_key')
    openai.api_key = OPENAI_API_KEY

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    subject = input("Please provide a subject!\n")
    prompt = f"Please give me some videos links to help study {subject}"
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")


def main():
    configure()
    openai_test()


main()
