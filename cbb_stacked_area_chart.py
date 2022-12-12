from cbb_boxscore import *
from espn_helper import *
from cbb_playbyplay import *
from stacked_area_chart import make_stacked_area_chart


def get_bottom_of_minute_scores(scores_by_minute):
    if (not scores_by_minute):
        no_points = []
        for i in range(1, 41):
            no_points.append({'minute': i, 'score': 0, 'player': ''})
        return no_points
    final_score_each_minute = []
    seen_minutes = set()
    for score in reversed(scores_by_minute):
        # filter out scores that are not the last score of that minute
        if (score['minute'] not in seen_minutes):
            final_score_each_minute.append(score)
            seen_minutes.add(score['minute'])
    final_score_each_minute.reverse()

    bottom_of_minute_scores = []  # [{'minute': 0, 'score': 0, 'player': ''}]
    minute = 1
    for index, score in enumerate(final_score_each_minute):
        if (score['minute'] != minute):
            for i in range(score['minute'] - minute):
                prev_score = final_score_each_minute[index-1]['score']
                prev_score = prev_score if index-1 >= 0 else 0
                empty_minute = {
                    'minute': minute, 'score': prev_score, 'player': ''}
                bottom_of_minute_scores.append(empty_minute)
                minute += 1
        bottom_of_minute_scores.append(score)
        minute += 1
    if (minute < 41):
        for i in range(41 - minute):
            prev_score = final_score_each_minute[-1]['score']
            empty_minute = {
                'minute': minute, 'score': prev_score, 'player': ''}
            bottom_of_minute_scores.append(empty_minute)
            minute += 1
    return bottom_of_minute_scores


def get_just_scores_per_minute(bottom_of_minute_scores):
    just_scores = []
    for score in bottom_of_minute_scores:
        just_scores.append(score['score'])
    return just_scores


def format_scores_for_stacked_area_chart(home_scores, away_scores):
    # e.g. formatted_scores = {'home': [1, 4, 6, 8, 9,...], 'away': [1, 4, 6, 8, 9,...]}
    return {'home': home_scores, 'away': away_scores}


def format_scores_for_stacked_area_chart(scores, labels):
    # e.g. formatted_scores = {'home': [1, 4, 6, 8, 9,...], 'away': [1, 4, 6, 8, 9,...]}
    formatted_scores = {}
    for i in range(len(scores)):
        formatted_scores[labels[i]] = scores[i]
    return formatted_scores


def get_scores_for_chart_for_players(scores_by_minute, player_names):
    scores_by_minute_for_players = get_scores_by_minute_for_players(
        scores_by_minute, player_names)
    bottom_of_minute_scores = get_bottom_of_minute_scores(
        scores_by_minute_for_players)
    scores = get_just_scores_per_minute(
        bottom_of_minute_scores)
    return scores


def get_scores_for_chart_without_players(scores_by_minute, player_names):
    scores_by_minute_for_players = get_scores_by_minute_without_players(
        scores_by_minute, player_names)
    bottom_of_minute_scores = get_bottom_of_minute_scores(
        scores_by_minute_for_players)
    scores = get_just_scores_per_minute(
        bottom_of_minute_scores)
    return scores


def get_starters_and_bench(game_id, home_away):
    bs_data = get_ncb_boxscore_data(game_id)
    boxscore = get_boxscore_data(bs_data)
    players = get_starter_bench_data(boxscore, home_away)
    return players


def create_chart_home_vs_away(game_id):
    pbp_data = get_ncb_playbyplay_data(game_id)
    playbyplay = get_playbyplay_data(pbp_data)
    made_shots = get_made_shots(playbyplay)

    home_scores_by_minutes = get_scores_by_minute(made_shots, 'home')
    home_bottom_of_minute_scores = get_bottom_of_minute_scores(
        home_scores_by_minutes)
    home_scores = get_just_scores_per_minute(
        home_bottom_of_minute_scores)

    away_scores_by_minutes = get_scores_by_minute(made_shots, 'away')
    away_bottom_of_minute_scores = get_bottom_of_minute_scores(
        away_scores_by_minutes)
    away_scores = get_just_scores_per_minute(
        away_bottom_of_minute_scores)

    stacked_area_data = format_scores_for_stacked_area_chart(
        home_scores, away_scores)
    make_stacked_area_chart(stacked_area_data)


def create_chart_players(game_id):
    pbp_data = get_ncb_playbyplay_data(game_id)
    playbyplay = get_playbyplay_data(pbp_data)
    made_shots = get_made_shots(playbyplay)

    home_players = get_starters_and_bench(game_id, 'home')
    home_scores_by_minutes = get_scores_by_minute(made_shots, 'home')
    home_scores = []
    for player_short_name in home_players['starters']:
        home_scores_player = get_scores_for_chart_for_players(
            home_scores_by_minutes, [player_short_name])
        home_scores.append(home_scores_player)
    home_scores_bench = get_scores_for_chart_without_players(
        home_scores_by_minutes, home_players['starters'])
    home_scores.append(home_scores_bench)

    away_players = get_starters_and_bench(game_id, 'away')
    away_scores_by_minutes = get_scores_by_minute(made_shots, 'away')
    away_scores = []
    away_scores_bench = get_scores_for_chart_without_players(
        away_scores_by_minutes, away_players['starters'])
    away_scores.append(away_scores_bench)
    for player_short_name in away_players['starters']:
        away_scores_player = get_scores_for_chart_for_players(
            away_scores_by_minutes, [player_short_name])
        away_scores.append(away_scores_player)

    scores = away_scores + home_scores
    labels = ['away bench'] + away_players['starters'] + \
        home_players['starters'] + ['home bench']
    stacked_area_data = format_scores_for_stacked_area_chart(
        scores,
        labels)

    make_stacked_area_chart(stacked_area_data)


# create_chart_home_vs_away(401479681)
create_chart_players(401479681)
