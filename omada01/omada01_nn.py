import random
import numpy as np
from collections import deque
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import Sequential


class Agent:
    def __init__(self, state_size, action_size, load_model=False):
        if load_model:
            self.state_size = state_size  # Get size of the state
            self.action_size = action_size  # Get size of the action
            self.last_action = None

            # Hyperparameters
            self.learning_rate = 0.00001  # Learning Rate

            # Hyperparameters to adjust the Exploitation-Explore tradeoff
            self.epsilon = 0.2  # Setting the epsilon (0= Explore, 1= Exploit)
            self.epsilon_decay = 0.999999  # Adjusting how our epsilon will decay
            self.epsilon_min = 0.2  # Min Epsilon

            self.batch_size = 5000  # Batch Size for training the neural network
            self.train_start = 50000  # If Agent's memory is less, no training is done

        else:
            self.state_size = state_size  # Get size of the state
            self.action_size = action_size  # Get size of the action
            self.last_action = None

            # Hyperparameters
            self.learning_rate = 0.01  # Learning Rate

            # Hyperparameters to adjust the Exploitation-Explore tradeoff
            self.epsilon = 1.0  # Setting the epsilon (0= Explore, 1= Exploit)
            self.epsilon_decay = 0.999  # Adjusting how our epsilon will decay
            self.epsilon_min = 0.1  # Min Epsilon

            self.batch_size = 5000  # Batch Size for training the neural network
            self.train_start = 50000  # If Agent's memory is less, no training is done

        # create main replay memory for the agent using deque
        self.memory = deque(maxlen=12000000)

        # create main model
        self.model = self.build_model()

        # Loading weights if load_model=True
        if load_model:
            try:
                self.model.load_weights("omada01/model_weights.h5")
            except FileNotFoundError:
                self.model.load_weights('model_weights.h5')

    # approximate Q function using Neural Network
    def build_model(self):
        model = Sequential()
        model.add(Dense(1, input_dim=self.state_size, activation='relu'))  # State is input
        model.add(Dense(2, activation='relu'))
        #model.add(Dense(2, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))  # Q_Value of each action is Output
        model.summary()
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    # get action from model using epsilon-greedy policy
    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            action = random.randrange(self.action_size)
        else:
            q_value = self.model.predict(state, verbose=0)
            action = np.argmax(q_value[0])
        self.last_action = action
        return action

    # save sample <state,action,reward,nest_state> to the replay memory
    def append_sample(self, state, action, reward):
        self.memory.append((state, action, reward))
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def train_model(self):
        if len(self.memory) < self.train_start:
            return
        batch_size = min(self.batch_size, len(self.memory))
        mini_batch = random.sample(self.memory, batch_size)

        update_input = np.zeros((batch_size, self.state_size))
        action, reward = [], []

        for i in range(self.batch_size):
            update_input[i] = mini_batch[i][0]
            action.append(mini_batch[i][1])
            reward.append(mini_batch[i][2])

        target = self.model.predict(update_input)
        print(action)
        for i in range(self.batch_size):
            # Q Learning: get maximum Q value at s' from model
            target[i][action[i]] = reward[i]

        # and do the model fit!
        self.model.fit(update_input, target, batch_size=self.batch_size,
                       epochs=1, verbose=0)


class TrainData:
    states = []
    actions = []


# if __name__ == '__main__':
#     # get size of state and action from environment
#     state_size = 1  # our nodes / total nodes 0-100%
#     action_size = 3  # min, median, max degree
#
#     load_model = False
#     agent = Agent(state_size, action_size, load_model)
#     data = TrainData()
#     omada01_moran.PlayerOmada01.AGENT = agent
#     omada01_moran.PlayerOmada01.DATA = data
#     omada01_moran.PlayerOmada01.USE_NN = True
#
#     scores, episodes = [], []
#     player_classes = [PlayerOmada01, PlayerOmada51, PlayerOmada52, PlayerOmada53]
#
#     EPISODES = 100
#     for e in range(EPISODES):
#         episodes.append(e)
#         games = 4
#         player_scores, player_name_scores, total = evaluate_player_in_multiple_games(player_classes,
#                                                                                      num_of_games=games,
#                                                                                      num_of_players=4, n=1000,
#                                                                                      m=10, steps=5000, seed=e,
#                                                                                      verbose=False)
#         print(f'Episode {e}:Player scores: {player_scores}, player name scores: {player_name_scores}, maximum possible score: {total}')
#         scores.append(player_scores[0])
#         print(f'Average score: {sum(scores)/len(scores)}')
#         reward = player_scores[0] - games * 1000 / 4
#
#         for i in range(len(data.states)):
#             state = data.states[i]
#             action = data.actions[i]
#             agent.append_sample(state, action, reward)
#
#         agent.train_model()
#         data.states = []
#         data.actions = []
#         if ((e+1) % 10 == 0) & (load_model is False):
#             agent.model.save_weights("model_weights.h5")
#             pylab.plot(episodes, scores, 'b')
#             pylab.savefig("train_progress.png")