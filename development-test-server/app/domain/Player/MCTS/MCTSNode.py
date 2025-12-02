import math


class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.value = 0
        self.untried_moves = state.legal_move() if state else []

    def best_child(self, exploration):
        best_score = -float('inf')
        best_child = None
        for child in self.children:
            exploit = child.value / child.visits if child.visits > 0 else 0
            explore = math.sqrt(math.log(self.visits) / child.visits) if child.visits > 0 else float('inf')
            score = exploit + exploration * explore
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def print_tree(self, depth=0, max_depth=2, prefix="", is_last=True):
        if depth == 0:
            print("\nMCTS Search Tree (up to depth={}):".format(max_depth))
            print("-- Each line shows:")
            print("   [Move made] by [Player], Visited [X times], Win rate [Y]")
            print("   Moves branch right; first move is most explored.\n")
        # Set up branch structure
        branch = "└─" if is_last else "├─"
        next_prefix = prefix + ("   " if is_last else "│  ")

        # Simple labels
        move_str = "Root" if self.move is None else f"Move {self.move}"
        player_str = f"Player {self.state.current_player()}" if hasattr(self, 'state') else ""
        avg_value = self.value / self.visits if self.visits > 0 else 0
        print(f"{prefix}{branch} {move_str} by {player_str} | Visited {self.visits} times | Win Rate: {avg_value:.2f}")

        # Print children
        if depth < max_depth:
            for i, child in enumerate(sorted(self.children, key=lambda c: c.visits, reverse=True)):
                child_is_last = (i == len(self.children) - 1)
                child.print_tree(depth + 1, max_depth, next_prefix, child_is_last)