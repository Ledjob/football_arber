from bs4 import BeautifulSoup
import requests
from datetime import datetime
import os

from utils.update_leagues import update_league_json
from utils.league_info import league_info

print("Zebet module loaded")



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
		"a-league": "https://www.zebet.fr/paris-football/australie/d1-australie",
		"bundesliga-austria": "https://www.zebet.fr/paris-football/autriche/d1-autriche",
		"division-1a": "https://www.zebet.fr/paris-football/belgique/d1-belgique",
		"super-lig": "https://www.zebet.fr/paris-football/turquie/d1-turquie",
        "primera-division": "https://www.zebet.fr/paris-football/argentine/d1-argentine",
        "primera-division-chile":"https://www.zebet.fr/paris-football/chili/d1-chili",
        "soccer-france-ligue-two":"https://www.zebet.fr/paris-football/france/ligue-2-bkt",
        "soccer-japan-j-league":"https://www.zebet.fr/paris-football/japon/d1-japon"
	}
	# 'basketball':
	# {
	# 	"nba": "https://www.zebet.fr/fr/competition/206-nba",
	# 	"euroleague": "https://www.zebet.fr/fr/competition/12044-euroligue",
	# }
}

# Absolute paths for JSON files
base_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))



# #add turkish and australia
# league_info = {
#     'football': {
#         'ligue1': {'sport_key': 'soccer_france_ligue_one', 'sport_title': 'Ligue 1 - France', 'file': './soccer_france_ligue_one.json'},
        
#         'liga': {'sport_key': 'soccer_spain_la_liga', 'sport_title': 'La Liga - Spain', 'file': './soccer_spain_la_liga.json'},
        
#         'bundesliga': {'sport_key': 'soccer_germany_bundesliga', 'sport_title': 'Bundesliga - Germany', 'file': './soccer_germany_bundesliga.json'},
        
#         'premier-league': {'sport_key': 'soccer_england_league1', 'sport_title': 'Premier-league - England', 'file': './soccer_england_league1.json'},
        
# 		'serie-a': {'sport_key': 'soccer_italy_serie_a', 'sport_title': 'Serie-a - Italia', 'file': './soccer_italy_serie_a.json'},
          
# 		'primeira': {'sport_key': 'soccer_portugal_primeira_liga', 'sport_title': 'Primeira - Portugal', 'file': './soccer_portugal_primeira_liga.json'},
          
# 		'serie-a-brasil': {'sport_key': 'soccer_brazil_campeonato', 'sport_title': 'Campeonato - Brazil', 'file': './soccer_brazil_campeonato.json'},
        
# 		'bundesliga-austria': {'sport_key': 'soccer_austria_bundesliga', 'sport_title': 'bundesliga - Austria', 'file': './soccer_austria_bundesliga.json'},
          
# 		'division-1a': {'sport_key': 'soccer_belgium_first_div', 'sport_title': 'Jupiler Pro League - Belgium', 'file': './soccer_belgium_first_div.json'},

#         'primera-division': {'sport_key': 'soccer_argentina_primera_division', 'sport_title': 'Primera División - Argentina', 'file': './soccer_argentina_primera_division.json'},

#         'primera-division-chile': {'sport_key': 'soccer_chile_campeonato', 'sport_title': 'Primera División - Chile', 'file': './soccer_chile_campeonato.json'},

#         'soccer-france-ligue-two': {'sport_key': 'soccer_france_ligue_two', 'sport_title': 'Ligue 2 - France', 'file': './soccer_france_ligue_two.json'},

#         'soccer-japan-j-league': {'sport_key': 'soccer_japan_j_league', 'sport_title': 'J League', 'file': './soccer_japan_j_league.json'},

#         'super-lig': {'sport_key': 'soccer_turkey_super_league', 'sport_title': 'Turkey Super League', 'file': './soccer_turkey_super_league.json'},
          
		
#     },
#     # 'basketball': { ... }
# }

def get_page(competition):
	if (competition["sport"] in competition_urls and competition["competition"] in competition_urls[competition["sport"]]):
		url = competition_urls[competition["sport"]][competition["competition"]]
	else:
		return None
	response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})
	html = BeautifulSoup(response.content, 'html.parser')
	return html

def get_id(competition):
    url = competition_urls[competition["sport"]][competition["competition"]]
    return int(url.split("/")[-1])

def get_games(competition):
    print(f"Getting games for {competition['sport']} - {competition['competition']}")
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
        odd2 = float(odds[1].text.replace(",", ".").strip()) #draw
        odd3 = float(odds[2].text.replace(",", ".").strip())

        now = datetime.now()

        if team1 < team2:
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
        else:
            games.append({
                "key": "Zebet",
                "title": "Zebet",
                "markets": [
                    {
                        "key": "h2h",
                        "last_update": str(now),
                        "outcomes": [
                            {
                                "name": team2,
                                "price": odd3
                            },
                            {
                                "name": team2,
                                "price": odd1
                            },
                            {
                                "name": "Draw",
                                "price": odd2
                            }
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