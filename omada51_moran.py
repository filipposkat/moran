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
        a, b, players, d = self.game_info.get_number_of_active_players()

        # Choose first foreign neighbor
        targets = [v for v in list_of_neighbors if node_types[v] != self.my_type]
        node = None
        if targets:
            node = max(targets, key=lambda item: self.game_info.g.degree[item])
            history = self.game_info.history
            took_from_me = [move.player_type for move in history if move.type_from == self.my_type]
            counter = Counter(took_from_me)
            sorted_counters = sorted(counter.items(), key=lambda kv: kv[1],
                                     reverse=True)  # sorted list of players based on attacks on us
            attacks_dict = {}  # dictionary containing attacks from each player
            for item in counter.items():
                if item[0] not in attacks_dict:
                    attacks_dict[item[0]] = item[1]
            sorted_attacks = sorted(attacks_dict.keys(), key=attacks_dict.get,
                                    reverse=True)  # sorted list of players based on attack count

            cntr = Counter(node_types.values())
            n_of_nodes_by_player = {}  # dict containing number of nodes per player
            for item in cntr.items():
                # item[0] = player, item[1]=n_of_nodes
                if item[0] not in n_of_nodes_by_player:
                    n_of_nodes_by_player[item[0]] = item[1]
            sorted_player_size = sorted(n_of_nodes_by_player.keys(), key=lambda k: n_of_nodes_by_player[k])
            # if len(sorted_player_size) > 2:
            #     sorted_player_size.pop(0)  # remove smallest player

            for t in sorted_attacks:
                if t != self.my_type and t in sorted_player_size:
                    count = attacks_dict[t]
                    same_count = []
                    # Check if other players have the same count
                    for p in attacks_dict:
                        if count == attacks_dict[p] and p != self.my_type and p in n_of_nodes_by_player:
                            same_count.append(p)
                    if same_count:
                        same_count = sorted(same_count, key=lambda plr: n_of_nodes_by_player[plr],
                                            reverse=True)  # sort these players by their size
                        #t = same_count[0]  # gets the largest player with the highest attack count

                    specific_targets = [v for v in list_of_neighbors if node_types[v] == t]
                    if specific_targets:
                        nodes = sorted(specific_targets, key=lambda item: self.game_info.g.degree[item])
                        min_degree_node = nodes[0]
                        median_degree_node = nodes[int(len(nodes)/2)]
                        max_degree_node = max(specific_targets, key=lambda item: self.game_info.g.degree[item])

                        node = max_degree_node
                        adaptive = False
                        if adaptive:
                            # compare out node count with total nodes:
                            if n_of_nodes_by_player[self.my_type] >= len(self.game_info.g.nodes) / len(players):
                                # we are relatively large, so we have high probability of subsequent selection,
                                node = min_degree_node
                            else:
                                # we are relatively small, so we have low probability of subsequent selection,
                                node = max_degree_node
                        return node
        return node
