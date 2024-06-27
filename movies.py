# movies.py
import requests
import json
from bs4 import BeautifulSoup
import random

def get_top_250_movies():
    url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    movies = []

    for item in soup.select('td.titleColumn'):
        title = item.a.text
        link = "https://www.imdb.com" + item.a['href']
        movies.append((title, link))

    return movies

def fetch_movies():
    url = 'https://caching.graphql.imdb.com/?operationName=Top250MoviesPagination&variables=%7B%22first%22%3A125%2C%22locale%22%3A%22es-ES%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22sha256Hash%22%3A%2226114ee01d97e04f65d6c8c7212ae8b7888fa57ceed105450d1fce09df749b2d%22%2C%22version%22%3A1%7D%7D'
    headers = {
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'content-type': 'application/json',
        'accept': 'application/graphql+json, application/json',
        'x-imdb-client-name': 'imdb-web-next-localized',
        'x-imdb-user-country': 'ES',
        'Referer': 'https://www.imdb.com/',
        'x-imdb-user-language': 'es-ES',
        'sec-ch-ua-platform': '"macOS"'
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    return [movie.get("node").get("id") for movie in data['data']['chartTitles']['edges']]

def get_random_movie():
    movies = fetch_movies()
    # print(f"las pelicuas son: {movies}")
    return random.choice(movies)


def get_movie_details():
    movie_id = get_random_movie()
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    response = requests.get(f'https://www.imdb.com/title/{movie_id}/', headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    movie_data = json.loads(soup.find('script', type='application/ld+json',).string)

    title = movie_data.get("name")
    image = movie_data.get("image")
    link = movie_data.get("url")

    return title, link, image
