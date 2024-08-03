import re
import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()

ODDS_API = os.getenv('odds_api')


# def save_files(div_odds):
#     with open(f'{league}.json', 'w') as f:
#         for league in soccer_path:
#             json.dump(div_odds, f)

# return a list of soccer leagues

sports = 'https://api.the-odds-api.com/v4/sports/?apiKey={ODDS_API}'

resp_sp  = requests.get(sports)
sports_resp = resp_sp.json()
# print(sports_resp)


# append sports to a list 
sport_path_list = []
for x in sports_resp:
  sport_path_list.append(x['key'])
#   print(x['key'], x['group'])

'''' print : 
            americanfootball_cfl American Football
            americanfootball_ncaaf American Football
            americanfootball_nfl American Football
            americanfootball_nfl_super_bowl_winner American Football
'''

soccer_path = []
expression = r'soccer_'

for string in sport_path_list:
   # If the string is data
    if (re.match(expression, string)):
        soccer_path.append(string)

#print(soccer_path)
#['soccer_argentina_primera_division', 'soccer_australia_aleague', 'soccer_belgium_first_div' ...]

for league in soccer_path:
    odds = f'https://api.the-odds-api.com/v4/sports/{league}/odds/?regions=eu&markets={ODDS_API}'
    resp = requests.get(odds)
    div_odds = resp.json()
    with open(f'{league}.json', 'w') as f:
            json.dump(div_odds, f)

