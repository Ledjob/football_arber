import requests
import json
from datetime import datetime
from difflib import SequenceMatcher
import sys
import os


# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from update_leagues import update_league_json

print("Wina module loaded")

competition_urls = {
	'football':
	{
		"ligue1": "https://www.winamax.fr/paris-sportifs/sports/1/7/4",
		"liga": "https://www.winamax.fr/paris-sportifs/sports/1/32/36",
		"bundesliga": "https://www.winamax.fr/paris-sportifs/sports/1/30/42",
		"premier-league": "https://www.winamax.fr/paris-sportifs/sports/1/1/1",
		"serie-a": "https://www.winamax.fr/paris-sportifs/sports/1/31/33",
		"primeira": "https://www.winamax.fr/paris-sportifs/sports/1/44/52",
		"serie-a-brasil": "https://www.winamax.fr/paris-sportifs/sports/1/13/83",
		"a-league": "https://www.winamax.fr/paris-sportifs/sports/1/34/144",
		"bundesliga-austria": "https://www.winamax.fr/paris-sportifs/sports/1/17/29",
		"division-1a": "https://www.winamax.fr/paris-sportifs/sports/1/33/38",
		"super-lig": "https://www.winamax.fr/paris-sportifs/sports/1/46/62",
	}
	# 'basketball':
	# {
	# 	"nba": "https://www.winamax.fr/paris-sportifs/sports/2/800000076/177",
	# 	"euroleague": "https://www.winamax.fr/paris-sportifs/sports/2/800000034/153",
	# }
}

# Absolute paths for JSON files
base_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))

#add turkish and australia
league_info = {
    'football': {
        'ligue1': {'sport_key': 'soccer_france_ligue_one', 'sport_title': 'Ligue 1 - France', 'file': '../../soccer_france_ligue_one.json'},
        
        'liga': {'sport_key': 'soccer_spain_la_liga', 'sport_title': 'La Liga - Spain', 'file': '../../soccer_spain_la_liga.json'},
        
        'bundesliga': {'sport_key': 'soccer_germany_bundesliga', 'sport_title': 'Bundesliga - Germany', 'file': '../../soccer_germany_bundesliga.json'},
        
        'premier-league': {'sport_key': 'soccer_england_league1', 'sport_title': 'Premier-league - England', 'file': '../../soccer_england_league1.json'},
        
		'serie-a': {'sport_key': 'soccer_italy_serie_a', 'sport_title': 'Serie-a - Italia', 'file': '../../soccer_italy_serie_a.json'},
          
		'primeira': {'sport_key': 'soccer_portugal_primeira_liga', 'sport_title': 'Primeira - Portugal', 'file': '../../soccer_portugal_primeira_liga.json'},
          
		'serie-a-brasil': {'sport_key': 'soccer_brazil_campeonato', 'sport_title': 'Campeonato - Brazil', 'file': '../../soccer_brazil_campeonato.json'},
        
		'bundesliga-austria': {'sport_key': 'soccer_austria_bundesliga', 'sport_title': 'bundesliga - Austria', 'file': '../../soccer_austria_bundesliga.json'},
          
		'division-1a': {'sport_key': 'soccer_belgium_first_div', 'sport_title': 'Jupiler Pro League - Belgium', 'file': '../../soccer_belgium_first_div.json'},
          
		
    },
    # 'basketball': { ... }
}

def get_page(competition):
    if (competition["sport"] in competition_urls and competition["competition"] in competition_urls[competition["sport"]]):
        url = competition_urls[competition["sport"]][competition["competition"]]
    else:
        return None
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    return response.text

def get_json(competition):
    html = get_page(competition)
    split1 = html.split("var PRELOADED_STATE = ")[1]
    split2 = split1.split(";</script>")[0]
    return json.loads(split2)

def get_id(competition):
    url = competition_urls[competition["sport"]][competition["competition"]]
    return int(url.split("/")[-1])

def get_page(competition):
    if (competition["sport"] in competition_urls and competition["competition"] in competition_urls[competition["sport"]]):
        url = competition_urls[competition["sport"]][competition["competition"]]
    else:
        return None
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    return response.text

def get_json(competition):
    html = get_page(competition)
    split1 = html.split("var PRELOADED_STATE = ")[1]
    split2 = split1.split(";</script>")[0]
    return json.loads(split2)

def get_id(competition):
    url = competition_urls[competition["sport"]][competition["competition"]]
    return int(url.split("/")[-1])

