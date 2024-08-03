import requests
import json
from bs4 import BeautifulSoup

def get_page():
    url = "https://www.netbet.fr/football/france/ligue-1-mcdonald-stm"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})
    html = response.text
    return html

def extract_nuxt_data_bs4(html):
  """Extracts the content between `<script>window.__NUXT__=(function(a,b,c,d,e,...` and `</script>` from an HTML string using BeautifulSoup.

  Args:
    html: The HTML content as a string.

  Returns:
    The extracted content as a dictionary.
  """

  soup = BeautifulSoup(html, 'html.parser')
  script_tag = soup.find('script', string=lambda t: t and t.startswith('window.__NUXT__=(function('))
  if script_tag:

    # Extract the JSON data from the script tag
    json_data = script_tag.string.split("window.__NUXT__=")[1].split(";</script>")[0]
    

    # Parse the JSON data
    data = json.loads(json_data)
    
    # Save the HTML content to a file
    with open("netbet.html", "w", encoding="utf-8") as f:
        f.write(data)

    return data
  else:
    return None

# Using BeautifulSoup
data = extract_nuxt_data_bs4(get_page())
print(type(data))

# Extract the teams and odds for all matches
# matches = []
# for event in data["data"][0]["prematch_event_list"]["data"]["events"]:
#     team1 = event["choices"]["choices"][0]["actor"]["label"]
#     team2 = event["choices"]["choices"][2]["actor"]["label"]
#     odds = [choice["odd"] for choice in event["choices"]["choices"]]
#     match_data = {
#         "team1": team1,
#         "team2": team2,
#         "odds": odds
#     }
#     matches.append(match_data)

# # Print the data for all matches
# for match in matches:
#     print(match)
