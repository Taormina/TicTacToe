from tictactoe import empty_board, whos_next, print_board, still_going, winner
import uuid
import pymysql.cursors
from flask import abort
import requests
import json

# if you'd like security, obviously change these
connection = pymysql.connect(host='localhost', user='root', password='', db='tictactoe', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

class Game():
	def __init__(self, player1, player2, game_id=None):
		self.game_id = game_id if game_id else str(uuid.uuid4())
		self.player1 = player1
		self.player2 = player2
		self.board = self.construct_board()
	def __eq__(self, other):
		return self.game_id == other.game_id and self.player1 == other.player1 and self.player2 == other.player2 and self.board == other.board

	def __str__(self):
		return "Game {} - {} vs. {}".format(self.game_id, self.player1, self.player2)

	def get_logs(self):
		try:
			with connection.cursor() as cursor:
				sql = """
					SELECT position
					FROM game_log l 
						JOIN game g
							ON l.game_id = g.id 
								AND g.id = %s
					ORDER BY time ASC"""
				cursor.execute(sql, (self.game_id,))
			connection.commit()
			return [row["position"] for row in cursor.fetchmany(size=9)]
		except Exception:
			abort(409, "Game ID {} couldn't be constructed!".format(self.game_id))

	def construct_board(self):
		moves = self.get_logs()
		board = empty_board()
		for move in moves:
			turn_taker = whos_next(board)
			y = move // 3
			x = move % 3
			if board[y][x]:
				abort(409, "Something is wrong with game history! Please make a new game.")
			board[y][x] = turn_taker
		return board
		
		

def prepare_game(player1, player2):
	# does execute sanitize this?
	game_id = str(uuid.uuid4())
	game = Game(player1, player2, game_id)
	try:
		with connection.cursor() as cursor:
			sql = """INSERT INTO game(id, player1, player2) 
				VALUES (%s, %s, %s)"""
			cursor.execute(sql, (game_id, player1, player2))
			connection.commit()
	except Exception:
		abort(500, "Failed to create Game ID {}!".format(game_id))
	return game


def get_game(game_id):
	game_row = None
	try:
		with connection.cursor() as cursor:
			sql = """SELECT player1, player2
				FROM game
				WHERE id = %s"""
			cursor.execute(sql, (game_id,))
		
		connection.commit()
		game_row = cursor.fetchone()
	except Exception:
		abort(404, "Game ID {} does not exist!".format(game_id))
	
	if game_row:
		return Game(game_row["player1"], game_row["player2"], game_id)
	else:
		abort(404, "Game ID {} does not exist!".format(game_id))


def make_move(game_id, position):
	if not isinstance(game_id, str):
		abort(400, "Invalid game id, you gave: {}".format(game_id))

	if not isinstance(position, int) or position not in range(9):
		abort(400, "Invalid position, should be 0 <= position <= 8, you gave: {}".format(position))

	try:
		with connection.cursor() as cursor:
			sql = """INSERT INTO game_log (game_id, position)
				VALUES (%s, %s)"""
			cursor.execute(sql, (game_id, position))
		
		connection.commit()
	except pymysql.err.IntegrityError:
		abort(409, "Couldn't insert move {} into game {} because this move has already been made".format(position, game_id))
	except Exception:
		abort(500, "Couldn't insert move {} into game {}".format(position, game_id))


def begin_game(player1, player2):
	game = prepare_game(player1, player2)
	resolve_and_alert(game)
	return game

def act_in_game(game_id, position):
	make_move(game_id, position)
	game = get_game(game_id)
	resolve_and_alert(game)
	return game

def resolve_and_alert(game):
	if still_going(game.board):
		next_up = whos_next(game.board)
		player = game.player1 if next_up == 'X' else game.player2
		# ping player/play with the game.board
		requests.post("{}/play".format(player), json={"board": game.board, "game": game.game_id})

	else:
		winning_side = winner(game.board)
		if winning_side == 'X':
			requests.post("{}/finish".format(game.player1), json={"winner": 1})
			requests.post("{}/finish".format(game.player2), json={"winner": -1})
		if winning_side == 'O':
			requests.post("{}/finish".format(game.player2), json={"winner": 1})
			requests.post("{}/finish".format(game.player1), json={"winner": -1})	
		else:
			requests.post("{}/finish".format(game.player1), json={"winner": 0})
			requests.post("{}/finish".format(game.player2), json={"winner": 0})

import atexit
def cleanup():
	connection.close()
atexit.register(cleanup)