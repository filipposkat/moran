import random
from collections import Counter

import networkx as nx

from moran_challenge_support import Player


class PlayerOmada51(Player):
    def initialize(self, game_info, player_id, my_type, player_seed) -> None:
        # This function is called once before the game starts.
        # Can be used for initializing auxiliary data of the player
        self.name = 'omada51'
        self.version = '0.1'

        self.game_info = game_info
        self.id = player_id
        self.my_type = my_type
        self.player_seed = player_seed
        self.rng = random.Random(self.player_seed)

    def move(self, from_node) -> int:
        # This function is called everytime player b has been selected for a move

        neighbors = self.game_info.g.neighbors(from_node)
        list_of_neighbors = list(neighbors)
        node_types = nx.get_node_attributes(self.game_info.g, "types")
        eg_centralities = nx.eigenvector_centrality(self.game_info.g)
        # Choose first foreign neighbor
        targets = [v for v in list_of_neighbors if node_types[v] != self.my_type]
        node = None
        if targets:
            node = max(targets, key=lambda item: self.game_info.g.degree[item])
            history = self.game_info.history
            took_from_me = [move.player_type for move in history if move.type_from == self.my_type]
            counter = Counter(took_from_me)
            sorted_counters = sorted(counter.items(), key=lambda kv: kv[1], reverse=True)  # sorted list of players based on attacks on us
            attacks_dict = {}  # dictionary containing attacks from each player
            for item in counter.items():
                if item[0] not in attacks_dict:
                    attacks_dict[item[0]] += item[1]
            cntr, num_of_distinct_type_values, distinct_type_keys, distinct_type_counts = self.game_info.get_number_of_active_players() # gets counte
            n_of_nodes_by_player = {}
            for item in cntr.items():
                if item[0] not in n_of_nodes_by_player:
                    n_of_nodes_by_player[item[0]] = item[1]

            for t, c in sorted_counters:
                if t != self.my_type:
                    count = attacks_dict[t]
                    same_count = []
                    # Check if other players have the same count
                    for p in attacks_dict:
                        if count == attacks_dict[p] and p != self.my_type:
                            same_count.append(p)
                    same_count.sort(key=lambda plr:n_of_nodes_by_player[plr])

                    specific_targets = [v for v in list_of_neighbors if node_types[v] == t]
                    if specific_targets:
                        node=max(specific_targets, key=lambda item:self.game_info.g.degree[item])
                        #node = max(specific_targets, key=lambda item: eg_centralities[item])
                        return node
        return node
