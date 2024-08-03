import requests 
import json
from datetime import datetime
def get_page():
    url = "https://www.winamax.fr/paris-sportifs/sports/1/7/4"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})
    html = response.text
    return html

def get_json():
	html = get_page()
	split1 = html.split("var PRELOADED_STATE = ")[1]
	split2 = split1.split(";</script>")[0]
	return json.loads(split2)

def get_games():
    games = []
    json = get_json()
    now = datetime.now()
    for game in json['matches']:
        if (json['matches'][game]["sportId"] != 1 or json["matches"][game]['tournamentId'] != 4):
             continue
        team1 = json['matches'][game]['competitor1Name']
        team2 = json['matches'][game]['competitor2Name']
        bet_id = json["matches"][game]['mainBetId']
        
        bet = json['bets'][str(bet_id)]['outcomes']
        
        if (len(bet) != 3):
             continue
        odds = [
             json["odds"][str(bet[0])],
             json["odds"][str(bet[1])],
             json["odds"][str(bet[2])],
        ]
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
                "price": odds[0]
              },
              {
                "name": team2,
                "price": odds[2]
              },
              {
                "name": "Draw",
                "price": odds[1]
              }
            ]
          }
        ]
        })

        
    return games


def main():
    print(get_games())


if __name__ == "__main__":
    main()