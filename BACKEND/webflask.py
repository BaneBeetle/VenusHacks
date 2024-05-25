from flask import Flask, render_template, request
import requests

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

    
    
def fetch_playlists(category, max_results=10):
    params = {
        'part': 'snippet',
        'q': category,
        'type': 'playlist',
        'maxResults': max_results,
        'key': YOUTUBE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    playlists = response.json()
    return playlists


def display_playlists(category):
    playlists = fetch_playlists(category)
    if 'items' in playlists:
        for item in playlists['items']:
            playlist_title = item['snippet']['title']
            playlist_id = item['id']['playlistId']
            playlist_url = f'https://www.youtube.com/playlist?list={playlist_id}'
            print(f'{playlist_title}: {playlist_url}\n')
    else:
        print("No playlists found.")


#FLASK HANDLING

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/flashcards')
def flashcards():
    return render_template('flashcards.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')


@app.route('/cafes.html', methods=['GET', 'POST'])    # HELEN NEEDS TO CREATE A CAFES SUBPAGE

def cafes():
    cafes = None
    if request.method == 'POST':
        city_name = request.form['city']
        cafes = search_cafes_in_city(city_name)
    return render_template('cafes.html', cafes=cafes)



@app.route('/music.html', methods=['GET', 'POST'])     # WORKS BUT THERES 2 MUSIC.CSS AND MUSIC.HTML FILES?

def music():
    playlists = None
    if request.method == 'POST':
        if 'category' in request.form:
            category = request.form['category']
            playlists_json = fetch_playlists(category)
            playlists = []
            if 'items' in playlists_json:
                for item in playlists_json['items']:
                    playlist_title = item['snippet']['title']
                    playlist_id = item['id']['playlistId']
                    playlist_url = f'https://www.youtube.com/playlist?list={playlist_id}'
                    playlists.append({'title': playlist_title, 'url': playlist_url})

    return render_template('music.html', playlists=playlists)


if __name__ == '__main__':
    app.run(debug=True)