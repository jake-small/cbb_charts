# import espn_scraper as espn
import os
import json
import sys
sys.path.insert(0, 'G:\JakeDoc\Files\Projects\Python\espn_scraper')
import espn_scraper as espn

def pp_json(data):
    print(json.dumps(data, indent=2, sort_keys=True))

def save_json(data, name):
  with open("{}".format(name), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

def get_espn_data(data_type, game_id):
  cache_name = f'cached_data/{data_type}_{game_id}.json'
  cache_exists = os.path.exists(cache_name)
  if cache_exists:
    print("Cache exists")
    f = open (cache_name, "r")
    data = json.loads(f.read())
  else:
    print("Cache doesn't exist")
    url = espn.get_game_url(data_type, "ncb", game_id)
    data = espn.get_url(url)
    save_json(data, cache_name)
  return data

# for data_type in ["boxscore", "playbyplay"]:
#   url = espn.get_game_url(data_type, "ncb", 401479681)
#   data = espn.get_url(url)
#   print(data)

# for index, data_type in enumerate(["boxscore", "playbyplay"]):
#   url = espn.get_game_url(data_type, "ncb", 401479681)
#   data = espn.get_url(url)
#   savejson(data, index)

get_espn_data("playbyplay", 401479681)
