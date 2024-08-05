
from bookmakers.winamax import wina
from bookmakers.zebet import zebet
import logging
from utils import config

print("Script started")

logging.basicConfig(level=logging.INFO)

competition_list = config.competitions

print(f"Processing {len(competition_list)} competitions")

for competition in competition_list:
    print(f"Processing {competition['sport']} - {competition['competition']}:")
    print("Winamax:")
    games, update_results = wina.get_games(competition)
    print(f"Retrieved {len(games)} games from Winamax")
    if update_results:
        print(f"Updated {update_results[0]} games and added {update_results[1]} new games")
    
    print("Zebet:")
    games, update_results = zebet.get_games(competition)
    print(f"Retrieved {len(games)} games from Zebet")
    if update_results:
        print(f"Updated {update_results[0]} games and added {update_results[1]} new games")
    
    print("\n")

print("Script finished")

