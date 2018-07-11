from base_agent import *
from functools import reduce
import math, random

max_score = 10
min_score = -10
max_depth = 10

game_server = 'http://localhost:5000/act'

@app.route("/play", methods=['POST'])
def play():
    json = request.get_json(force=True)
    flat_mapped = reduce(list.__add__, json["board"])
    pretty_print(flat_mapped)

    # Need a way for the agent to become aware of which player it is
    player = 'O'
    position = minimax(flat_mapped, player)[0]
    print("Going to make move:", position)

    requests.post(game_server, json={"position": position, "game": json["game"]})

    return 'ok'

def is_win(game_state, player):
    if len(game_state) != 9:
        raise ValueError('game_state does not have a length of 9')
    elif (
        all_equal(game_state[0:3], player)
        or all_equal(game_state[3:6], player)
        or all_equal(game_state[6:9], player)
        or all_equal([game_state[i] for i in [0,3,6]], player)
        or all_equal([game_state[i] for i in [1,4,7]], player)
        or all_equal([game_state[i] for i in [2,5,8]], player)
        or all_equal([game_state[i] for i in [0,4,8]], player)
        or all_equal([game_state[i] for i in [2,4,6]], player)
    ):
        return True
    else:
        return False

def has_ended(game_state):
    return len(get_available_moves(game_state)) == 0

def get_other_player(player):
    if player == 'X':
        return 'O'
    else:
        return 'X'

def all_equal(list, value):
    # https://stackoverflow.com/questions/3525953/check-if-all-values-of-iterable-are-zero
    return all(i == value for i in list)

def calculate_score(game_state, player):
    if is_win(game_state, player):
        return max_score
    elif is_win(game_state, get_other_player(player)):
        return min_score
    else:
        return 0

def get_available_moves(game_state):
    empty_moves = ['', ' ', None, 0]
    return [i for i,x in enumerate(game_state) if x in empty_moves]

def make_move(game_state, player, move):
    if isinstance(game_state, str):
        game_state = list(game_state)
        game_state[move] = player
        game_state = "".join(game_state)
    else:
        game_state[move] = player
    return game_state

def minimax(game_state, player):
    # returns a tuple of (best_move, best_score)
    return optimize_children_by_score(game_state, player, 0, min, max_value, return_move=True)

def max_value(game_state, player, depth):
    # returns max score
    return optimize_children_by_score(game_state, player, depth, max, min_value)

def min_value(game_state, player, depth):
    # returns min score
    return optimize_children_by_score(game_state, player, depth, min, max_value)

def optimize_children_by_score(game_state, player, depth, parent_optimization_function, child_optimization_function, return_move=False):
    if has_ended(game_state) or depth >= max_depth:
        score = calculate_score(game_state, player)
        if return_move:
            # I don't know why I'm randomly returning a move in this case and it may be introducing a bug
            return (random.choice(get_available_moves(game_state)), score)
        else:
            return score
        return

    other_player = get_other_player(player)
    optimized_move_and_score = parent_optimization_function([(move, child_optimization_function(make_move(game_state, other_player, move), other_player, 0)) for move in get_available_moves(game_state)], key = lambda x: x[1])

    if return_move:
        return optimized_move_and_score
    else:
        return optimized_move_and_score[1]

def pretty_print(game_state):
    print(game_state[0:3])
    print(game_state[3:6])
    print(game_state[6:9])
    print('---')
