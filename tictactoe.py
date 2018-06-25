"""
A board is a String[3][3] contain one of the following values ['X', 'O', '']
Winner is follows the same enum structure.
Both can always be found on the state.
"""

def lanes(board):
	return [
		board[0], # top row
		board[1], # middle row
		board[2], # bottom row
		[row[0] for row in board], # left column
		[row[1] for row in board], # middle column
		[row[2] for row in board], # right column
		[board[0][0], board[1][1], board[2][2]], # downward diagonal
		[board[0][2], board[1][1], board[2][0]] # upward diagonal
	]

def print_board(board):
	for row in board:
		row = ['_' if x == '' else x for x in row]
		print ' '.join(row)
		

def winner(board):
	player1win = ['X'] * 3
	player2win = ['O'] * 3
	for lane in lanes(board):
		if lane == player1win:
			return 'X'
		if lane == player2win:
			return 'O'
	return ''

def is_empty(board):
	flat_mapped = reduce(list.__add__, board)
	remaining_empty = len([x for x in flat_mapped if x == ''])
	return remaining_empty > 0

def whos_next(board):
	flat_mapped = reduce(list.__add__, board)
	remaining_empty = len([x for x in flat_mapped if x == ''])
	return 'X' if remaining_empty % 2 else 'O' 

def empty_board():
	return [[''] * 3] * 3