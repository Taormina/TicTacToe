from random import choice
from base_agent import *

@app.route("/play", methods=['POST'])
def play():
	json = request.get_json(force=True)
	flat_mapped = reduce(list.__add__, json["board"])
	return str(choice([i for i,x in enumerate(flat_mapped) if x == '']))