

from utils import first


def get_boxscore_data(bs_data):
    # json data looks like:
    #   page -> content -> gamepackage ->
    #                                     bxscr -> [{home team}, {away team}]
    return bs_data['page']['content']['gamepackage']['bxscr']


def get_starter_bench_data(bs_data, home_away):
    is_home = True if home_away == 'home' else False
    data = first(bs_data, condition=lambda x: x['tm']['hm'] == is_home)
    starters = first(data['stats'],
                     condition=lambda x: x['type'] == 'starters')
    starter_names = get_athletes(starters)
    bench = first(data['stats'],
                  condition=lambda x: x['type'] == 'bench')
    bench_names = get_athletes(bench)
    return {'starters': starter_names, 'bench': bench_names}


def get_athletes(raw_athlete_data):
    athletes = []
    for athlete in raw_athlete_data['athlts']:
        athletes.append(athlete['athlt']['shrtNm'])
    return athletes
