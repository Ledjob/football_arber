import json
import re
from typing import List, Dict, Union
import pandas as pd
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.DEBUG)

@dataclass
class BettingOdds:
    id: str
    bookie: str
    home_name: str
    home_odd: float
    draw: str
    draw_odd: float
    away_name: str
    away_odd: float

def load_json_file(filename: str) -> Union[Dict, List]:
    with open(filename, 'r') as file:
        return json.load(file)

def get_soccer_paths(sport_list: List[Dict]) -> List[str]:
    return [x['key'] for x in sport_list if x['key'].startswith('soccer_')]

def calculate_profit_percentage(bet: float, calc: float) -> float:
    arb_profit = (bet / calc) - bet
    return ((bet + arb_profit) - bet) / bet * 100

def process_league_data(league: str) -> List[BettingOdds]:
    try:
        data = load_json_file(f'{league}.json')
        logging.debug(f"Loaded data for {league}: {type(data)}")
        if isinstance(data, list):
            logging.debug(f"First item in data: {type(data[0])}")
            if data and isinstance(data[0], str):
                logging.warning(f"Data for {league} contains strings, not objects. Skipping this league.")
                return []
        
        odds_list = []
        for match in data:
            logging.debug(f"Processing match: {type(match)}")
            if isinstance(match, dict) and 'bookmakers' in match:
                for bookmaker in match['bookmakers']:
                    if 'markets' in bookmaker and bookmaker['markets']:
                        outcomes = bookmaker['markets'][0]['outcomes']
                        if len(outcomes) >= 3:
                            odds_list.append(BettingOdds(
                                id=match['id'],
                                bookie=bookmaker['key'],
                                home_name=outcomes[0]['name'],
                                home_odd=outcomes[0]['price'],
                                draw=outcomes[2]['name'],
                                draw_odd=outcomes[2]['price'],
                                away_name=outcomes[1]['name'],
                                away_odd=outcomes[1]['price']
                            ))
                    else:
                        logging.warning(f"Bookmaker {bookmaker['key']} has no markets or outcomes")
            else:
                logging.warning(f"Unexpected match structure: {match}")
        return odds_list
    except FileNotFoundError:
        logging.error(f"File not found: {league}.json")
        return []
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in file: {league}.json")
        return []
    except Exception as e:
        logging.error(f"Unexpected error processing {league}.json: {str(e)}")
        return []

def analyze_arbitrage_opportunities(df: pd.DataFrame) -> None:
    for _, group in df.groupby('id'):
        max_odds = group.max()
        calc = sum(1 / max_odds[['home_odd', 'draw_odd', 'away_odd']])
        
        if calc < 0.99:
            profit_percentage = calculate_profit_percentage(100, calc)
            print(f"{max_odds.home_name} vs {max_odds.away_name}")
            print(f"Arbitrage opportunity: {calc:.4f}")
            print(f"Home: {max_odds.home_odd:.2f}, Draw: {max_odds.draw_odd:.2f}, Away: {max_odds.away_odd:.2f}")
            print(f"Potential profit: {profit_percentage:.2f}% (without fees)")
            print_best_odds(group)
            print()

def print_best_odds(group: pd.DataFrame) -> None:
    for outcome in ['home', 'draw', 'away']:
        best = group.loc[group[f'{outcome}_odd'] == group[f'{outcome}_odd'].max()].iloc[0]
        print(f"Best {outcome.capitalize()} odds: {best[f'{outcome}_odd']:.2f} ({best['bookie']})")

def main():
    sport_list = load_json_file('sports_title.json')
    soccer_paths = get_soccer_paths(sport_list)

    all_odds = []
    for league in soccer_paths:
        league_odds = process_league_data(league)
        all_odds.extend(league_odds)
        logging.info(f"Processed {league}: {len(league_odds)} odds entries")

    if not all_odds:
        print("No valid data found. Please check your input files and log for details.")
        return

    df = pd.DataFrame(all_odds)
    analyze_arbitrage_opportunities(df)

if __name__ == "__main__":
    main()