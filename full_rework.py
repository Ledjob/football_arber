
import pandas as pd
import numpy as np



id_list = []
home_list = []
home_name = []
away_name = []
draw_name = []
draw_list = []
away_list = []
bookie_list = []

for x in div_odds: #change that
  # print(x['home_team'], x['away_team'], x['bookmakers'])
  for y in x['bookmakers']:
    id_list.append(x['id'])
    bookie_list.append(y['key'])
    home_name.append(y['markets'][0]['outcomes'][0]['name'])
    draw_name.append(y['markets'][0]['outcomes'][2]['name'])
    away_name.append(y['markets'][0]['outcomes'][1]['name'])
   
    home_list.append(y['markets'][0]['outcomes'][0]['price'])
    draw_list.append(y['markets'][0]['outcomes'][2]['price'])
    away_list.append(y['markets'][0]['outcomes'][1]['price'])
    # print(x['id'], y['markets'][0]['outcomes'])
    # 7d981aac76904af2160dac1dfb7e8d68 [{'name': 'Aston Villa', 'price': 2.09}, {'name': 'Southampton', 'price': 3.69}, {'name': 'Draw', 'price': 3.65}]


final_df1 = pd.DataFrame(list(zip(id_list, bookie_list, home_name, home_list, draw_name, draw_list, away_name, away_list)), columns=['id', 'bookie', 'home_name', 'home_odd', 'draw', 'draw_odd', 'away_name', 'away_odd'])
#print(final_df1)

l = [v for k, v in final_df1.groupby('id')]

# for i in range(len((l))):
#   #  print((1/l[i].home_odd.max()) + (1/l[0].draw_odd.max()) + (1/l[0].away_odd.max()))
#   print(l[i].max())

bookie_h = []
for i in range(len((l))):
  #  print((1/l[i].home_odd.max()) + (1/l[i].draw_odd.max()) + (1/l[i].away_odd.max()))
  tables = l[i].max()
  calc =  (1/tables.home_odd) + (1/tables.draw_odd) + (1/tables.away_odd)
  if calc > 1:
    pass
  else:
    bookie_h.append(l[i].loc[l[i].home_odd == l[i].home_odd.max()])
    print(f"{tables.home_name} - {tables.away_name} : {calc} > home bookie :")
    


# l[0].loc[l[0].home_odd == l[0].home_odd.max()]

# bookie_home = l[0].loc[l[0].home_odd == l[0].home_odd.max()]
# print(bookie_home.bookie)
# print(bookie_home.home_odd)

# bookie_home.bookie

# l[0].loc[l[0].away_odd == l[0].away_odd.max()]
# bookie_away = l[0].loc[l[0].away_odd == l[0].away_odd.max()]
# print(bookie_away.bookie)
# print(bookie_away.away_odd)

###########################

