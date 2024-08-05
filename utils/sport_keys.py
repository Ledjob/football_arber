import json
import requests

import os
from dotenv import load_dotenv

load_dotenv()

ODDS_API = os.getenv('ODDS_API')

sports = f'https://api.the-odds-api.com/v4/sports/?apiKey={ODDS_API}'

'''run to get a json file of all sports'''
def get_sports(sports):

    resp_sp  = requests.get(sports)
    sports_resp = resp_sp.json()

    with open('sports_title.json', 'w') as f:
        json.dump(sports_resp, f)


if __name__ == '__main__':
    get_sports(sports)