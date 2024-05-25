
from flask import Flask, render_template, request
import requests

YOUTUBE_API_KEY= 'AIzaSyCCQuFz2-6xXs_me9KVwCwicxb5WUQuwTA'
BASE_URL = 'https://www.googleapis.com/youtube/v3/search'

app = Flask(__name__)

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

app = Flask(__name__, template_folder='templates')
@app.route('/', methods=['GET', 'POST'])
def index():
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
