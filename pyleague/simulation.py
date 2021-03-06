"""Simulation

This module contains the functions for the simulation of the games.
Simulation regards different aspects: the final outcome, the final results, minute of the goals etc.
"""

import random
from typing import Tuple, List
import models

def get_weight(team: models.Team, is_home: bool) -> int:
    """Produces the weight of a team

    The weight is the basic number which will determine a team's probability of winning the game when compared to
    the weight of the opponent.
    It is given by the sum of the different parameters which characterize a single team.
    This makes it very easy to add new parameters that will determine the measurement of the probabilities.

    :param team: team whose weight must be calculated
    :param is_home: specifies if the team will play the game at home, this will give the team an extra weight
    :return: a positive number (strictly greater than 0) representing the weight of the team
    """

    team_weight = 0
    team_weight += team.strength_value
    team_weight += team.attack_power
    team_weight += team.defense_power
    team_weight += team.form_value

    if is_home:
        team_weight += 20

    if team_weight <= 0:
        raise ValueError

    return team_weight


def evaluate_line(
    pt1: Tuple[float, float], pt2: Tuple[float, float], x: float
) -> float:
    """Evaluates f(x) where f is a line between two points

    Applies the formula of the line passing between two points.

    :param pt1: first point of the line
    :param pt2: second point of the line
    :param x: function input
    :return: f(x)
    """

    y = (pt2[1] - pt1[1]) * (x - pt1[0]) / (pt2[0] - pt1[0]) + pt1[1]
    return y


def get_relative_distance(x: float, y: float) -> float:
    """Evaluates the relative distance between two values

    :param: x: first value
    :param: y: second value
    :return: relative distance
    """
    return (x - y) / max(abs(x), abs(y))


def get_draw_weight(a_weight: int, b_weight: int) -> int:
    """Produces the weight of the draw outcome (represented by 'X')

    Once we have two team weights, we should allocate some weight to the possibility of a draw, since its probability
    is never 0.
    The probability of a draw is a function of the relative distance between two points.
    If the relative distance is small, there will be a higher probability of draw.
    If the relative distance is large, then a team is much better than the other.
    When the draw probability is small (because there is a much better team), it has always
    this probability must be greater than the probability that the weaker team could win.

    :param a_weight: weight of the first team
    :param b_weight: weight of the second team
    :return: weight of the draw
    """
    if b_weight > a_weight:
        a_weight, b_weight = b_weight, a_weight

    # the first point of the line: if the teams have an equal weight, draw probability is 0.35
    draw_line_pt1 = (0, 0.35)

    # second point of the line (measured after observations)
    draw_line_pt2 = (0.18, 0.3)

    # TODO: this should never happen
    if a_weight == 0:
        return 0

    x = get_relative_distance(a_weight, b_weight)
    y = evaluate_line(draw_line_pt1, draw_line_pt2, x)

    # once we have value y we should transform it in a conformable weight
    draw_weight = ((y * a_weight) + (y * b_weight)) / (1 - y)
    return int(draw_weight)


def generate_outcome(team_a: models.Team, team_b: models.Team) -> str:
    """Generates the match outcome for a game between two teams 
    
    :param team_a: the first team that is taking part in the match
    :type team_a: Team
    :param team_b: the second team that is taking part in the match
    :type team_b: Team
    :return: either 1, X, or 2 indicating which team won the match (X is for ties)
    :rtype: str
    """
    a_weight = get_weight(team_a, is_home=True)
    b_weight = get_weight(team_b, is_home=False)
    d_weight = get_draw_weight(a_weight, b_weight)
    weights = [a_weight, d_weight, b_weight]
    outcome = random.choices(population=["1", "X", "2"], weights=weights, k=1)[0]
    return outcome


def evaluate_goal_weights(
    scorer_team: models.Team, defender_team: models.Team, with_zero: bool
):
    """Evaluates the weight-age for a goal 

    :param scorer_team: the Team that is visiting (is away) the second team in a match
    :type scorer_team: models.Team
    :param defender_team: the Team that is at home against the first team in a match
    :type defender_team: models.Team
    :param with_zero: (not sure)
    :type with_zero: bool
    :return: (not sure)
    :rtype: List[int]
    """
    goal_0_line = ((0, 0.3), (0.96, 0.05))

    goal_1_line = ((0, 0.5), (0.96, 0.2))
    goal_2_line = ((0, 0.3), (0.96, 0.5))
    goal_3_line = ((0, 0.2), (0.96, 0.4))
    goal_4_line = ((0, 0.1), (0.96, 0.3))

    x = (scorer_team.attack_power - defender_team.attack_power) / max(
        abs(scorer_team.attack_power), abs(defender_team.defense_power)
    )
    w_0 = evaluate_line(goal_0_line[0], goal_0_line[1], x)
    w_1 = evaluate_line(goal_1_line[0], goal_1_line[1], x)
    w_2 = evaluate_line(goal_2_line[0], goal_2_line[1], x)
    w_3 = evaluate_line(goal_3_line[0], goal_3_line[1], x)
    w_4 = evaluate_line(goal_4_line[0], goal_4_line[1], x)
    if w_3 <= 0.0:
        w_3 = 0.05
    if w_4 <= 0.0:
        w_4 = 0.05

    weights = [w_1, w_2, w_3, w_4]
    if with_zero:
        weights.insert(0, w_0)
    return [w_1, w_2, w_3, w_4]


