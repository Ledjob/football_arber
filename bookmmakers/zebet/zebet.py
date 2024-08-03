from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json
import os
from datetime import datetime
from difflib import SequenceMatcher

competition_urls = {
	'football':
	{
		"ligue1": "https://www.zebet.fr/paris-football/france/ligue-1-mcdonalds",
		"liga": "https://www.zebet.fr/fr/competition/306-laliga",
		"bundesliga": "https://www.zebet.fr/fr/competition/268-bundesliga",
		"premier-league": "https://www.zebet.fr/fr/competition/94-premier_league",
		"serie-a": "https://www.zebet.fr/fr/competition/305-serie_a",
		"primeira": "https://www.zebet.fr/fr/competition/154-primeira_liga",
		"serie-a-brasil": "https://www.zebet.fr/fr/competition/81-brasileirao",
		"a-league": "https://www.zebet.fr/fr/competition/2169-a_league",
		"bundesliga-austria": "https://www.zebet.fr/fr/competition/131-bundesliga",
		"division-1a": "https://www.zebet.fr/fr/competition/101-pro_league_1a",
		"super-lig": "https://www.zebet.fr/fr/competition/254-super_lig",
	},
	'basketball':
	{
		"nba": "https://www.zebet.fr/fr/competition/206-nba",
		"euroleague": "https://www.zebet.fr/fr/competition/12044-euroligue",
	}
}



def get_page(competition):
	if (competition["sport"] in competition_urls and competition["competition"] in competition_urls[competition["sport"]]):
		url = competition_urls[competition["sport"]][competition["competition"]]
	else:
		return None
	response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})
	html = BeautifulSoup(response.content, 'html.parser')
	return html

def get_games(competition):
    html = get_page(competition)
    games = []
    
    # Select all the event elements
    game_elements = html.select("psel-event-main.psel-event")
    
    for el in game_elements:
        # Select team names
        team_names = el.select(".psel-opponent__name")
        if len(team_names) < 2:
            continue
        
        team1 = team_names[0].text.strip()
        team2 = team_names[1].text.strip()
        
        # Select odds
        odds = el.select(".psel-outcome__data")
        if len(odds) < 3:
            continue
        
        odd1 = float(odds[0].text.replace(",", ".").strip())
        odd2 = float(odds[1].text.replace(",", ".").strip())
        odd3 = float(odds[2].text.replace(",", ".").strip())
        
        now = datetime.now()

        games.append({
              "key": "Zebet",
        "title": "Zebet",
        "markets": [
          {
            "key": "h2h",
            "last_update": str(now),
            "outcomes": [
              {
                "name": team1,
                "price": odd1
              },
              {
                "name": team2,
                "price": odd3
              },
              {
                "name": "Draw",
                "price": odd2
              }
            ]
          }
        ]
        })

        if competition['sport'] == 'football' and competition           ['competition'] == 'ligue1':
            update_ligue1_json(games)
    
    return games

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def update_ligue1_json(games, json_file='../soccer_france_ligue_one.json'):
    # Load the Ligue 1 JSON
    json_path = os.path.join(os.path.dirname(__file__), json_file)
    with open(json_path, 'r') as f:
        ligue1_data = json.load(f)

    for game in games:
        # Extract team names from the outcomes
        team1 = game['markets'][0]['outcomes'][0]['name']
        team2 = game['markets'][0]['outcomes'][1]['name']

        # Find matching game or create new entry
        match_found = False
        for ligue1_game in ligue1_data:
            if (similar(ligue1_game['home_team'], team1) > 0.8 and similar(ligue1_game['away_team'], team2) > 0.8) or \
               (similar(ligue1_game['home_team'], team2) > 0.8 and similar(ligue1_game['away_team'], team1) > 0.8):
                # Match found, update or append bookmaker
                bookmaker_found = False
                for bookmaker in ligue1_game['bookmakers']:
                    if bookmaker['key'] == 'Zebet':
                        # Update existing Zebet entry
                        bookmaker.update(game)
                        bookmaker_found = True
                        break
                if not bookmaker_found:
                    # Append new Zebet entry
                    ligue1_game['bookmakers'].append(game)
                match_found = True
                break

        if not match_found:
            # No match found, create new entry
            new_entry = {
                "id": f"{team1.lower().replace(' ', '_')}_{team2.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}",
                "sport_key": "soccer_france_ligue_one",
                "sport_title": "Ligue 1 - France",
                "commence_time": datetime.now().isoformat(),
                "home_team": team1,
                "away_team": team2,
                "bookmakers": [game]
            }
            ligue1_data.append(new_entry)

    # Write the updated data back to the file
    with open(json_path, 'w') as f:
        json.dump(ligue1_data, f, indent=2)

# Example usage:
competition = {
    "sport": "football",
    "competition": "ligue1"
}
print(get_games(competition))