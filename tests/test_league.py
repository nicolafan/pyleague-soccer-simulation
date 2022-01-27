from typing import List

import pytest

from pyleague import league, util
from pyleague.models import Team


def test_create_league():
    league_name = util.get_random_string(10)

    teams_fail_1: List[Team] = [util.get_random_team()]

    teams_fail_2: List[Team] = []
    for i in range(41):
        teams_fail_2.append(util.get_random_team())

    teams_fail_3: List[Team] = []
    for i in range(13):
        teams_fail_3.append(util.get_random_team())

    teams_fail_4: List[Team] = []
    x = util.get_random_team()
    x.identifier = "equ"
    teams_fail_4.append(x)
    x = util.get_random_team()
    x.identifier = "equ"
    teams_fail_4.append(x)

    teams_ok: List[Team] = []
    for i in range(20):
        teams_ok.append(util.get_random_team())

    with pytest.raises(ValueError):
        league.create_league(league_name, teams_fail_1)
    with pytest.raises(ValueError):
        league.create_league(league_name, teams_fail_2)
    with pytest.raises(ValueError):
        league.create_league(league_name, teams_fail_3)
    with pytest.raises(ValueError):
        league.create_league(league_name, teams_fail_4)

    tournament = league.create_league(league_name, teams_ok)
    assert tournament is not None


def test_generate_fixtures():
    league_name = util.get_random_string(10)
    teams: List[Team] = []
    played = {}
    for i in range(20):
        random_team = util.get_random_team()
        teams.append(random_team)
        played[random_team.identifier] = {"home": 0, "away": 0}

    tournament = league.League(name=league_name, teams=teams)

    assert len(tournament.fixtures) == tournament.n_participants * 2 - 2

    for matchday in tournament.fixtures:
        for (x, y) in matchday:
            played[x]["home"] += 1
            played[y]["away"] += 1
        playing_teams = [team for game in matchday for team in game]
        assert len(playing_teams) == len(set(playing_teams))

    for team in played:
        assert (
            played[team]["home"] == 19 and played[team]["home"] == played[team]["away"]
        )
