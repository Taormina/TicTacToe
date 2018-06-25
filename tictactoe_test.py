import pytest
from tictactoe import *

test_board = [
	['X', '', 'O'],
	['X', '', ''],
	['O', 'O', 'X']
]

def test_lanes():
	test_lanes = lanes(test_board)
	assert test_lanes[0] == ['X', '', 'O']
	assert test_lanes[1] == ['X', '', '']
	assert test_lanes[2] == ['O', 'O', 'X']
	assert test_lanes[3] == ['X', 'X', 'O']
	assert test_lanes[4] == ['', '', 'O']
	assert test_lanes[5] == ['O', '', 'X']
	assert test_lanes[6] == ['X', '', 'X']
	assert test_lanes[7] == ['O', '', 'O']

def test_no_winner():
	assert winner(empty_board()) == ''
	assert winner(test_board) == ''

def test_multiple_winners():
	"""
	undefined who should win, in theory whatever calls this should never allow this state to happen,
	but this method's responsibility is just to notice that one of them won. who gets credit is
	unhandled because this should never happen in a real game
	"""
	assert winner([
		['X', 'O', ''], 
		['X', 'O', ''], 
		['X', 'O', '']
	]) != '' 
	
def test_winner():
	assert winner([
		['X'] * 3, 
		[''] * 3,
		[''] * 3
	]) == 'X'

	assert winner([['', 'O', '']] * 3) == 'O'

def test_remaining_empty():
	assert remaining_empty(empty_board()) == 9
	assert remaining_empty([['X', 'O', 'X']] * 3) == 0
	assert remaining_empty(test_board) == 3

def test_whos_next():
	assert whos_next(empty_board()) == 'X'
	assert whos_next(test_board) == 'X'
	assert whos_next([
		['', '', ''],
		['X', '', ''],
		['', '', '']
	]) == 'O'

