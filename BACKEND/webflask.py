# WEBFLASK

import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import requests
from dotenv import load_dotenv
import os
import openai
import googleapiclient.discovery


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

def openai_test(subject):
    OPENAI_API_KEY = os.getenv('api_key')
    if OPENAI_API_KEY is None:
        raise ValueError("API Key not found.")

    openai.api_key = OPENAI_API_KEY 

    if not OPENAI_API_KEY:
        raise ValueError("API Key not found. Please set the 'api_key' environment variable in your .env file.")
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY) 

    prompts = [] 

    prompt = f"Please give me 5 videos links to help study {subject}" 
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




#FLASK HANDLING

@app.route('/')
def home():
    return render_template('homepage.html')

app.secret_key = 'rizzmaster'
@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if 'tasks' not in session:
        session['tasks'] = []

    if request.method == 'POST':
        task_content = request.form['task']
        session['tasks'].append(task_content)
        session.modified = True  # Mark the session as modified after appending a task

    return render_template('todo.html', tasks=session['tasks'])

@app.route('/cafes.html', methods=['GET', 'POST'])    # HELEN NEEDS TO CREATE A CAFES SUBPAGE

def cafes():
    cafes = None
    if request.method == 'POST':
        city_name = request.form['city']
        cafes = search_cafes_in_city(city_name)
    return render_template('cafes.html', cafes=cafes)


@app.route('/music', methods=['GET', 'POST'])
def music():
    if request.method == "POST":
        print(request)
        subject = request.form['category']
        youtube_videos = youtube_test(subject) 
        print("youtube: ", youtube_videos)
        return render_template('music.html', youtube_videos=youtube_videos)
    return render_template('music.html')



@app.route('/videos', methods=['GET', 'POST'])
def videos():
    if request.method == "POST":
        print(request)
        learner = request.form['learner']
        subject = request.form['subject']
        
        responses = generate_tips(learner, subject)
        youtube_videos = youtube_test(subject)
        print("youtube: ", youtube_videos)
        return render_template('videos.html', responses=responses, youtube_videos=youtube_videos)
    return render_template('videos.html')

def generate_tips(learner, subject): # Will return a list of tips
    configure()
    OPENAI_API_KEY = os.getenv('api_key') # Grabs the API key and puts it into the variable OPENAI_API_KEY (Has to be named this)
    openai.api_key = OPENAI_API_KEY # Feed it into openai

    if not OPENAI_API_KEY:
        raise ValueError("API Key not found. Please set the 'api_key' environment variable in your .env file.")

    client = openai.OpenAI(api_key=OPENAI_API_KEY) # Create a client, passing in the API key
    learn_prompt = f"What study tips do you have for {subject} if I am a {learner} learner?"

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

def generate_flashcards(subject, number): # Will return a string formatted in JSON
    configure()
    OPENAI_API_KEY = os.getenv('api_key') # Grabs the API key and puts it into the variable OPENAI_API_KEY (Has to be named this)
    openai.api_key = OPENAI_API_KEY # Feed it into openai

    if not OPENAI_API_KEY:
        raise ValueError("API Key not found. Please set the 'api_key' environment variable in your .env file.")

    client = openai.OpenAI(api_key=OPENAI_API_KEY) # Create a client, passing in the API key

    prompt = f"Generate {int(number)} questions and answers on the subject {subject} as a JSON object with the keys Question, Answer."

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

def youtube_test(subject):
    configure()
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv('YOUTUBE_KEY')

    return_list = []

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)
    request = youtube.search().list(
        part='snippet',
        q=subject,
        maxResults=5,
        order="relevance",
        type="video"
    )
    return_value = request.execute()
    
    for items in return_value['items']:
        #print(items['snippet']['title'])
        x = items['id']['videoId']
        link = f"https://www.youtube.com/watch?v={x}"
        #print(link)

        return_list.append([items['snippet']['title'], items['id']['videoId'], link, items['snippet']['thumbnails']['high']['url']])

    return return_list

@app.route('/flashcards', methods=['GET', 'POST'])
def flashcards():
    if request.method == 'POST':
        subject = request.form['category']
        learner = request.form['learner']
        
        flashcards_json = generate_flashcards(subject, learner)

        print("flashcards: ")
        print(flashcards_json)
        flashcards = parse_flashcards(flashcards_json)  # Parse JSON string to extract questions and answers
        return render_template('flashcards.html', flashcards=flashcards)
    return render_template('flashcards.html')

def parse_flashcards(flashcards_json):
    # Assuming flashcardsJson contains the JSON string
    flashcards_data = json.loads(flashcards_json)
    processed_responses = []
    # Now you can access the questions list
    questions = flashcards_data['questions']

    # Iterate over the questions list
    for question_obj in questions:
        question = question_obj['Question']
        answer = question_obj['Answer']
        processed_responses.append({'Question': question, 'Answer': answer})
    return processed_responses

if __name__ == '__main__':
    app.run(debug=True)
