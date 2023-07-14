from operator import itemgetter
import json
FILE_NAME = 'high_score.txt'
def load():
    try:
        with open(FILE_NAME, 'r') as f:
            high_scores = json.load(f)
    except FileNotFoundError:
        high_scores = []
    finally:
        return high_scores


def record(player_name, player_score, high_scores):
    high_scores.append((player_name, player_score))
    high_scores = sorted(high_scores, key = itemgetter(1), reverse = True)[:10]

    with open(FILE_NAME, 'w') as f:
        json.dump(high_scores, f)

def get_best_ten(f):
    return(f[0:9])
#high_scores = []