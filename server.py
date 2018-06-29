from tictactoe import *
from game_factory import begin_game, act_in_game
from flask import Flask, request
app = Flask(__name__)


@app.route("/begin", methods=['POST'])
def begin():
	json = request.get_json(force=True)
	"""
	Collect url1 and url2 <along with a secret from each player>
	Initialize and store the game somewhere
	Ping the first player to give coordinates by sending it the empty board state
	"""
	begin_game(json["player1"], json["player2"])
	print("let's begin") 
	return "ok"

def get_game(game_id):
	return empty_board()

@app.route("/act", methods=['POST'])
def act():
	"""
	Look up game
	Confirm it is the player's turn and perform action, 409 otherwise
	Notify next player with state
	Notify both players if game over
	"""
	import time
	time.sleep(2)
	json = request.get_json(force=True)
	game = act_in_game(json["game"], json["position"])
	print_board(game.board)
	return "ok"


# test_board = [
# 	['X', '', 'O'],
# 	['X', '', 'O'],
# 	['O', '', 'X']
# ]

# print_board(test_board)
# print(lanes(test_board))

# print(winner(test_board))
# print(winner(empty_board()))
# print(winner([['X'] * 3] * 3))
# print(winner([['O'] * 3] * 3))

# print(whos_next(test_board))
# print(whos_next(empty_board()))


if __name__ == "__main__":
    app.run()
