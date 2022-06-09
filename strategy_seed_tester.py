from matplotlib import pylab
import numpy as np

from moran_challenge_support import evaluate_player_in_multiple_games
from omada01_moran import PlayerOmada01
from omada51_moran import PlayerOmada51
from omada52_moran import PlayerOmada52
from omada53_moran import PlayerOmada53


if __name__ == '__main__':
    # get size of state and action from environment
    player_classes = [PlayerOmada01, PlayerOmada51, PlayerOmada52, PlayerOmada53]

    MAX_SEED = 1000
    GAMES = 1

    scores = []
    wins = 0
    for s in range(MAX_SEED):
        player_scores, player_name_scores, total = evaluate_player_in_multiple_games(player_classes,
                                                                                     num_of_games=GAMES,
                                                                                     num_of_players=4, n=1000,
                                                                                     m=10, steps=5000, seed=s,
                                                                                     verbose=False)
        print(f'Episode {e}:Player scores: {player_scores}, player name scores: {player_name_scores}, maximum possible score: {total}')
        scores.append(player_scores[0])
        if player_scores[0] == max(player_scores):
            wins += 1
        avg = np.mean(scores)
        std = np.std(scores)
        cv = std/avg
        print(f'Average score: {avg}')
        print(f'Standard Deviation/AVG: {cv*100:.2}%')

    avg = np.mean(scores)
    median = np.median(scores)
    std = np.std(scores)
    cv = std / avg
    ci_low = avg - 2*std/np.sqrt(len(scores))
    ci_high = avg + 2*std/np.sqrt(len(scores))
    print("=================Results=====================")
    print(f'Mean: {avg}')
    print(f'Median: {median}')
    print(f'CV: {cv*100:.2}')
    print(f'95% Confidence Interval: {ci_low} - {ci_high}')
    print('==============================================')

