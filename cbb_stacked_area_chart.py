from cbb_playbyplay import *
from stacked_area_chart import make_stacked_area_chart


def get_bottom_of_minute_scores(scores_by_minute):
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
            prev_score = prev_score if index-1 >= 0 else 0
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


def create_chart_home_vs_away(game_id):
    pbp_data = get_espn_data("playbyplay", game_id)
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
    pbp_data = get_espn_data("playbyplay", game_id)
    playbyplay = get_playbyplay_data(pbp_data)
    made_shots = get_made_shots(playbyplay)

    home_scores_by_minutes = get_scores_by_minute(made_shots, 'home')
    home_scores_TrayceJacksonDavis = get_scores_for_chart_for_players(
        home_scores_by_minutes, ['Trayce Jackson-Davis'])
    home_scores_bench = get_scores_for_chart_without_players(
        home_scores_by_minutes, ['Trayce Jackson-Davis'])

    away_scores_by_minutes = get_scores_by_minute(made_shots, 'away')
    away_scores_PeteNance = get_scores_for_chart_for_players(
        away_scores_by_minutes, ['Pete Nance'])
    away_scores_bench = get_scores_for_chart_without_players(
        away_scores_by_minutes, ['Pete Nance'])

    stacked_area_data = format_scores_for_stacked_area_chart(
        [away_scores_PeteNance, away_scores_bench,
            home_scores_bench, home_scores_TrayceJacksonDavis],
        ['Nance', 'UNC Bench', "IU Bench", 'TJD'])

    # stacked_area_data = format_scores_for_stacked_area_chart(
    #     home_scores, away_scores)

    make_stacked_area_chart(stacked_area_data)


# create_chart_home_vs_away(401479681)
create_chart_players(401479681)