def get_winning_score(team_winner: models.Team, team_loser: models.Team):
    """Evaluates the number of goals both teams score in a match 

    :param team_winner: the Team object that wins in a match
    :type team_winner: models.Team
    :param team_loser: the Team object that loses in a match
    :type team_loser: models.Team
    :return: the number of goals both teams score in a match
    :rtype: Tuple[int, int]
    """
    goal_weights = evaluate_goal_weights(team_winner, team_loser, False)
    goals_w = random.choices(population=[1, 2, 3, 4], weights=goal_weights, k=1)[0]

    possible_away = [0]
    for i in range(1, goals_w):
        possible_away.append(i)

    goal_weights = evaluate_goal_weights(team_winner, team_loser, True)
    goal_weights = goal_weights[: len(possible_away)]
    goals_l = random.choices(population=possible_away, weights=goal_weights, k=1)[0]

    return goals_w, goals_l


def get_drawing_score(team_a: models.Team, team_b: models.Team):
    """Evaluates the drawing score

    :param team_a: the first team that takes part in a match
    :type team_a: models.Team
    :param team_b: the second team that takes part in a match
    :type team_b: models.Team
    :return: (not sure)
    :rtype: Tuple[float, float], Tuple[int, int]
    """

    # TODO: use a cycle
    goal_0_line = ((-0.1, 0.4), (0.1, 0.3))
    goal_1_line = ((-0.1, 0.3), (0.1, 0.4))
    goal_2_line = ((-0.1, 0.2), (0.1, 0.3))
    goal_3_line = ((-0.1, 0.15), (0.1, 0.2))
    goal_4_line = ((-0.1, 0.05), (0.1, 0.1))

    attacks_sum = team_a.attack_power + team_b.attack_power
    defenses_sum = team_a.defense_power + team_b.defense_power

    x = (attacks_sum - defenses_sum) / abs(max(attacks_sum, defenses_sum))

    w_0 = evaluate_line(goal_0_line[0], goal_0_line[1], x)
    w_1 = evaluate_line(goal_1_line[0], goal_1_line[1], x)
    w_2 = evaluate_line(goal_2_line[0], goal_2_line[1], x)
    w_3 = evaluate_line(goal_3_line[0], goal_3_line[1], x)
    w_4 = evaluate_line(goal_4_line[0], goal_4_line[1], x)

    weights = [w_0, w_1, w_2, w_3, w_4]
    goals = random.choices(population=[0, 1, 2, 3, 4], weights=weights, k=1)[0]

    return goals, goals


def generate_result(
    team_a: models.Team, team_b: models.Team, outcome: str
) -> Tuple[int, int]:
    """Generates the result of a pairing between two teams (depending on what condition the game is held under, i.e. at home or away)

    :param team_a: the first team that is taking part in the match
    :type team_a: models.Team
    :param team_b: the second team that is taking part in the match
    :type team_b: models.Team
    :param outcome: number representing the winner of the match: 1, 2, X (X is for ties)
    :type outcome: str
    :return: the number of goals both teams, one at home and the one away, score in a match 
    :rtype: Tuple[int, int]
    """
    if outcome == "1":
        goals_home, goals_away = get_winning_score(team_a, team_b)
    elif outcome == "2":
        goals_away, goals_home = get_winning_score(team_b, team_a)
    else:
        goals_home, goals_away = get_drawing_score(team_a, team_b)
    return goals_home, goals_away


def generate_time_for_goals(goals_h: int, goals_a: int) -> Tuple[List[int], List[int]]:
    """Generates the times during the game when both the home team and the away team score a goal

    :param goals_h: the number of goals the home team scores
    :type goals_h: int
    :param goals_a: the number of goals the away team scores
    :type goals_a: int
    :return: two lists containing the time in minutes during the match for when the home team and the away team score, respectively
    :rtype: Tuple[List[int], List[int]]
    """
    goal_mins = random.sample([i for i in range(91)], goals_h + goals_a)
    mins_goal_h = goal_mins[:goals_h]
    mins_goal_a = goal_mins[goals_h : goals_h + goals_a]
    return mins_goal_h, mins_goal_a
