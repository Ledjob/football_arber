from bs4 import BeautifulSoup
import requests

competition_urls = {
		'football':
		{
			"ligue1": "https://www.betclic.fr/football-s1/ligue-1-mcdonald-s-c4",
			"liga": "https://www.betclic.fr/football-s1/espagne-liga-primera-c7",
			"bundesliga": "https://www.betclic.fr/football-s1/allemagne-bundesliga-c5",
			"premier-league": "https://www.betclic.fr/football-s1/angl-premier-league-c3",
			"serie-a": "https://www.betclic.fr/football-s1/italie-serie-a-c6",
			"primeira": "https://www.betclic.fr/football-s1/portugal-primeira-liga-c32",
			"serie-a-brasil": "https://www.betclic.fr/football-s1/bresil-serie-a-c187",
			"a-league": "https://www.betclic.fr/football-s1/australie-a-league-c1874",
			"bundesliga-austria": "https://www.betclic.fr/football-s1/autriche-bundesliga-c35",
			"division-1a": "https://www.betclic.fr/football-s1/belgique-division-1a-c26",
			"super-lig": "https://www.betclic.fr/football-s1/turquie-super-lig-c37",
		},
		'basketball':
		{
			"nba": "https://www.betclic.fr/basket-ball-s4/nba-c13",
			"euroleague": "https://www.betclic.fr/basket-ball-s4/euroligue-c14",
		}
}

def get_page(competition):
    if competition["sport"] in competition_urls and competition["competition"] in competition_urls[competition["sport"]]:
        url = competition_urls[competition["sport"]][competition["competition"]]
    else:
        return None
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})
    html = BeautifulSoup(response.content, 'html.parser')
    return html

def get_games(competition):
    html = get_page(competition)
    games = []
    
    # Select all the game elements
    game_elements = html.select(".btnWrapper.is-inline")
    
    for el in game_elements:
        # Select team names and odds
        team_names = el.select(".btn_label.is-top span")
        odds = el.select(".btn_label")
        
        if len(team_names) == 3 and len(odds) == 6:
            team1 = team_names[0].text.strip()
            team2 = team_names[2].text.strip()
            odd1 = float(odds[1].text.replace(",", ".").strip())
            odd2 = float(odds[3].text.replace(",", ".").strip())
            odd3 = float(odds[5].text.replace(",", ".").strip())
            
            games.append({
                'team1': team1,
                'team2': team2,
                'odds': [odd1, odd2, odd3]
            })
    
    return games

# Example usage:
competition = {
    "sport": "football",
    "competition": "ligue1"
}
print(get_games(competition))