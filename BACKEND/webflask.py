from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os
import openai


app = Flask(__name__)


YELP_API_KEY = 'hYkh7Y38ofnKkkZCLXNoSzo9btQj7eYM7v0hbAyQ0gWSPvm236SOY1RB9oaPg5x1OA8dozm2tICepSMNZpd4XLXUiXyu2HTUa8dOEOJdQ8C8wNeRd1e-cvh35mxRZnYx'
YELP_API_URL = 'https://api.yelp.com/v3/businesses/search'

YOUTUBE_API_KEY= 'AIzaSyCCQuFz2-6xXs_me9KVwCwicxb5WUQuwTA'
BASE_URL = 'https://www.googleapis.com/youtube/v3/search'


# PYTHON FUNCTIONS


def search_cafes_in_city(city):
    headers = {'Authorization': f'Bearer {YELP_API_KEY}'}
    params = {'term': 'cafe', 'location': city}
    response = requests.get(YELP_API_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        cafes = response.json()['businesses']
        return cafes  
    else:
        return None
    

def configure(): 
    load_dotenv()

def openai_music_test(category):
    OPENAI_API_KEY = os.getenv('api_key')
    if OPENAI_API_KEY is None:
        raise ValueError("API Key not found.")

    openai.api_key = OPENAI_API_KEY 

    if not OPENAI_API_KEY:
        raise ValueError("API Key not found. Please set the 'api_key' environment variable in your .env file.")
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY) 

    prompts = [] 

    prompt = f"Please give me some links from Youtube for music playlist to help study {category}" 
    prompts.append(prompt)

    responses = []

    for specific_prompt in prompts:
        string = ""
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": specific_prompt}],
            stream=True,
        )

        for chunk in stream:
            # print(chunk, 'df')
            if chunk.choices[0].delta.content is not None:
                string += chunk.choices[0].delta.content
            else:
                responses.append(string.split("\n"))
                print('LIKE ARE EWR EVEN HERE???')
                string = ""

    return responses    

def openai_test(subject, learner):
    OPENAI_API_KEY = os.getenv('api_key')
    if OPENAI_API_KEY is None:
        raise ValueError("API Key not found.")

    openai.api_key = OPENAI_API_KEY 

    if not OPENAI_API_KEY:
        raise ValueError("API Key not found. Please set the 'api_key' environment variable in your .env file.")
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY) 

    prompts = [] 

    prompt = f"Please give me some videos links to help study {subject}" 
    prompt2 = f"What study tips do you have if I am a {learner} learner?"
    prompts.append(prompt)
    prompts.append(prompt2)

    responses = []

    for specific_prompt in prompts:
        string = ""
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": specific_prompt}],
            stream=True,
        )

        for chunk in stream:
            # print(chunk, 'df')
            if chunk.choices[0].delta.content is not None:
                string += chunk.choices[0].delta.content
            else:
                responses.append(string.split("\n"))
                string = ""

    return responses




#FLASK HANDLING

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/flashcards')
def flashcards():
    return render_template('flashcards.html')

@app.route('/cafes.html', methods=['GET', 'POST'])    # HELEN NEEDS TO CREATE A CAFES SUBPAGE

def cafes():
    cafes = None
    if request.method == 'POST':
        city_name = request.form['city']
        cafes = search_cafes_in_city(city_name)
    return render_template('cafes.html', cafes=cafes)


@app.route('/music', methods=['GET', 'POST'])
def music():
    if request.method == 'POST':
        parts = []
        category = request.form['category']
        responses = openai_music_test(category)
        processed_responses = []
        for response_split in responses:
            print("response_split: ", response_split)
            for response in response_split:
                print("response: ", response)
                if " -" in response:
                    parts = response.split(" -")
                elif ":" in response:
                    parts = response.split(":")
                if len(parts) > 0:
                    print("parts: ", parts)
                    title = parts[0].strip().split(' ', 1)[1]  # remove the numbering
                    url = parts[1].strip()
                    processed_responses.append({'title': title, 'url': url})
                    print("results: ", processed_responses)
        return render_template('music.html', responses=processed_responses)
    return render_template('music.html')


@app.route('/video-submit', methods=['POST'])
def videos():
    number = 0
    subject = request.form['subject']
    learner = request.form['learner']
    
    responses = openai_test(subject, learner)
    processed_responses = []

    for response_split in responses:
        for response in response_split:
            print("response: ", response)
            print("response splited: ", response.split(" h"))
            if "http" in response:  # only process strings containing URLs
                parts = response.split('tutorial: ', 1)
                if len(parts) == 2:
                    title = parts[0].strip().split(' ', 1)[1]  # remove the numbering
                    url = parts[1].strip()
                    processed_responses.append({'title': title, 'url': url})
                    print("results: ", processed_responses)
    return render_template('videos.html', responses=processed_responses)


if __name__ == '__main__':
    app.run(debug=True)
