from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import requests
import googleapiclient.discovery
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

def generate_tips(learner): # Will return a list of tips
    configure()
    OPENAI_API_KEY = os.getenv('api_key') # Grabs the API key and puts it into the variable OPENAI_API_KEY (Has to be named this)
    openai.api_key = OPENAI_API_KEY # Feed it into openai

    if not OPENAI_API_KEY:
        raise ValueError("API Key not found. Please set the 'api_key' environment variable in your .env file.")
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY) # Create a client, passing in the API key
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

def generate_flashcards(subject): # Will return a string formatted in JSON
    configure()
    OPENAI_API_KEY = os.getenv('api_key') # Grabs the API key and puts it into the variable OPENAI_API_KEY (Has to be named this)
    openai.api_key = OPENAI_API_KEY # Feed it into openai

    if not OPENAI_API_KEY:
        raise ValueError("API Key not found. Please set the 'api_key' environment variable in your .env file.")
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY) # Create a client, passing in the API key

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
        maxResults=1,
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
#FLASK HANDLING


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/flashcards')
def flashcards():
    return render_template('flashcards.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')

@app.route('/music')
def music():
    return render_template('music.html')


@app.route('/todo')
def todo():
    return render_template('todo.html')


@app.route('/cafes', methods=['GET', 'POST'])    # HELEN NEEDS TO CREATE A CAFES SUBPAGE
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


# @app.route('/music.html', methods=['GET', 'POST'])    
# def music():
#     playlists = None
#     if request.method == 'POST':
#         if 'category' in request.form:
#             category = request.form['category']
#             playlists_json = fetch_playlists(category)
#             playlists = []
#             if 'items' in playlists_json:
#                 for item in playlists_json['items']:
#                     playlist_title = item['snippet']['title']
#                     playlist_id = item['id']['playlistId']
#                     playlist_url = f'https://www.youtube.com/playlist?list={playlist_id}'
#                     playlists.append({'title': playlist_title, 'url': playlist_url})

#     return render_template('music.html', playlists=playlists)


@app.route('/musicResults.html', methods=['GET', 'POST'])    
def musicResult():
    print(request)
    category = request.form['category']
    responses = openai_music_test(category)
    return render_template('musicResults.html', responses=responses)

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


app.secret_key = 'your_secret_key'
@app.route('/todo', methods=['GET', 'POST'])
def todotask():
    if 'tasks' not in session:
        session['tasks'] = []

    if request.method == 'POST':
        task_content = request.form['task']
        session['tasks'].append(task_content)

    return render_template('todo.html', tasks=session['tasks'])




if __name__ == '__main__':
    app.run(debug=True)
