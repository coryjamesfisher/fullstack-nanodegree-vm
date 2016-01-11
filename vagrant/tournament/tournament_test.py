#!/usr/bin/env python
"""
Test cases for tournament.py
"""

from tournament import *

def test_delete_matches():
    """
    Test that the module can delete matches
    """
    delete_matches()
    print "1. Old matches can be deleted."


def test_delete():
    """
    Test that the module can delete matches and players
    """
    delete_matches()
    delete_players()
    print "2. Player records can be deleted."

def test_count():
    """
    Test that the module can get the count of players
    """
    delete_matches()
    delete_players()
    player_count = count_players()
    if player_count == '0':
        raise TypeError(
                "countPlayers() should return numeric zero, not string '0'.")
    if player_count != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."

def test_register():
    """
    Test that the module can register players
    """
    delete_matches()
    delete_players()
    register_player("Chandra Nalaar")
    player_count = count_players()
    if player_count != 1:
        raise ValueError(
                "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."

def test_register_count_delete():
    """
    Test that the module can count after adding and deleting players
    """
    delete_matches()
    delete_players()
    register_player("Markov Chaney")
    register_player("Joe Malik")
    register_player("Mao Tsu-hsi")
    register_player("Atlanta Hope")
    player_count = count_players()
    if player_count != 4:
        raise ValueError(
                "After registering four players, countPlayers should be 4.")
    delete_players()
    player_count = count_players()
    if player_count != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."

def test_standings_before_matches():
    """
    Test that the module gives accurate pre-match standings
    """
    delete_matches()
    delete_players()
    register_player("Melpomene Murray")
    register_player("Randy Schwartz")
    standings = player_standings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
                "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."

def test_report_matches():
    """
    Test that the module allows reporting of match outcomes
    """
    delete_matches()
    delete_players()
    register_player("Bruno Walton")
    register_player("Boots O'Neal")
    register_player("Cathy Burton")
    register_player("Diane Grant")
    standings = player_standings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    report_match(id1, id2)
    report_match(id3, id4)
    standings = player_standings()
    for (player_id, player_name, wins, matches) in standings:
        if matches != 1:
            raise ValueError("Each player should have one match recorded.")
        if player_id in (id1, id3) and wins != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif player_id in (id2, id4) and wins != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."

def test_pairings():
    """
    Test that the module can pair players appropriately based on
    their standings
    """
    delete_matches()
    delete_players()
    register_player("Twilight Sparkle")
    register_player("Fluttershy")
    register_player("Applejack")
    register_player("Pinkie Pie")
    standings = player_standings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    report_match(id1, id2)
    report_match(id3, id4)
    pairings = swiss_pairings()
    if len(pairings) != 2:
        raise ValueError(
                "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
                "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."

def test_win_and_match_counts():
    """
    This method will test a tournament with a larger
    number of players to make sure standings report
    the proper amount of win/loss totals for all players
    combined.
    """

    delete_matches()
    delete_players()
    register_player('Player One')
    register_player('Player Two')
    register_player('Player Three')
    register_player('Player Four')
    register_player('Player Five')
    register_player('Player Six')
    register_player('Player Seven')
    register_player('Player Eight')

    for r in range(4):
        pairings = swiss_pairings()
        i = 1
        for match in pairings:

            i += 1
            if i % 2 == 0:
                report_match(match[0], match[2])
            else:
                report_match(match[2], match[0])

    standings = player_standings()

    num_matches_doubled = 0
    num_wins = 0
    for player in standings:

        num_wins += player[2]
        num_matches_doubled += player[3]

    if num_matches_doubled / 2 != 16:
        raise ValueError(
            "Number of matches should be 16 for 8 players on 4 rounds"
        )

    if num_wins != 16:
        raise ValueError(
            "Number of wins should be 16 for 8 players on 4 rounds"
        )
    print "9. After 8 players go 4 rounnds there are " \
          "16 games played with 16 winners yielded"


if __name__ == '__main__':
    test_delete_matches()
    test_delete()
    test_count()
    test_register()
    test_register_count_delete()
    test_standings_before_matches()
    test_report_matches()
    test_pairings()
    test_win_and_match_counts()

    print "Success!  All tests pass!"
