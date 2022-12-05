# import espn_scraper as espn
import espn_scraper as espn
import os
import json
import sys
sys.path.insert(0, 'G:\JakeDoc\Files\Projects\Python\espn_scraper')


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
        f = open(cache_name, "r")
        data = json.loads(f.read())
    else:
        print("Cache doesn't exist")
        url = espn.get_game_url(data_type, "ncb", game_id)
        data = espn.get_url(url)
        save_json(data, cache_name)
    return data


def get_playbyplay_data(pbp_data, combine_halfs=True):
    # json data looks like:
    #   page -> content -> gamepackage ->
    #                                     pbp -> playGrps
    #                                     shtChrt -> plays
    playbyplay_groups = pbp_data['page']['content']['gamepackage']['pbp']['playGrps']
    if (combine_halfs):
        # combine first and second half data
        return playbyplay_groups[0] + playbyplay_groups[1]
    return playbyplay_groups


def get_scores_by_minute(made_shots, homeAway):
    if (homeAway != 'home' and homeAway != 'away'):
        print(
            f"Error in get_scores_by_minute(). Param 'homeAway' needs to be either 'home' or 'away', it was {homeAway}")
        return
    score = homeAway + 'Score'
    pts = []
    prev_made_shots = [{'minute': 0, 'score': 0, 'player': ''}]
    for made_shot in made_shots:
        display_value = made_shot['clock']['displayValue']
        display_minute = int(display_value[:display_value.index(":")])
        period = made_shot['period']['number']
        minute = (20 * period) - display_minute
        if (made_shot['homeAway'] == homeAway):
            if (minute != prev_made_shots[0]['minute']):
                for prev_shot in prev_made_shots:
                    pts.append(
                        {'minute': prev_shot['minute'], 'score': prev_shot['score'], 'player': prev_shot['player']})
                dif = minute - \
                    prev_made_shots[0]['minute'] - \
                    len(prev_made_shots)
                for i in range(dif):
                    pts.append(
                        {'minute': prev_shot['minute']+i+1, 'score': prev_shot['score'], 'player': prev_shot['player']})
                prev_made_shots = [{'minute': minute,
                                    'score': made_shot[score],
                                    'player': get_player_who_scored(made_shot)}]
            else:
                prev_made_shots.append({'minute': minute,
                                        'score': made_shot[score],
                                        'player': get_player_who_scored(made_shot)})
    # add final minutes
    for prev_shot in prev_made_shots:
        pts.append(
            {'minute': prev_shot['minute'], 'score': prev_shot['score'], 'player': prev_shot['player']})
        dif = minute - \
            prev_made_shots[0]['minute'] - \
            len(prev_made_shots)
        for i in range(dif):
            pts.append(
                {'minute': prev_shot['minute']+i+1, 'score': prev_shot['score'], 'player': prev_shot['player']})
    return pts


def get_player_who_scored(made_shot):
    text = made_shot['text']
    return text[:text.index(" made ")]


def get_made_shots(playbyplay):
    return [s for s in playbyplay if 'scoringPlay' in s]


# pbp_data = get_espn_data("playbyplay", 401479681)
# playbyplay = get_playbyplay_data(pbp_data)
# made_shots = get_made_shots(playbyplay)
# home_score_by_minutes = get_scores_by_minute(made_shots, 'home')
# # print(home_score_by_minutes)
# away_score_by_minutes = get_scores_by_minute(made_shots, 'away')
# # print(away_score_by_minutes)



# save_json(made_shots, 'cached_data/pbp.json')
# data = {'home': [1, 4, 6, 8, 9],'away': [1, 4, 6, 8, 9]}
