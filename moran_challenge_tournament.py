import sys
import argparse

from moran_challenge_support import evaluate_player_in_multiple_games

parser=argparse.ArgumentParser()
# moran_challenge_support.PlayerZero moran_challenge_support.PlayerOne moran_challenge_support.PlayerTwo moran_challenge_support.PlayerThree

parser.add_argument('-p0', help='Class for player zero', type=str, default='moran_challenge_support.PlayerZero')
parser.add_argument('-p1', help='Class for player one', type=str, default='moran_challenge_support.PlayerOne')
parser.add_argument('-p2', help='Class for player two', type=str, default='moran_challenge_support.PlayerTwo')
parser.add_argument('-p3', help='Class for player three', type=str, default='moran_challenge_support.PlayerThree')
parser.add_argument('-num_of_games', help='Number of games', type=int, default=1)
parser.add_argument('-num_of_players', help='Number of players', type=int, default=4)
parser.add_argument('-n', help='Number of nodes of the graph', type=int, default=1000)
parser.add_argument('-m', help='Number of links of each new node (Barabasi-Albert model)', type=int, default=10)
parser.add_argument('-steps', help='Maximum number of steps for the Moran procedure', type=int, default=5000)
parser.add_argument('-seed', help='Seed for random number generator', type=int, default=123)
parser.add_argument('-verbose', action='store_true', help='Verbose execution')

args=parser.parse_args()
all_flag_values = parser.parse_args()
flag_verbose = all_flag_values.verbose

# num_of_args = len(sys.argv)
# if num_of_args < 5:
#     exit(f'Insufficient number of arguments ({num_of_args - 1})')
#
# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))

# player_classes = [PlayerOmadaXX, PlayerZero, PlayerOne, PlayerTwo]
player_classes = []
# player_class_names = sys.argv[1:5]
player_class_names = [args.p0, args.p1, args.p2, args.p3]

for player_name in player_class_names:
    player_files = player_name.split('.')
    player_module_name = player_files[0]
    player_class_name = player_files[1]
    class_module = __import__(player_module_name)
    player_class = getattr(class_module, player_class_name)
    player_classes.append(player_class)

num_of_games=args.num_of_games
num_of_players=args.num_of_players
n=args.n
m=args.m
steps=args.steps
seed=args.seed

player_scores, player_name_scores, total = evaluate_player_in_multiple_games(player_classes, num_of_games=num_of_games, num_of_players=num_of_players, n=n,
                                                         m=m, steps=steps, seed=seed, verbose=flag_verbose)
print(f'Player scores: {player_scores}, player name scores: {player_name_scores}, maximum possible score: {total}')

