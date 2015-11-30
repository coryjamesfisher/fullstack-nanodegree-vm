-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- CREATE TOURNAMENT DB AND SWITCH TO IT
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\connect tournament

-- CREATE PLAYER STRUCTURE
CREATE TABLE player
(
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL
);


-- CREATE MATCH_STATE STRUCTURE
CREATE TABLE match_state
(
	id INTEGER NOT NULL PRIMARY KEY,
	description TEXT NOT NULL
);

-- INSERT ALL VALID STATES FOR A MATCH
INSERT INTO 
	match_state (id, description)
 VALUES (1, 'Not Started'),
	(2, 'In Progress'),
	(3, 'Finished');


-- CREATE MATCH STRUCTURE
CREATE TABLE match
(
	id SERIAL PRIMARY KEY,
	playerOneId INTEGER NOT NULL REFERENCES player (id),
	playerTwoId INTEGER NOT NULL REFERENCES player (id),
	winningPlayerId INTEGER DEFAULT NULL REFERENCES player (id),
	match_state INTEGER NOT NULL DEFAULT 1 REFERENCES match_state (id)
);

