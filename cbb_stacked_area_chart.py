from cbb_playbyplay import *


def get_bottom_of_minute_scores(scores_by_minute):
    bottom_of_minute_scores = []
    seen_minutes = set()
    for score in reversed(scores_by_minute):
        # filter out scores that are not the last score of that minute
        if score['minute'] not in seen_minutes:
            bottom_of_minute_scores.append(score)
            seen_minutes.add(score['minute'])
    bottom_of_minute_scores.reverse()
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
# print(home_scores_by_minutes)
away_scores_by_minutes = get_scores_by_minute(made_shots, 'away')
# print(away_scores_by_minutes)

bottom_of_minute_scores = get_bottom_of_minute_scores(home_scores_by_minutes)
scores = format_scores_for_stacked_area_chart(bottom_of_minute_scores)
print(len(scores))
