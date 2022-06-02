import random
from collections import Counter

import networkx as nx

from moran_challenge_support import Player


class PlayerOmada52(Player):

    def initialize(self, game_info, player_id, my_type, player_seed) -> None:
        # This function is called once before the game starts.
        # Can be used for initializing auxiliary data of the player
        self.name = 'omada52'
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

        # Choose first foreign neighbor
        targets = [v for v in list_of_neighbors if node_types[v] != self.my_type]
        node = None
        if targets:
            #node = targets[0]
            node = max(targets, key=lambda item: self.game_info.g.degree[item])
            counter = Counter(node_types.values())
            sorted_counter = sorted(counter.items(), key=lambda kv: kv[1], reverse=True) # kv[1] returns count of nodes for each item (node_type)
            for t,c in sorted_counter:
                if t != self.my_type:
                    specific_targets = [v for v in list_of_neighbors if node_types[v] == t]
                    if specific_targets:
                        node = max(specific_targets, key=lambda item: self.game_info.g.degree[item])
                        return node