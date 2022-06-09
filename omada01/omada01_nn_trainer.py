from matplotlib import pylab

from omada01.omada01_nn import Agent, TrainData
import omada01_moran
from moran_challenge_support import evaluate_player_in_multiple_games
from omada01_moran import PlayerOmada01
from omada51_moran import PlayerOmada51
from omada52_moran import PlayerOmada52
from omada53_moran import PlayerOmada53

if __name__ == '__main__':
    # get size of state and action from environment
    state_size = 1  # our nodes / total nodes 0-100%
    action_size = 3  # min, median, max degree

    load_model = False
    agent = Agent(state_size, action_size, load_model)
    data = TrainData()
    omada01_moran.PlayerOmada01.AGENT = agent
    omada01_moran.PlayerOmada01.DATA = data
    omada01_moran.PlayerOmada01.USE_NN = True

    scores, episodes = [], []
    player_classes = [PlayerOmada01, PlayerOmada51, PlayerOmada52, PlayerOmada53]

    EPISODES = 1000
    for e in range(EPISODES):
        episodes.append(e)
        games = 1
        player_scores, player_name_scores, total = evaluate_player_in_multiple_games(player_classes,
                                                                                     num_of_games=games,
                                                                                     num_of_players=4, n=1000,
                                                                                     m=10, steps=5000, seed=e,
                                                                                     verbose=False)
        print(
            f'Episode {e}:Player scores: {player_scores}, player name scores: {player_name_scores}, maximum possible score: {total}')
        scores.append(player_scores[0])
        print(f'Average score: {sum(scores) / len(scores)}')
        reward = (player_scores[0] / games - 250) / 10  # takes values from -25 to 75

        for i in range(len(data.states)):
            state = data.states[i]
            action = data.actions[i]
            agent.append_sample(state, action, reward)
        print(data.actions)
        agent.train_model()
        data.states = []
        data.actions = []
        if ((e + 1) % 5 == 0) & (load_model is False):
            agent.model.save_weights("model_weights.h5")
            pylab.plot(episodes, scores, 'b')
            pylab.savefig("train_progress.png")