def get_games(competition):
    print(f"Getting games for {competition['sport']} - {competition['competition']}")
    games = []
    json_data = get_json(competition)
    now = datetime.now()
    for game in json_data['matches']:
        if (json_data['matches'][game]['tournamentId'] != get_id(competition)):
            continue
        team1 = json_data['matches'][game]['competitor1Name']
        team2 = json_data['matches'][game]['competitor2Name']
        bet_id = json_data["matches"][game]['mainBetId']
        bet = json_data['bets'][str(bet_id)]['outcomes']
        if (competition["sport"] == "football" and len(bet) != 3):
            continue
        if (competition["competition"] == "basketball" and len(bet) != 2):
            continue
        if (competition["sport"] == "football"):
            odds = [
                json_data['odds'][str(bet[0])],
                json_data['odds'][str(bet[1])],
                json_data['odds'][str(bet[2])],
            ]
        elif (competition["sport"] == "basketball"):
            odds = [
                json_data['odds'][str(bet[0])],
                json_data['odds'][str(bet[1])],
            ]
        games.append({
            "key": "Winamax",
            "title": "Winamax",
            "markets": [
                {
                    "key": "h2h",
                    "last_update": str(now),
                    "outcomes": [
                        {
                            "name": team1,
                            "price": odds[0]
                        },
                        {
                            "name": team2,
                            "price": odds[2] if competition["sport"] == "football" else odds[1]
                        },
                        {
                            "name": "Draw",
                            "price": odds[1]
                        } if competition["sport"] == "football" else None
                    ]
                }
            ]
        })

    print(f"Retrieved {len(games)} games")
    
    update_results = None

    # Debugging print statements
    print("Checking league_info for sport and competition:")
    print(f"Sport: {competition['sport']}, Competition: {competition['competition']}")

    if competition['sport'] in league_info:
        print(f"Sport {competition['sport']} found in league_info")
        if competition['competition'] in league_info[competition['sport']]:
            print(f"Competition {competition['competition']} found in league_info[{competition['sport']}]")
            league = league_info[competition['sport']][competition['competition']]
            print(f"Updating league JSON for {league['sport_title']} with file {league['file']}")
            update_results = update_league_json(games, league, league['file'])
        else:
            print(f"Competition {competition['competition']} NOT found in league_info[{competition['sport']}]")
    else:
        print(f"Sport {competition['sport']} NOT found in league_info")

    return games, update_results

# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()

# def update_ligue1_json(games, json_file='../../soccer_france_ligue_one.json'):
#     # Load the Ligue 1 JSON
#     json_path = os.path.join(os.path.dirname(__file__), json_file)
#     with open(json_path, 'r') as f:
#         ligue1_data = json.load(f)

#     for game in games:
#         # Extract team names from the outcomes
#         team1 = game['markets'][0]['outcomes'][0]['name']
#         team2 = game['markets'][0]['outcomes'][1]['name']

#         # Find matching game or create new entry
#         match_found = False
#         for ligue1_game in ligue1_data:
#             if (similar(ligue1_game['home_team'], team1) > 0.7 and similar(ligue1_game['away_team'], team2) > 0.7) or \
#                (similar(ligue1_game['home_team'], team2) > 0.7 and similar(ligue1_game['away_team'], team1) > 0.7):
#                 # Match found, update or append bookmaker
#                 bookmaker_found = False
#                 for bookmaker in ligue1_game['bookmakers']:
#                     if bookmaker['key'] == 'Winamax':
#                         # Update existing Winamax entry
#                         bookmaker.update(game)
#                         bookmaker_found = True
#                         break
#                 if not bookmaker_found:
#                     # Append new Winamax entry
#                     ligue1_game['bookmakers'].append(game)
#                 match_found = True
#                 break

#         if not match_found:
#             # No match found, create new entry
#             new_entry = {
#                 "id": f"{team1.lower().replace(' ', '_')}_{team2.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}",
#                 "sport_key": "soccer_france_ligue_one",
#                 "sport_title": "Ligue 1 - France",
#                 "commence_time": datetime.now().isoformat(),
#                 "home_team": team1,
#                 "away_team": team2,
#                 "bookmakers": [game]
#             }
#             ligue1_data.append(new_entry)

#     # Write the updated data back to the file
#     with open(json_path, 'w') as f:
#         json.dump(ligue1_data, f, indent=2)