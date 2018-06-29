CREATE DATABASE IF NOT EXISTS tictactoe;

USE tictactoe;

CREATE TABLE IF NOT EXISTS game (
	id VARCHAR(60) NOT NULL,
	player1 CHAR(128) NOT NULL,
	player2 CHAR(128) NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT current_timestamp,
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS game_log (
	game_id VARCHAR(60) NOT NULL,
	position TINYINT NOT NULL,
	time TIMESTAMP NOT NULL DEFAULT current_timestamp,
	PRIMARY KEY (game_id, position),
	FOREIGN KEY (game_id) REFERENCES game(id)
);
