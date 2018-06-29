from flask import Flask, request
import requests
app = Flask(__name__)

wins = 0
loses = 0
draws = 0

@app.route("/finish", methods=['POST'])
def finish():
	global wins
	global loses
	global draws
	result = request.get_json(force=True)["winner"]
	if result == 1:
		wins += 1
	elif result == 0:
		draws += 1
	elif result == -1:
		loses += 1
	return "ok"

if __name__ == "__main__":
    app.run()


import atexit
def tally_results():
	global wins
	global loses
	global draws
	print("I won {0} times, lost {1} times, and tied {2} for a career total score of {3}".format(wins, loses, draws, wins - loses))
atexit.register(tally_results)
