SCORE_FILE = "score.txt"

def load_high_score():
    try:
        with open(SCORE_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 0

def save_high_score(score):
    high_score = load_high_score()
    if score > high_score:
        with open(SCORE_FILE, "w") as f:
            f.write(str(score))
        return score
    return high_score