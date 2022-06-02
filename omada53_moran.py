import random

import networkx as nx

from moran_challenge_support import Player


class PlayerOmada53(Player):

    def initialize(self, game_info, player_id, my_type, player_seed) -> None:
        # This function is called once before the game starts.
        # Can be used for initializing auxiliary data of the player
        self.name = 'omada53'
        self.version = '0.1'

        self.game_info = game_info
        self.id = player_id
        self.my_type = my_type
        self.player_seed = player_seed
        self.rng = random.Random(self.player_seed)

    def move(self, from_node) -> int:
        # This function is called everytime player b has been selected for a move
        G = self.game_info.g
        rnd = self.rng

        nodes = G.nodes()
        neighbors = self.game_info.g.neighbors(from_node)
        list_of_neighbors = list(neighbors)
        node_types = nx.get_node_attributes(self.game_info.g, "types")

        # Choose first foreign neighbor
        rnd.seed(self.player_seed)
        targets = [v for v in list_of_neighbors if node_types[v] != self.my_type]
        node = None

        if targets:
            # Option 1: use random target #
            # node = targets[rnd.randint(0, len(targets) - 1)]

            # Option 2: Use centrality #
            centralities = nx.eigenvector_centrality(G)
            tragets_centralities = {}
            for t in targets:
                tragets_centralities[t] = centralities[t]

            # finds the target (key) with maximum centrality:
            max_centr_target = max(tragets_centralities, key=tragets_centralities.get)
            node = max_centr_target
        return node

