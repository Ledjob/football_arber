

import re
from bs4 import BeautifulSoup
import requests
import json

competition_urls = {
	'football': 
	{
		"ligue1": "https://www.netbet.fr/football/france/ligue-1-mcdonald-stm",
		"liga": "https://www.netbet.fr/football/espagne/laliga",
		"bundesliga": "https://www.netbet.fr/football/allemagne/bundesliga",
		"premier-league": "https://www.netbet.fr/football/angleterre/premier-league",
		"serie-a": "https://www.netbet.fr/football/italie/coupe-d-italie",
		"primeira": "https://www.netbet.fr/football/portugal/primeira-liga",
		"serie-a-brasil": "https://www.netbet.fr/football/bresil/brasileirao",
		"a-league": "https://www.netbet.fr/football/australie/a-league",
		"bundesliga-austria": "https://www.netbet.fr/football/autriche/bundesliga",
		"division-1a": "https://www.netbet.fr/football/belgique/pro-league",
		"super-lig": "https://www.netbet.fr/football/turquie/super-lig",
	},
	'basketball':
	{
		"nba": "https://www.netbet.fr/basketball/etats-unis/nba",
		"euroleague": "https://www.netbet.fr/basketball/coupes-d-europe/euroligue",
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

def extract_data_from_script(script_content):
    # Extract JSON-like data from script content
    data_pattern = re.compile(r'rematch_event_list:\{.*?events:\[(.*?)\]\}\}')
    match = data_pattern.search(script_content)
    
    if not match:
        return []
    
    events_data = match.group(1)
    
    # Clean up the string to make it JSON compatible
    events_data = events_data.replace("'", '"').replace(":", '":').replace(",", ',"').replace("{", '{"').replace("}", '"}').replace(',""', '","').replace('" "', '"')

    # Fix any other issues with the string format
    events_data = re.sub(r'(?<=[\[{,])(\w+)(?=[\]}:,])', r'"\1"', events_data)
    
    try:
        events_json = json.loads(f'[{events_data}]')
    except json.JSONDecodeError:
        return []

    games = []
    for event in events_json:
        teams = [actor['label'] for actor in event.get('actors', [])]
        if len(teams) < 2:
            continue
        
        odds = [choice['oddsDisplay'] for choice in event.get('choices', {}).get('choices', [])]
        if len(odds) < 3:
            continue
        
        games.append({
            'team1': teams[0],
            'team2': teams[1],
            'odds': [float(odds[0].replace(",", ".")), float(odds[1].replace(",", ".")), float(odds[2].replace(",", "."))]
        })
    
    return games

def get_games(competition):
    html = get_page(competition)
    scripts = html.find_all('script')
    
    for script in scripts:
        script_content = script.string
        if script_content and 'rematch_event_list' in script_content:
            games = extract_data_from_script(script_content)
            if games:
                return games
    
    return []

# Example usage:
competition = {
    "sport": "football",
    "competition": "ligue1"
}
print(get_games(competition))