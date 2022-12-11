from utils import save_json
import espn_scraper as espn
import os
import json
import sys
sys.path.insert(0, 'G:\JakeDoc\Files\Projects\Python\espn_scraper')


def get_espn_data(data_type, sport, game_id):
    cache_name = f'cached_data/{data_type}_{game_id}.json'
    cache_exists = os.path.exists(cache_name)
    if cache_exists:
        print("Cache exists")
        f = open(cache_name, "r")
        data = json.loads(f.read())
    else:
        print("Cache doesn't exist")
        url = espn.get_game_url(data_type, sport, game_id)
        if (not url.endswith('_xhr=1')):
            url = url[:-6] + '&_xhr=1'
        data = espn.get_url(url)
        save_json(data, cache_name)
    return data


def get_ncb_boxscore_data(game_id):
    return get_espn_data('boxscore', 'ncb', game_id)


def get_ncb_playbyplay_data(game_id):
    return get_espn_data('playbyplay', 'ncb', game_id)
