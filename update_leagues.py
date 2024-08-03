import json
import os
from datetime import datetime
from difflib import SequenceMatcher
import logging

logging.basicConfig(level=logging.INFO)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def update_league_json(games, league_info, json_file):
    json_path = json_file  # Use the passed absolute path
    
    logging.info(f"Updating file: {json_path}")
    
    if not os.path.exists(json_path):
        logging.info(f"File does not exist. Creating new file: {json_path}")
        with open(json_path, 'w') as f:
            json.dump([], f)

    with open(json_path, 'r') as f:
        league_data = json.load(f)
    
    logging.info(f"Loaded {len(league_data)} existing games from {json_path}")
    
    games_updated = 0
    games_added = 0

    for game in games:
        team1 = game['markets'][0]['outcomes'][0]['name']
        team2 = game['markets'][0]['outcomes'][1]['name']

        match_found = False
        for league_game in league_data:
            if (similar(league_game['home_team'], team1) > 0.7 and similar(league_game['away_team'], team2) > 0.7) or \
               (similar(league_game['home_team'], team2) > 0.7 and similar(league_game['away_team'], team1) > 0.7):
                bookmaker_found = False
                for bookmaker in league_game['bookmakers']:
                    if bookmaker['key'] == game['key']:
                        bookmaker.update(game)
                        bookmaker_found = True
                        break
                if not bookmaker_found:
                    league_game['bookmakers'].append(game)
                match_found = True
                games_updated += 1
                break

        if not match_found:
            games_added += 1
            new_entry = {
                "id": f"{team1.lower().replace(' ', '_')}_{team2.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}",
                "sport_key": league_info['sport_key'],
                "sport_title": league_info['sport_title'],
                "commence_time": datetime.now().isoformat(),
                "home_team": team1,
                "away_team": team2,
                "bookmakers": [game]
            }
            league_data.append(new_entry)

    logging.info(f"Updated {games_updated} games and added {games_added} new games")

    with open(json_path, 'w') as f:
        json.dump(league_data, f, indent=2)
    
    logging.info(f"Saved updated data to {json_path}")

    return games_updated, games_added
