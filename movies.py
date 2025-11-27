# movies.py
from wsgiref import headers
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
        'accept': 'application/graphql+json, application/json',
        'accept-language': 'es-419,es;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://www.imdb.com',
        'priority': 'u=1, i',
        'referer': 'https://www.imdb.com/',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'x-amzn-sessionid': '145-0330121-3935347',
        'x-imdb-client-name': 'imdb-web-next-localized',
        'x-imdb-client-rid': '0ZF8JJ0Q4CFRXNV5WEBK',
        'x-imdb-consent-info': 'eyJhZ2VTaWduYWwiOiJBRFVMVCIsImlzR2RwciI6ZmFsc2V9',
        'x-imdb-user-country': 'MX',
        'x-imdb-user-language': 'es-MX',
        'x-imdb-weblab-treatment-overrides': '{"IMDB_NAV_PRO_FLY_OUT_1321244":"T2","SEARCH_CONSUMER_CLUSTER_CLIENT_MIGRATION_1272244":"T2"}',
        # 'cookie': 'session-id=145-0330121-3935347; session-id-time=2082787201l; ubid-main=133-0325105-1593837; international-seo=es; ad-oo=0; ci=eyJhZ2VTaWduYWwiOiJBRFVMVCIsImlzR2RwciI6ZmFsc2V9; session-token=XY1xP7yXjR2jsddilVeODYLq9rTK5DeStEPhgo5kg0Rh4vOJkuAityGIN9x97u9an7uUZAGPp9UOTmzON9LtrVGKC9qEcmbEwrL+Y4ceMm7TX5zfI5qqZD1VbYPtQP4i0OvCtFBM5V2bWN8DE+FUHcMDgcVC5D5cSG9qhEsEtOqR1Bp5Jw0tfy9op/xatxfrHpgwc84fHBN5yUbdEnBrlQdUMcfMvAbijdREhuhckTAdtw+c8m1trDYLg4NXzL2mLEU8pIhCia2vt0R+zu8VFOehTaI5Yor1wF1p3eJIiA5Dlamr5tNg7djrLrY0hbnWI6wGTJr/xNE04ps8BZIAQnwLJZJZo5YW',
    }

    params = {
        'operationName': 'Top250MoviesPagination',
        'variables': '{"first":125,"isInPace":true,"locale":"es-MX"}',
        'extensions': '{"persistedQuery":{"sha256Hash":"319aff999f4470d7f3fd777c449397c089fd2d8f1c71a05ebf99a81128833e9e","version":1}}',
    }

    response = requests.get('https://caching.graphql.imdb.com/', params=params, headers=headers)
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
