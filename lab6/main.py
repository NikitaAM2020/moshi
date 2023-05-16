import random


class TreeNode:
    def __init__(self, state):
        self.state = state
        self.children = []

    def add_child(self, node):
        self.children.append(node)


def build_tree(state, player):
    node = TreeNode(state)
    winner = check_winner(state)

    if winner is not None:
        return node

    for i in range(3):
        for j in range(3):
            if state[i][j] == "-":
                new_state = [row.copy() for row in state]
                new_state[i][j] = player
                node.add_child(build_tree(new_state, "O" if player == "X" else "X"))

    return node


def print_board(state):
    for row in state:
        print(" ".join(row))


def check_winner(state):
    lines = state + [[state[i][j] for i in range(3)] for j in range(3)] + [[state[i][i] for i in range(3)]] + [
        [state[i][2 - i] for i in range(3)]]

    for line in lines:
        if line == ["X", "X", "X"]:
            return "X"
        elif line == ["O", "O", "O"]:
            return "O"

    return None


def get_human_move(state):
    while True:
        move = input("Enter your move (row column): ")
        parts = move.split()
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            row = int(parts[0])
            col = int(parts[1])
            if 0 <= row < 3 and 0 <= col < 3 and state[row][col] == "-":
                return row, col
        print("Invalid move. Try again.")


def get_computer_move(tree):
    best_score = float("-inf")
    best_move = None

    for child in tree.children:
        score = minimax(child, False)
        if score > best_score:
            best_score = score
            best_move = child.state

    for i in range(3):
        for j in range(3):
            if tree.state[i][j] != best_move[i][j]:
                return i, j


def minimax(node, maximizing_player):
    winner = check_winner(node.state)

    if winner is not None:
        return 1 if winner == "X" else -1

    if maximizing_player:
        max_eval = float("-inf")
        for child in node.children:
            eval = minimax(child, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for child in node.children:
            eval = minimax(child, True)
            min_eval = min(min_eval, eval)
    return min_eval


def play_game():
    state = [["-" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    tree = build_tree(state, current_player)
    while True:
        print_board(state)

        if current_player == "X":
            row, col = get_human_move(state)
            state[row][col] = current_player
        else:
            row, col = get_computer_move(tree)
            state[row][col] = current_player

        winner = check_winner(state)

        if winner is not None:
            print_board(state)
            if winner == "X":
                print("You win!")
            else:
                print("Computer wins!")
            break

        if all(state[i][j] != "-" for i in range(3) for j in range(3)):
            print_board(state)
            print("It's a tie!")
            break

        current_player = "O" if current_player == "X" else "X"


play_game()
