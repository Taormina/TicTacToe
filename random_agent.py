from random import choice
from base_agent import *
from functools import reduce


game_server = 'http://localhost:5000/act'

@app.route("/play", methods=['POST'])
def play():
	json = request.get_json(force=True)
	flat_mapped = reduce(list.__add__, json["board"])
	position = choice([i for i,x in enumerate(flat_mapped) if x == ''])

	requests.post(game_server, json={"position": position, "game": json["game"]})


	return 'ok'