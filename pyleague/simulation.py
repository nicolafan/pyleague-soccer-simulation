import random

from typing import Tuple

from . import models


def get_weight(x: models.Team, is_home: bool) -> int:

    x_weight = x.strength_value
    x_weight += x.attack_power
    x_weight += x.defense_power
    x_weight += x.form_value

    if is_home:
        x_weight += 20

    return x_weight


def evaluate_line(
    pt1: Tuple[float, float], pt2: Tuple[float, float], x: float
) -> float:
    y = (pt2[1] - pt1[1]) * (x - pt1[0]) / (pt2[0] - pt1[0]) + pt1[1]
    return y


def get_draw_weight(a_weight: int, b_weight: int) -> int:
    if b_weight > a_weight:
        a_weight, b_weight = b_weight, a_weight

    draw_line_pt1 = (0, 0.35)
    draw_line_pt2 = (0.18, 0.3)

    if a_weight == 0:
        return 0

    x = (a_weight - b_weight) / a_weight
    y = evaluate_line(draw_line_pt1, draw_line_pt2, x)

    draw_weight = ((y * a_weight) + (y * b_weight)) / (1 - y)
    return int(draw_weight)


def generate_outcome(team_a: models.Team, team_b: models.Team) -> str:
    a_weight = get_weight(team_a, is_home=True)
    b_weight = get_weight(team_b, is_home=False)
    d_weight = get_draw_weight(a_weight, b_weight)
    weights = [a_weight, d_weight, b_weight]
    outcome = random.choices(population=["1", "X", "2"], weights=weights, k=1)[0]
    return outcome


def evaluate_goal_weights(scorer_team: models.Team, defender_team: models.Team, with_zero: bool):
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
    goal_weights = evaluate_goal_weights(team_winner, team_loser, False)
    goals_w = random.choices(population=[1, 2, 3, 4], weights=goal_weights, k=1)[0]

    possible_away = [0]
    for i in range(1, goals_w):
        possible_away.append(i)

    goal_weights = evaluate_goal_weights(team_winner, team_loser, True)
    goal_weights = goal_weights[:len(possible_away)]
    goals_l = random.choices(population=possible_away, weights=goal_weights, k=1)[0]

    return goals_w, goals_l


def get_drawing_score(team_a: models.Team, team_b: models.Team):
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


def generate_result(team_a: models.Team, team_b: models.Team, outcome: str) -> Tuple[int, int]:
    goals_home = 0
    goals_away = 0

    if outcome == "1":
        goals_home, goals_away = get_winning_score(team_a, team_b)
    elif outcome == "2":
        goals_away, goals_home = get_winning_score(team_b, team_a)
    else:
        goals_home, goals_away = get_drawing_score(team_a, team_b)
    return goals_home, goals_away
