from cbb_playbyplay import *


def get_bottom_of_minute_scores(scores_by_minute):
    final_score_each_minute = []
    seen_minutes = set()
    for score in reversed(scores_by_minute):
        # filter out scores that are not the last score of that minute
        if (score['minute'] not in seen_minutes):
            final_score_each_minute.append(score)
            seen_minutes.add(score['minute'])
    final_score_each_minute.reverse()

    bottom_of_minute_scores = [{'minute': 0, 'score': 0, 'player': ''}]
    minute = 1
    for index, score in enumerate(final_score_each_minute):
        if (score['minute'] != minute):
            for i in range(score['minute'] - minute):
                prev_score = final_score_each_minute[index -
                                                     1]['score'] if index-1 >= 0 else 0
                empty_minute = {
                    'minute': minute, 'score': prev_score, 'player': ''}
                bottom_of_minute_scores.append(empty_minute)
                minute += 1
        bottom_of_minute_scores.append(score)
        minute += 1
    return bottom_of_minute_scores


def format_scores_for_stacked_area_chart(bottom_of_minute_scores):
    # e.g. formatted_scores = {'home': [1, 4, 6, 8, 9,...], 'away': [1, 4, 6, 8, 9,...]}
    formatted_scores = []
    for score in bottom_of_minute_scores:
        formatted_scores.append(score['score'])
    return formatted_scores


pbp_data = get_espn_data("playbyplay", 401479681)
playbyplay = get_playbyplay_data(pbp_data)
made_shots = get_made_shots(playbyplay)

home_scores_by_minutes = get_scores_by_minute(made_shots, 'home')
home_bottom_of_minute_scores = get_bottom_of_minute_scores(
    home_scores_by_minutes)
home_scores = format_scores_for_stacked_area_chart(
    home_bottom_of_minute_scores)

away_scores_by_minutes = get_scores_by_minute(made_shots, 'away')
away_bottom_of_minute_scores = get_bottom_of_minute_scores(
    away_scores_by_minutes)
away_scores = format_scores_for_stacked_area_chart(
    away_bottom_of_minute_scores)


print(home_scores)
print(away_scores)
