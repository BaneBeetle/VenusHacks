import openai
OPENAI_API_KEY = "sk-proj-WfzaTUpb5ZNF5VUHoITVT3BlbkFJoktbge9m0nEcx87zr250"
openai.api_key = OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

subject = input("Please provide a subject!\n")
prompt = f"Please provide video links for {subject}"
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")

