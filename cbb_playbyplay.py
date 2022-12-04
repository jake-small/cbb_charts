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


def get_score_by_minute(made_shots, home_team):
    # home_pts
    #   minute
    #   total score
    # away_pts
    #   minute
    #   total score

    # 19:41 -> 1
    homeAway = 'home' if home_team else 'away'
    score = homeAway + 'Score'
    pts = []
    prev_made_shots = [{'minute': 0, 'score': 0}]
    for made_shot in made_shots:
        display_value = made_shot['clock']['displayValue']
        display_minute = int(display_value[:display_value.index(":")])
        period = made_shot['period']['number']
        minute = (20 * period) - display_minute
        if (made_shot['homeAway'] == homeAway):
            if (minute != prev_made_shots[0]['minute']):
                for prev_shot in prev_made_shots:
                    pts.append(
                        {'minute': prev_shot['minute'], 'score': prev_shot['score']})
                dif = minute - \
                    prev_made_shots[0]['minute'] - \
                    len(prev_made_shots)
                for i in range(dif):
                    pts.append(
                        {'minute': prev_shot['minute']+i+1, 'score': prev_shot['score']})
                prev_made_shots = [{'minute': minute,
                                    'score': made_shot[score]}]
            else:
                prev_made_shots.append({'minute': minute,
                                        'score': made_shot[score]})
                # dif = minute - prev_home_made_shot['minute']
                # for i in range(dif):
                #     print(dif)
                #     # print(prev_home_made_shot['homeScore'])
                #     home_pts.append(
                #         {'minute': minute, 'homeScore': prev_home_made_shot['homeScore']})
            # prev_home_made_shot = {'minute': minute,
            #                        'homeScore': made_shot['homeScore']}

    # add final minutes points
    for prev_shot in prev_made_shots:
        pts.append(
            {'minute': prev_shot['minute'], 'score': prev_shot['score']})
        dif = minute - \
            prev_made_shots[0]['minute'] - \
            len(prev_made_shots)
        for i in range(dif):
            pts.append(
                {'minute': prev_shot['minute']+i+1, 'score': prev_shot['score']})

    # print(pts)
    return pts


pbp = get_espn_data("playbyplay", 401479681)

# json data we need should be around here:
# page -> content -> gamepackage ->
#                                   pbp -> playGrps
#                                   shtChrt -> plays
playbyplay_groups = pbp['page']['content']['gamepackage']['pbp']['playGrps']
playbyplay = playbyplay_groups[0] + playbyplay_groups[1]
made_shots = [s for s in playbyplay if 'scoringPlay' in s]

get_score_by_minute(made_shots, True)

# save_json(made_shots, 'cached_data/pbp.json')

# data = {'home': [1, 4, 6, 8, 9],'away': [1, 4, 6, 8, 9]}
