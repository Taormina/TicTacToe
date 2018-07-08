# Tic-Tac-Toe
## Anthony, what is this?

I'm trying to make games! As some of you may be aware, I just started Taormina Innovations, LLC. I would love feedback from friends that would potentially be interested in playing "AI Games".

## AI Games, what are we talking here?

For now, just Tic-Tac-Toe to serve as a proof of concept to start the conversation. But we could be talking about a lot more! For now, I really want to collect feedback [**on this Google Form**](https://goo.gl/forms/Y8AXjW7gjqYdbE1O2) about what sorts of games might be interesting to build for.

Tic-Tac-Toe is interesting, so to win, you'll need to be able to build something that would never lose.

## What is this repository?

This is the source code for the game server along with an agent that plays randomly. Directions for running it locally are below. With this, you can easily test your own agents, which can be written in whatever language you want.

# The Protocol

As implemented, the game server manages distinct games between a `player1` and a `player2`. The arguments are the **exact address to connect to with no trailing slash**. There are no SLAs and anyone can take as long as they need. A game is started by sending the following request to the game server.
```
POST /begin
{
	"player1": "http://localhost:9001",
	"player2": "http://127.0.0.1:9002"
}
```

Once the server receives this message and initializes a new game between these two players, it then asks player1 to begin play. Each player acts on their turn by implementing the following endpoint.
```
POST /play
{
	"board": [
	    ["", "", ""],
	    ["X", "", ""],
	    ["", "", "O"]
	],
	"game": "<uuid>"
}
```

The agent that receives this message is expected to play next, so in this case would be 'X'. The next move is made by declaring the integer position between 0 and 8 that you would like to play at, as shown below.
```
[
	[0, 1, 2],
	[3, 4, 5],
	[6, 7, 8]
]
```
When the agent has decided its next move, it will hit the game server.
```
POST /act
{
	"position": 0
	"game": "<unique game id from the /play request>"
}
```

The game server will continue alternating turns between the players until a winner has been decided. When this happens, the game is over and both players will be hit at the following endpoint where a win is a 1, a draw is a 0, and a loss is a -1.
```
POST /winner
{
	"winner": 0
}
```

## Game Server Responses
If for some reason there is a problem with the game, the game will throw an error, otherwise, default it will return a 200 "ok" message if everything worked.

# Installing
`virtualenv` and the like are things you might want to bother with before going forward.

## The APIs
`pip install -r requirements.txt`

## The Database
```
brew install mysql
```

### Creating the tables
```
mysql -uroot # connect to a MySQL shell as the root user
mysql> source setup.sql;
mysql> quit;
```

# Running

## The Game Server
`FLASK_APP=server.py flask run`

## The Random Agent
`FLASK_APP=random_agent.py flask run`

## The Database
`brew services start mysql` # will keep MySQL running in the background.

### Creating the tables
```
mysql -uroot # connect to a MySQL shell as the root user
mysql> source setup.sql;
mysql> quit;
```

## Docker
It's also possible to develop locally using docker + docker compose:

```sh
## binds game server to `:80` (override with `GAME_PORT=<NUMBER>`)
docker-compose up
```

# Testing
`pytest`

# Hosting
I recommend `ngrok` for anyone hosting their agent to the world temporarily. Also, this would mean that anyone can run a game server for themselves without even needing to be in the same network.
