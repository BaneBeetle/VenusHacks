from flask import Flask, render_template, request
import requests
import pandas as pd


APIkey = 'hYkh7Y38ofnKkkZCLXNoSzo9btQj7eYM7v0hbAyQ0gWSPvm236SOY1RB9oaPg5x1OA8dozm2tICepSMNZpd4XLXUiXyu2HTUa8dOEOJdQ8C8wNeRd1e-cvh35mxRZnYx'
APIURL = 'https://api.yelp.com/v3/businesses/search'


app = Flask(__name__)



def search_cafes_in_city(city):
    headers = {'Authorization': f'Bearer {'hYkh7Y38ofnKkkZCLXNoSzo9btQj7eYM7v0hbAyQ0gWSPvm236SOY1RB9oaPg5x1OA8dozm2tICepSMNZpd4XLXUiXyu2HTUa8dOEOJdQ8C8wNeRd1e-cvh35mxRZnYx'}'}
    params = {'term': 'cafe', 'location': city}
    response = requests.get('https://api.yelp.com/v3/businesses/search', headers=headers, params=params)
    if response.status_code == 200:
        cafes = response.json()['businesses']
        return cafes
    else:
        return None

@app.route('/', methods=['GET', 'POST'])

def index():
    cafes = None
    if request.method == 'POST':
        city_name = request.form['city']
        cafes = search_cafes_in_city(city_name)
        
    return render_template('cafes.html', cafes=cafes)



if __name__ == '__main__':
    app.run(debug=True)

