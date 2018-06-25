from tictactoe import *
from flask import Flask, request
app = Flask(__name__)


@app.route("/begin", methods=['POST'])
def begin():
	url1 = request.args[""]
	"""
	Collect url1 and url2 along with a secret from each player
	Initialize and store the game somewhere
	Ping the first player to give coordinates by sending it the empty board state
	"""
	return "begin"

def get_game(game_id):
	return empty_board()

@app.route("/act")
def act():
	game = get_game(request.args["game"])

	"""
	Look up game
	Confirm it is the player's turn and perform action, 409 otherwise
	Notify next player with state
	Notify both players if game over
	"""

	return "Hello World"


test_board = [
	['X', '', ''],
	['X', '', 'O'],
	['O', 'X', '']
]

print_board(test_board)
print lanes(test_board)

print winner(test_board)
print winner(empty_board())
print winner([['X'] * 3] * 3)
print winner([['O'] * 3] * 3)

print whos_next(test_board)
print whos_next(empty_board())


if __name__ == "__main__":
    app.run()
