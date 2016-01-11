#!/usr/bin/env python
"""
tournament.py -- implementation of a Swiss-system tournament
"""

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def delete_matches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""DELETE FROM match""")
        conn.commit()
    except psycopg2.Error:
        print "Failed to delete matches"


def delete_players():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""DELETE FROM player""")
        conn.commit()
    except psycopg2.Error:
        print "Failed to delete players"


def count_players():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""SELECT COUNT(*) FROM player""")
        return cur.fetchone()[0]
    except psycopg2.Error:
        print "Failed to count players"
        return

def register_player(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""INSERT INTO player (name) VALUES (%s)""", (name,))
        conn.commit()
    except psycopg2.Error:
        print "Failed to register player"
        raise

def player_standings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            'SELECT player.id, player.name, '
            'SUM(CASE WHEN matches.winningPlayerId = player.id THEN 1 ELSE 0 END) as wins, '
            'count(matches) as matches '
            'FROM player '
            'LEFT JOIN match matches on matches.playerOneId = player.id '
            'OR matches.playerTwoId = player.id '
            'GROUP BY player.id, player.name ORDER BY wins desc, player.id ASC')
        return cur.fetchall()
    except psycopg2.Error:
        print "Failed to count players"
        raise

def report_match(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            'INSERT INTO match '
            '(playerOneId, playerTwoId, winningPlayerId, match_state) '
            ' VALUES (%s, %s, %s, 3)',
            (winner, loser, winner,))
        conn.commit()
    except psycopg2.Error:
        print "Failed to register player"
        raise


def swiss_pairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = player_standings()
    matches = list()

    for player_one_index in range(len(standings)):

        # If this player makes the pair
        if (player_one_index + 1) % 2 == 0:

            # Get the previous player
            player_two_index = player_one_index - 1

            # Add a match with current and previous player
            match = (
                standings[player_one_index][0], standings[player_one_index][1],
                standings[player_two_index][0], standings[player_two_index][1]
            )
            matches.append(match)

    return matches
