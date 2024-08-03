import json
import pandas as pd
import requests

import os
from dotenv import load_dotenv

load_dotenv()

ODDS_API = os.getenv('odds_api')

up_sports = 'https://api.the-odds-api.com/v4/sports/upcoming/odds/?regions=eu&markets=h2h&apiKey={ODDS_API}'



# resp_sp  = requests.get(up_sports)
# sports_resp = resp_sp.json()

# for x in sports_resp:
#     print(x)

def get_key(up_sports):

    resp_sp  = requests.get(up_sports)
    
    sports_resp = resp_sp.json()

    with open('sports_keys.json', 'w') as f:
        json.dump(sports_resp, f)


if __name__ == '__main__':
    get_key(up_sports)

