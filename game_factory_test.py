import pytest
from game_factory import *
from tictactoe import empty_board, print_board
import random
from functools import reduce

def get_uuid():
	return str(uuid.uuid4())

uuid1 = get_uuid()
uuid2 = get_uuid()
prepared_game = prepare_game(uuid1, uuid2)

def test_prepare_game():
	assert prepared_game.player1 == uuid1
	assert prepared_game.player2 == uuid2

	uuid.UUID(prepared_game.game_id)

	fetched_game = get_game(prepared_game.game_id)

	assert prepared_game == fetched_game

def test_make_move():
	make_move(prepared_game.game_id, 0)
	assert get_game(prepared_game.game_id) != prepared_game # the new move makes the boards different

def test_same_move_twice():
	make_move(prepared_game.game_id, 2)
	with pytest.raises(Exception):
		make_move(prepared_game.game_id, 2)

def test_bad_move_inputs():
	with pytest.raises(Exception):
		make_move(prepared_game, 2)
	with pytest.raises(Exception):
		make_move(20, 1)
	with pytest.raises(Exception):
		make_move(prepared_game.game_id, -1)
	with pytest.raises(Exception):
		make_move(prepared_game.game_id, 10)

def test_get_logs():
	new_game = prepare_game(get_uuid(), get_uuid())
	for i in range(9):
		assert len(new_game.get_logs()) == i
		make_move(new_game.game_id, i)
	assert len(new_game.get_logs()) == 9

class MockGame(Game):
	def __init__(self, game_id=get_uuid(), player1=get_uuid(), player2=get_uuid(), positions=[]):
		self.positions = positions
		super(MockGame, self).__init__(game_id, player1, player2)

	def get_logs(self):
		return self.positions

def test_empty_construct_board():
	game = Game(get_uuid(), get_uuid(), get_uuid())
	assert game.construct_board() == empty_board()

	mock_game = MockGame()
	assert mock_game.construct_board() == empty_board()

def test_construct_board():
	game = MockGame(positions=[1])
	assert game.board == [['', 'X', ''], [''] * 3, [''] * 3]

def test_full_construct_board():
	game = MockGame(positions=range(9))
	assert game.board == [['X', 'O', 'X'], ['O', 'X', 'O'], ['X', 'O', 'X']]

def test_obvious():
	all_posititions = [i for i in range(9)]
	random.shuffle(all_posititions)
	game = MockGame(positions=all_posititions)
	flatmapped_board = flat_mapped = reduce(list.__add__, game.board)
	assert len([x for x in flat_mapped if x == 'X']) == 5
	assert len([o for o in flat_mapped if o == 'O']) == 4

def test_game_equality():
	game1 = Game('player1', 'player2')
	game2 = Game('player2', 'player1')
	game3 = Game('player1', 'player2')
	assert game1 == game1
	assert game1 != game2
	assert game1 != game3
